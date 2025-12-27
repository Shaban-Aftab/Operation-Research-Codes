"""
===============================================================
INTEGER LINEAR PROGRAMMING (ILP) SOLVER
Branch & Bound Method with Simplex for LP Relaxation
===============================================================

Supports:
- Pure Integer Programming (all variables integer)
- Mixed Integer Programming (some integer, some continuous)
- Binary Integer Programming (0/1 variables)

Features:
- Branch and Bound algorithm
- Simplex method for LP relaxation
- Big M method for >= and = constraints
- Tree visualization
- Top-N solutions

"""

import copy
import math


# ============================================================
# SIMPLEX SOLVER FOR LP RELAXATION
# ============================================================

class SimplexSolver:
    """Simplex solver for LP relaxation in Branch & Bound"""
    
    def __init__(self, objective, constraints, rhs, constraint_types, is_maximization=True, verbose=False):
        self.num_variables = len(objective)
        self.num_constraints = len(constraints)
        self.objective = objective[:]
        self.constraints = [row[:] for row in constraints]
        self.rhs = rhs[:]
        self.constraint_types = constraint_types[:]
        self.is_maximization = is_maximization
        self.tableau = None
        self.basic_vars = []
        self.var_names = []
        self.M = 10000
        self.is_feasible = True
        self.is_unbounded = False
        self.verbose = verbose
        self.use_big_m = any(t in [2, 3] for t in self.constraint_types)
    
    def create_initial_tableau(self):
        """Create initial simplex tableau"""
        # Convert >= constraints to <= by negating
        # For ax >= b, convert to -ax <= -b
        self.converted_constraints = []
        self.converted_rhs = []
        self.converted_types = []
        
        for i in range(self.num_constraints):
            if self.constraint_types[i] == 2:  # >= constraint
                # Convert to <=: negate both sides
                self.converted_constraints.append([-c for c in self.constraints[i]])
                self.converted_rhs.append(-self.rhs[i])
                self.converted_types.append(1)  # Now it's <=
            else:
                self.converted_constraints.append(self.constraints[i][:])
                self.converted_rhs.append(self.rhs[i])
                self.converted_types.append(self.constraint_types[i])
        
        num_slack = sum(1 for t in self.converted_types if t == 1)
        num_artificial = sum(1 for t in self.converted_types if t == 3)
        
        total_vars = self.num_variables + num_slack + num_artificial
        num_rows = self.num_constraints + 1
        num_cols = total_vars + 1
        
        self.tableau = [[0.0 for _ in range(num_cols)] for _ in range(num_rows)]
        self.var_names = [f"x{i+1}" for i in range(self.num_variables)]
        
        slack_idx = self.num_variables
        artificial_idx = self.num_variables + num_slack
        
        self.basic_vars = []
        
        # Fill constraint rows
        for i in range(self.num_constraints):
            for j in range(self.num_variables):
                self.tableau[i][j] = self.converted_constraints[i][j]
            
            if self.converted_types[i] == 1:  # <=
                self.tableau[i][slack_idx] = 1
                self.var_names.append(f"s{i+1}")
                self.basic_vars.append(slack_idx)
                slack_idx += 1
            else:  # == (use artificial variable)
                self.tableau[i][artificial_idx] = 1
                self.var_names.append(f"a{i+1}")
                self.basic_vars.append(artificial_idx)
                artificial_idx += 1
            
            self.tableau[i][-1] = self.converted_rhs[i]
        
        # Fill objective row
        for j in range(self.num_variables):
            if self.is_maximization:
                self.tableau[-1][j] = -self.objective[j]
            else:
                self.tableau[-1][j] = self.objective[j]
        
        # Big M for artificial variables
        if num_artificial > 0:
            art_start = self.num_variables + num_slack
            for i in range(self.num_constraints):
                if self.converted_types[i] == 3:  # Equality constraint
                    # Find the artificial variable column for this row
                    art_col = self.basic_vars[i]
                    if art_col >= art_start:
                        # Add Big M penalty to objective
                        if self.is_maximization:
                            self.tableau[-1][art_col] = self.M
                        else:
                            self.tableau[-1][art_col] = -self.M
                        
                        # Eliminate artificial variable from objective row
                        for j in range(num_cols):
                            if self.is_maximization:
                                self.tableau[-1][j] -= self.M * self.tableau[i][j]
                            else:
                                self.tableau[-1][j] += self.M * self.tableau[i][j]

    
    def find_pivot_column(self):
        """Find entering variable"""
        obj_row = self.tableau[-1][:-1]
        
        if self.is_maximization:
            min_val = min(obj_row)
            if min_val >= -1e-10:
                return -1
            return obj_row.index(min_val)
        else:
            max_val = max(obj_row)
            if max_val <= 1e-10:
                return -1
            return obj_row.index(max_val)
    
    def find_pivot_row(self, pivot_col):
        """Find leaving variable using minimum ratio test"""
        ratios = []
        for i in range(len(self.tableau) - 1):
            if self.tableau[i][pivot_col] > 1e-10:
                ratio = self.tableau[i][-1] / self.tableau[i][pivot_col]
                ratios.append((ratio, i))
        
        if not ratios:
            return -1
        
        ratios.sort()
        return ratios[0][1]
    
    def perform_pivot(self, pivot_row, pivot_col):
        """Perform pivot operation"""
        self.basic_vars[pivot_row] = pivot_col
        pivot_element = self.tableau[pivot_row][pivot_col]
        
        # Normalize pivot row
        for j in range(len(self.tableau[pivot_row])):
            self.tableau[pivot_row][j] /= pivot_element
        
        # Eliminate pivot column in other rows
        for i in range(len(self.tableau)):
            if i != pivot_row:
                factor = self.tableau[i][pivot_col]
                for j in range(len(self.tableau[i])):
                    self.tableau[i][j] -= factor * self.tableau[pivot_row][j]
    
    def solve(self):
        """Solve LP using simplex"""
        self.create_initial_tableau()
        
        max_iterations = 100
        for iteration in range(max_iterations):
            pivot_col = self.find_pivot_column()
            if pivot_col == -1:
                break
            
            pivot_row = self.find_pivot_row(pivot_col)
            if pivot_row == -1:
                self.is_unbounded = True
                return None, None
            
            self.perform_pivot(pivot_row, pivot_col)
        
        # Check for infeasibility (artificial variables in basis)
        for i, bv in enumerate(self.basic_vars):
            if bv < len(self.var_names) and self.var_names[bv].startswith('a'):
                if self.tableau[i][-1] > 1e-6:
                    self.is_feasible = False
                    return None, None
        
        # Extract solution
        solution = {f"x{i+1}": 0.0 for i in range(self.num_variables)}
        for i, bv in enumerate(self.basic_vars):
            if bv < self.num_variables:
                solution[f"x{bv+1}"] = self.tableau[i][-1]
        
        # Verify solution against CONVERTED constraints
        for i in range(len(self.converted_constraints)):
            lhs = sum(self.converted_constraints[i][j] * solution[f"x{j+1}"] for j in range(self.num_variables))
            rhs_val = self.converted_rhs[i]
            
            # All converted constraints are <= or =
            if self.converted_types[i] == 1:  # <=
                if lhs > rhs_val + 1e-6:
                    self.is_feasible = False
                    return None, None
            elif self.converted_types[i] == 3:  # =
                if abs(lhs - rhs_val) > 1e-6:
                    self.is_feasible = False
                    return None, None
        
        obj_value = sum(self.objective[j] * solution[f"x{j+1}"] for j in range(self.num_variables))
        
        return solution, obj_value


# ============================================================
# TREE NODE FOR VISUALIZATION
# ============================================================

class TreeNode:
    def __init__(self, node_id, parent_id=None, branch_constraint="", depth=0):
        self.node_id = node_id
        self.parent_id = parent_id
        self.branch_constraint = branch_constraint
        self.depth = depth
        self.solution = None
        self.obj_value = None
        self.status = ""
        self.left_child = None
        self.right_child = None
        self.is_optimal = False


# ============================================================
# INTEGER LINEAR PROGRAMMING SOLVER
# ============================================================

class ILPSolver:
    """Complete ILP solver with Pure/Mixed/Binary support"""
    
    def __init__(self):
        self.objective = []
        self.constraints = []
        self.rhs = []
        self.constraint_types = []
        self.is_maximization = True
        self.num_variables = 0
        self.num_constraints = 0
        
        # Integer variable specifications
        self.integer_vars = []  # Indices of integer variables
        self.binary_vars = []   # Indices of binary (0/1) variables
        self.ilp_type = 1  # 1=Pure, 2=Mixed, 3=Binary
        
        # Solution tracking
        self.best_solution = None
        self.best_obj_value = None
        self.nodes_explored = 0
        self.iteration = 0
        self.tree_nodes = {}
        self.root_node = None
        self.optimal_path = []
        self.top_n = 1
        self.top_solutions = []
    
    def get_user_input(self):
        """Get problem input from user"""
        print("\n" + "=" * 70)
        print("      INTEGER LINEAR PROGRAMMING (ILP) SOLVER")
        print("           Branch & Bound with Tree Visualization")
        print("=" * 70)
        
        # Problem type
        print("\nSelect Problem Type:")
        print("1. Maximization")
        print("2. Minimization")
        
        while True:
            try:
                choice = int(input("Enter choice (1 or 2): "))
                if choice in [1, 2]:
                    self.is_maximization = (choice == 1)
                    break
                print("Please enter 1 or 2")
            except ValueError:
                print("Invalid input!")
        
        # Number of variables
        while True:
            try:
                self.num_variables = int(input("\nEnter the number of decision variables: "))
                if self.num_variables > 0:
                    break
            except ValueError:
                print("Invalid input!")
        
        # Number of constraints
        while True:
            try:
                self.num_constraints = int(input("Enter the number of constraints: "))
                if self.num_constraints > 0:
                    break
            except ValueError:
                print("Invalid input!")
        
        # Objective function
        print(f"\n--- OBJECTIVE FUNCTION ---")
        print(f"Enter coefficients for Z = c1*x1 + c2*x2 + ... + c{self.num_variables}*x{self.num_variables}")
        
        for i in range(self.num_variables):
            while True:
                try:
                    coef = float(input(f"  Coefficient of x{i+1}: "))
                    self.objective.append(coef)
                    break
                except ValueError:
                    print("  Invalid input!")
        
        # Constraints
        print(f"\n--- CONSTRAINTS ---")
        print("Constraint types: 1 = <=, 2 = >=, 3 = =, 4 = <, 5 = >")
        
        for i in range(self.num_constraints):
            print(f"\nConstraint {i+1}:")
            constraint = []
            
            for j in range(self.num_variables):
                while True:
                    try:
                        coef = float(input(f"  Coefficient of x{j+1}: "))
                        constraint.append(coef)
                        break
                    except ValueError:
                        print("  Invalid input!")
            
            self.constraints.append(constraint)
            
            while True:
                try:
                    ctype = int(input("  Constraint type (1=<=, 2=>=, 3==, 4=<, 5=>): "))
                    if ctype in [1, 2, 3, 4, 5]:
                        if ctype == 4:
                            print("  Note: '<' constraint will be treated as '<='")
                            self.constraint_types.append(1)
                        elif ctype == 5:
                            print("  Note: '>' constraint will be treated as '>='")
                            self.constraint_types.append(2)
                        else:
                            self.constraint_types.append(ctype)
                        break
                    print("  Please enter 1, 2, 3, 4, or 5")
                except ValueError:
                    print("  Invalid input!")
            
            while True:
                try:
                    rhs = float(input("  Right-hand side (RHS) value: "))
                    self.rhs.append(rhs)
                    break
                except ValueError:
                    print("  Invalid input!")
        
        # Integer variable specification
        print(f"\n--- INTEGER VARIABLES ---")
        print("Which variables must be integers?")
        print("1. All variables must be integers")
        print("2. Select specific variables")
        
        while True:
            try:
                choice = int(input("Enter choice (1 or 2): "))
                if choice == 1:
                    self.integer_vars = list(range(self.num_variables))
                    self.ilp_type = 1  # Pure Integer
                    break
                elif choice == 2:
                    var_input = input(f"Enter variable numbers (1 to {self.num_variables}) separated by commas: ")
                    self.integer_vars = [int(x.strip()) - 1 for x in var_input.split(",") if x.strip()]
                    self.ilp_type = 2  # Mixed Integer
                    break
                print("Please enter 1 or 2")
            except ValueError:
                print("Invalid input!")
        
        # Binary variables (optional)
        print("\n--- BINARY VARIABLES (optional) ---")
        print("Are any variables binary (0/1)?")
        binary_input = input(f"Enter variable numbers (1-{self.num_variables}) separated by commas (or press Enter to skip): ").strip()
        if binary_input:
            self.binary_vars = [int(x.strip()) - 1 for x in binary_input.split(",") if x.strip()]
            if len(self.binary_vars) == self.num_variables:
                self.ilp_type = 3  # Binary
        
        # Top solutions
        print(f"\n--- TOP SOLUTIONS ---")
        while True:
            try:
                self.top_n = int(input("How many top solutions to display? (default=1): ") or "1")
                if self.top_n > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Invalid input!")
        
        self.display_problem()
    
    def display_problem(self):
        """Display formulated problem"""
        print("\n" + "=" * 70)
        print("            FORMULATED ILP PROBLEM")
        print("=" * 70)
        
        obj_type = "Maximize" if self.is_maximization else "Minimize"
        terms = []
        for i, c in enumerate(self.objective):
            if c >= 0 and i > 0:
                terms.append(f"+ {c}x{i+1}")
            elif c < 0:
                terms.append(f"- {abs(c)}x{i+1}")
            else:
                terms.append(f"{c}x{i+1}")
        
        print(f"\n{obj_type} Z = " + " ".join(terms))
        
        print("\nSubject to:")
        type_symbols = {1: "<=", 2: ">=", 3: "="}
        
        for i in range(self.num_constraints):
            terms = []
            for j, c in enumerate(self.constraints[i]):
                if c >= 0 and j > 0:
                    terms.append(f"+ {c}x{j+1}")
                elif c < 0:
                    terms.append(f"- {abs(c)}x{j+1}")
                else:
                    terms.append(f"{c}x{j+1}")
            symbol = type_symbols.get(self.constraint_types[i], "<=")
            print(f"  " + " ".join(terms) + f" {symbol} {self.rhs[i]}")
        
        # Integer constraints
        int_vars = ", ".join([f"x{i+1}" for i in self.integer_vars])
        print(f"\n  Integer constraint: {int_vars} must be integers")
        
        if self.binary_vars:
            bin_vars = ", ".join([f"x{i+1}" for i in self.binary_vars])
            print(f"  Binary constraint: {bin_vars} ∈ {{0, 1}}")
        
        print("  All variables >= 0")
    
    def is_integer_solution(self, solution):
        """Check if solution satisfies integer constraints"""
        if solution is None:
            return False
        
        for i in self.integer_vars:
            val = solution[f"x{i+1}"]
            if abs(val - round(val)) > 1e-6:
                return False
        
        return True
    
    def find_branching_variable(self, solution):
        """Find variable to branch on (most fractional)"""
        max_frac = 0
        branch_var = None
        branch_val = None
        
        for i in self.integer_vars:
            val = solution[f"x{i+1}"]
            frac = abs(val - round(val))
            
            if frac > 1e-6 and frac > max_frac:
                max_frac = frac
                branch_var = i
                branch_val = val
        
        return branch_var, branch_val
    
    def solve_subproblem(self, extra_constraints):
        """Solve LP relaxation with extra branch constraints"""
        all_constraints = [row[:] for row in self.constraints] + [c[0] for c in extra_constraints]
        all_rhs = self.rhs[:] + [c[1] for c in extra_constraints]
        all_types = self.constraint_types[:] + [c[2] for c in extra_constraints]
        
        # Add binary constraints as bounds
        for i in self.binary_vars:
            if i not in [c[3] if len(c) > 3 else -1 for c in extra_constraints]:
                # x_i <= 1
                coef = [0.0] * self.num_variables
                coef[i] = 1.0
                all_constraints.append(coef)
                all_rhs.append(1.0)
                all_types.append(1)
        
        solver = SimplexSolver(
            self.objective,
            all_constraints,
            all_rhs,
            all_types,
            self.is_maximization,
            verbose=False
        )
        
        return solver.solve()
    
    def solve(self):
        """Main Branch & Bound algorithm"""
        print("\n" + "=" * 70)
        print("         SOLVING USING BRANCH & BOUND")
        print("=" * 70)
        
        # Solve root LP relaxation
        print("\n" + "-" * 50)
        print("STEP 1: LP Relaxation (Root Node)")
        print("-" * 50)
        
        root_solution, root_obj = self.solve_subproblem([])
        self.nodes_explored = 1
        
        root = TreeNode(0, None, "ROOT", 0)
        root.solution = root_solution
        root.obj_value = root_obj
        self.tree_nodes[0] = root
        self.root_node = root
        
        if root_solution is None:
            print("Problem is INFEASIBLE!")
            root.status = "INFEASIBLE"
            return
        
        print(f"\nLP Relaxation Solution:")
        for i in range(self.num_variables):
            print(f"  x{i+1} = {root_solution[f'x{i+1}']:.4f}")
        print(f"  Z = {root_obj:.4f}")
        
        if self.is_integer_solution(root_solution):
            print("\n>>> LP solution is already integer! Optimal found.")
            root.status = "INTEGER"
            root.is_optimal = True
            self.best_solution = root_solution
            self.best_obj_value = root_obj
            self.optimal_path = [0]
            self.top_solutions = [(root_obj, root_solution, [0])]
            self.display_final_solution()
            return
        
        root.status = "BRANCHED"
        
        # Initialize best bound
        if self.is_maximization:
            self.best_obj_value = float('-inf')
        else:
            self.best_obj_value = float('inf')
        
        # Branch and Bound queue
        queue = [([], root_obj, 0, "", 0)]
        
        print("\n" + "-" * 50)
        print("STEP 2: Branch & Bound Iterations")
        print("-" * 50)
        
        node_counter = 0
        
        while queue:
            self.iteration += 1
            
            # Best-first search
            if self.is_maximization:
                queue.sort(key=lambda x: x[1], reverse=True)
            else:
                queue.sort(key=lambda x: x[1])
            
            current_constraints, bound, parent_id, branch_info, depth = queue.pop(0)
            
            if depth == 0 and self.iteration > 1:
                continue
            
            print(f"\n{'*' * 60}")
            print(f"ITERATION {self.iteration}")
            print("*" * 60)
            
            # Solve subproblem
            solution, obj_value = self.solve_subproblem(current_constraints)
            
            # Create tree node
            if depth > 0:
                node_counter += 1
                current_node_id = node_counter
                node = TreeNode(current_node_id, parent_id, branch_info, depth)
                node.solution = solution
                node.obj_value = obj_value
                self.tree_nodes[current_node_id] = node
                
                parent_node = self.tree_nodes[parent_id]
                if parent_node.left_child is None:
                    parent_node.left_child = current_node_id
                else:
                    parent_node.right_child = current_node_id
                
                print(f"Node {current_node_id}: {branch_info}")
            else:
                current_node_id = 0
                node = self.tree_nodes[0]
            
            if solution is None:
                print("  Result: INFEASIBLE - Pruned")
                node.status = "INFEASIBLE"
                continue
            
            print(f"\n  LP Solution:")
            for i in range(self.num_variables):
                val = solution[f"x{i+1}"]
                is_int = abs(val - round(val)) < 1e-6
                marker = "" if is_int else " (fractional)"
                print(f"    x{i+1} = {val:.4f}{marker}")
            print(f"    Z = {obj_value:.4f}")
            
            # Bound check
            worst_in_top = self.top_solutions[-1][0] if len(self.top_solutions) >= self.top_n else (float('-inf') if self.is_maximization else float('inf'))
            
            if self.is_maximization and obj_value <= worst_in_top:
                print(f"  Result: PRUNED (bound {obj_value:.4f} <= {worst_in_top:.4f})")
                node.status = "PRUNED"
                continue
            elif not self.is_maximization and obj_value >= worst_in_top:
                print(f"  Result: PRUNED (bound {obj_value:.4f} >= {worst_in_top:.4f})")
                node.status = "PRUNED"
                continue
            
            # Check if integer
            if self.is_integer_solution(solution):
                print(f"  Result: INTEGER SOLUTION FOUND!")
                node.status = "INTEGER"
                
                solution_copy = {k: v for k, v in solution.items()}
                path = []
                trace_id = current_node_id
                while trace_id is not None:
                    path.insert(0, trace_id)
                    trace_id = self.tree_nodes[trace_id].parent_id
                
                self.top_solutions.append((obj_value, solution_copy, path))
                
                if self.is_maximization:
                    self.top_solutions.sort(key=lambda x: x[0], reverse=True)
                else:
                    self.top_solutions.sort(key=lambda x: x[0])
                
                if len(self.top_solutions) > self.top_n:
                    self.top_solutions = self.top_solutions[:self.top_n]
                
                if self.top_solutions:
                    self.best_obj_value = self.top_solutions[0][0]
                    self.best_solution = self.top_solutions[0][1]
                    self.optimal_path = self.top_solutions[0][2]
                    
                    for nid in self.tree_nodes:
                        self.tree_nodes[nid].is_optimal = (nid in self.optimal_path)
                
                print(f"  >>> Solution #{len(self.top_solutions)} with Z = {obj_value:.4f}")
                continue
            
            # Branch
            var_idx, frac_val = self.find_branching_variable(solution)
            floor_val = math.floor(frac_val)
            ceil_val = math.ceil(frac_val)
            
            node.status = "BRANCHED"
            
            print(f"\n  Branching on x{var_idx+1} = {frac_val:.4f}")
            print(f"    Left:  x{var_idx+1} <= {floor_val}")
            print(f"    Right: x{var_idx+1} >= {ceil_val}")
            
            coef = [0.0] * self.num_variables
            coef[var_idx] = 1.0
            
            # Left branch
            left_constraints = current_constraints + [(coef[:], floor_val, 1, var_idx)]
            left_info = f"x{var_idx+1} <= {floor_val}"
            queue.append((left_constraints, obj_value, current_node_id, left_info, depth + 1))
            
            # Right branch
            right_constraints = current_constraints + [(coef[:], ceil_val, 2, var_idx)]
            right_info = f"x{var_idx+1} >= {ceil_val}"
            queue.append((right_constraints, obj_value, current_node_id, right_info, depth + 1))
        
        # Draw tree visualization
        self.draw_tree()
        
        # Display final solution
        self.display_final_solution()
    
    
    def draw_tree(self):
        """Draw Branch & Bound tree visualization"""
        if not self.tree_nodes:
            return
        
        print("\n" + "=" * 70)
        print("              BRANCH & BOUND TREE")
        print("=" * 70)
        print("\nLegend:")
        print("  ✓ = Integer solution (optimal)")
        print("  ● = Integer solution")
        print("  ○ = Fractional (branched)")
        print("  ✗ = Infeasible/Pruned")
        print()
        
        self._draw_node_recursive(0, "", True)
    
    def _draw_node_recursive(self, node_id, prefix, is_last):
        """Recursively draw tree nodes"""
        if node_id not in self.tree_nodes:
            return
        
        node = self.tree_nodes[node_id]
        
        # Node marker
        if node.is_optimal:
            marker = "✓"
        elif node.status == "INTEGER":
            marker = "●"
        elif node.status == "INFEASIBLE" or node.status == "PRUNED":
            marker = "✗"
        elif node.status == "BRANCHED":
            marker = "○"
        else:
            marker = "□"
        
        # Connector
        if node.depth == 0:
            connector = ""
            new_prefix = ""
        else:
            connector = "└── " if is_last else "├── "
            new_prefix = prefix + ("    " if is_last else "│   ")
        
        # Node info
        if node.depth == 0:
            info = f"LP{node_id+1} (Root)"
        else:
            info = f"LP{node_id+1}: {node.branch_constraint}"
        
        # Display node
        if node.solution:
            x_vals = ", ".join([f"x{i+1}={node.solution[f'x{i+1}']:.2f}" 
                               for i in range(min(self.num_variables, 3))])
            z_val = f"z={node.obj_value:.2f}"
            
            print(f"{prefix}{connector}{marker} {info}")
            print(f"{new_prefix}    {x_vals}, {z_val}")
            
            if node.status == "INTEGER":
                if node.is_optimal:
                    print(f"{new_prefix}    [OPTIMAL SOLUTION]")
                else:
                    print(f"{new_prefix}    [Integer solution]")
            elif node.status == "INFEASIBLE":
                print(f"{new_prefix}    [Infeasible]")
            elif node.status == "PRUNED":
                print(f"{new_prefix}    [Pruned by bound]")
        else:
            print(f"{prefix}{connector}{marker} {info}")
            print(f"{new_prefix}    [No solution - {node.status}]")
        
        # Draw children
        children = []
        if node.left_child is not None:
            children.append(node.left_child)
        if node.right_child is not None:
            children.append(node.right_child)
        
        for i, child_id in enumerate(children):
            self._draw_node_recursive(child_id, new_prefix, i == len(children) - 1)
    
    def display_final_solution(self):

        """Display final solution(s)"""
        print("\n" + "=" * 70)
        if self.top_n > 1:
            print(f"           TOP {len(self.top_solutions)} INTEGER SOLUTIONS")
        else:
            print("              OPTIMAL INTEGER SOLUTION")
        print("=" * 70)
        
        if not self.top_solutions:
            print("\nNo feasible integer solution found!")
            return
        
        print(f"\nNodes Explored: {len(self.tree_nodes)}")
        print(f"Iterations: {self.iteration}")
        print(f"Solutions Found: {len(self.top_solutions)}")
        
        for rank, (obj_val, solution, path) in enumerate(self.top_solutions, 1):
            print("\n" + "-" * 60)
            print(f"  SOLUTION #{rank}")
            print("-" * 60)
            
            print("\n  Decision Variables:")
            for i in range(self.num_variables):
                val = solution[f"x{i+1}"]
                if i in self.integer_vars:
                    print(f"    x{i+1} = {int(round(val))} (integer)")
                else:
                    print(f"    x{i+1} = {val:.4f}")
            
            print(f"\n  Objective Value Z = {obj_val:.4f}")
            
            path_str = " -> ".join([f"Node {nid}" for nid in path])
            print(f"  Solution Path: {path_str}")
        
        if self.top_n > 1 and len(self.top_solutions) > 1:
            print("\n" + "=" * 60)
            print("                SOLUTIONS SUMMARY")
            print("=" * 60)
            print(f"\n  {'Rank':<6}{'Z Value':<15}{'Solution':<30}")
            print("  " + "-" * 55)
            
            for rank, (obj_val, solution, _) in enumerate(self.top_solutions, 1):
                sol_str = ", ".join([f"x{i+1}={int(round(solution[f'x{i+1}']))}" for i in self.integer_vars])
                print(f"  {rank:<6}{obj_val:<15.4f}{sol_str:<30}")


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    """Main application"""
    print("\n" + "=" * 70)
    print("|" + " " * 8 + "INTEGER LINEAR PROGRAMMING SOLVER" + " " * 25 + "|")
    print("|" + " " * 10 + "Branch & Bound Algorithm" + " " * 32 + "|")
    print("|" + " " * 6 + "Pure • Mixed • Binary • Zero Dependencies" + " " * 17 + "|")
    print("=" * 70)
    
    while True:
        solver = ILPSolver()
        solver.get_user_input()
        
        input("\nPress ENTER to solve...")
        solver.solve()
        
        print("\n" + "-" * 70)
        choice = input("\nSolve another problem? (y/n): ").lower()
        if choice != 'y':
            print("\n" + "=" * 70)
            print("Thank you for using ILP Solver!")
            print("=" * 70 + "\n")
            break


if __name__ == "__main__":
    main()
