import copy
import math

class SimplexSolver:
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
    
    def display_tableau(self, iteration=0, pivot_row=None, pivot_col=None):
        """Display the current simplex tableau in a formatted table"""
        if not self.verbose:
            return
        
        method_name = "Big M Method" if self.use_big_m else "Simplex Method"
        print(f"\n  {'─'*70}")
        if iteration == 0:
            print(f"  INITIAL TABLEAU ({method_name})")
        else:
            print(f"  ITERATION {iteration} - {method_name}")
        print(f"  {'─'*70}")
        
        # Header row
        header = "  Basic  │"
        for j, name in enumerate(self.var_names):
            if j == pivot_col:
                header += f" *{name:>6}"
            else:
                header += f" {name:>7}"
        header += " │    RHS"
        print(header)
        print(f"  {'─'*7}┼{'─'*(8*len(self.var_names))}─┼{'─'*8}")
        
        # Constraint rows
        for i in range(len(self.tableau) - 1):
            basic_name = self.var_names[self.basic_vars[i]] if i < len(self.basic_vars) else "?"
            row_marker = " *" if i == pivot_row else "  "
            row = f"{row_marker}{basic_name:>5} │"
            for j in range(len(self.tableau[i]) - 1):
                val = self.tableau[i][j]
                if abs(val) < 1e-10:
                    val = 0
                if i == pivot_row and j == pivot_col:
                    row += f" [{val:>5.2f}]"
                else:
                    row += f" {val:>7.2f}"
            rhs_val = self.tableau[i][-1]
            if pivot_row == i:
                row += f" │{rhs_val:>7.2f} ← Pivot Row"
            else:
                row += f" │{rhs_val:>7.2f}"
            print(row)
        
        print(f"  {'─'*7}┼{'─'*(8*len(self.var_names))}─┼{'─'*8}")
        
        # Zj-Cj row
        zj_cj_row = "  Zj-Cj │"
        for j in range(len(self.tableau[-1]) - 1):
            val = self.tableau[-1][j]
            if abs(val) < 1e-10:
                val = 0
            if j == pivot_col:
                zj_cj_row += f" *{val:>6.2f}"
            else:
                zj_cj_row += f" {val:>7.2f}"
        obj_val = -self.tableau[-1][-1] if self.is_maximization else self.tableau[-1][-1]
        zj_cj_row += f" │ Z={obj_val:>5.2f}"
        print(zj_cj_row)
        print(f"  {'─'*70}")
        
        if pivot_col is not None and pivot_col >= 0:
            print(f"  Pivot Column: {self.var_names[pivot_col]} (index {pivot_col})")
        if pivot_row is not None and pivot_row >= 0:
            entering = self.var_names[pivot_col] if pivot_col is not None else "?"
            leaving = self.var_names[self.basic_vars[pivot_row]] if pivot_row < len(self.basic_vars) else "?"
            print(f"  Entering Variable: {entering}")
            print(f"  Leaving Variable: {leaving}")
    def create_initial_tableau(self):
        num_slack = sum(1 for t in self.constraint_types if t == 1)
        num_surplus = sum(1 for t in self.constraint_types if t == 2)
        num_artificial = sum(1 for t in self.constraint_types if t in [2, 3])
        total_vars = self.num_variables + num_slack + num_surplus + num_artificial
        num_rows = self.num_constraints + 1
        num_cols = total_vars + 1
        self.tableau = [[0.0 for _ in range(num_cols)] for _ in range(num_rows)]
        self.var_names = [f"x{i+1}" for i in range(self.num_variables)]
        slack_idx = self.num_variables
        surplus_idx = self.num_variables + num_slack
        artificial_idx = self.num_variables + num_slack + num_surplus
        self.basic_vars = []
        for i in range(self.num_constraints):
            for j in range(self.num_variables):
                self.tableau[i][j] = self.constraints[i][j]
            if self.constraint_types[i] == 1:
                self.tableau[i][slack_idx] = 1
                self.var_names.append(f"s{i+1}")
                self.basic_vars.append(slack_idx)
                slack_idx += 1
            elif self.constraint_types[i] == 2:
                self.tableau[i][surplus_idx] = -1
                self.var_names.append(f"e{i+1}")
                surplus_idx += 1
                self.tableau[i][artificial_idx] = 1
                self.var_names.append(f"a{i+1}")
                self.basic_vars.append(artificial_idx)
                artificial_idx += 1
            else:
                self.tableau[i][artificial_idx] = 1
                self.var_names.append(f"a{i+1}")
                self.basic_vars.append(artificial_idx)
                artificial_idx += 1
            self.tableau[i][-1] = self.rhs[i]
        for j in range(self.num_variables):
            if self.is_maximization:
                self.tableau[-1][j] = -self.objective[j]
            else:
                self.tableau[-1][j] = self.objective[j]
        for i in range(self.num_constraints):
            if self.constraint_types[i] in [2, 3]:
                for j in range(self.num_variables + num_slack + num_surplus, total_vars):
                    if self.tableau[i][j] == 1:
                        if self.is_maximization:
                            self.tableau[-1][j] = self.M
                        else:
                            self.tableau[-1][j] = -self.M
                        for k in range(len(self.tableau[-1])):
                            if self.is_maximization:
                                self.tableau[-1][k] -= self.M * self.tableau[i][k]
                            else:
                                self.tableau[-1][k] += self.M * self.tableau[i][k]
                        break
    def find_pivot_column(self):
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
        self.basic_vars[pivot_row] = pivot_col
        pivot_element = self.tableau[pivot_row][pivot_col]
        for j in range(len(self.tableau[pivot_row])):
            self.tableau[pivot_row][j] /= pivot_element
        for i in range(len(self.tableau)):
            if i != pivot_row:
                factor = self.tableau[i][pivot_col]
                for j in range(len(self.tableau[i])):
                    self.tableau[i][j] -= factor * self.tableau[pivot_row][j]
    def solve(self):
        self.create_initial_tableau()
        
        # Display initial tableau
        self.display_tableau(iteration=0)
        
        max_iterations = 100
        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            pivot_col = self.find_pivot_column()
            if pivot_col == -1:
                if self.verbose:
                    print(f"\n  >>> OPTIMAL SOLUTION FOUND after {iteration-1} iterations")
                break
            pivot_row = self.find_pivot_row(pivot_col)
            if pivot_row == -1:
                self.is_unbounded = True
                if self.verbose:
                    print(f"\n  >>> UNBOUNDED SOLUTION - No leaving variable found")
                return None, None
            
            # Display tableau with pivot info before pivoting
            if self.verbose:
                self.display_tableau(iteration=iteration, pivot_row=pivot_row, pivot_col=pivot_col)
            
            self.perform_pivot(pivot_row, pivot_col)
        
        # Display final tableau
        if self.verbose and iteration > 0:
            print(f"\n  {'─'*70}")
            print(f"  FINAL OPTIMAL TABLEAU")
            print(f"  {'─'*70}")
            self.display_tableau(iteration="Final")
        
        for i, bv in enumerate(self.basic_vars):
            if bv < len(self.var_names) and self.var_names[bv].startswith('a'):
                if self.tableau[i][-1] > 1e-6:
                    self.is_feasible = False
                    if self.verbose:
                        print(f"\n  >>> INFEASIBLE - Artificial variable {self.var_names[bv]} still in basis with value {self.tableau[i][-1]:.4f}")
                    return None, None
        solution = {f"x{i+1}": 0.0 for i in range(self.num_variables)}
        for i, bv in enumerate(self.basic_vars):
            if bv < self.num_variables:
                solution[f"x{bv+1}"] = self.tableau[i][-1]
        obj_value = sum(self.objective[j] * solution[f"x{j+1}"] for j in range(self.num_variables))
        return solution, obj_value

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

class BranchAndBound:
    def __init__(self):
        self.objective = []
        self.constraints = []
        self.rhs = []
        self.constraint_types = []
        self.is_maximization = True
        self.num_variables = 0
        self.num_constraints = 0
        self.integer_vars = []
        self.best_solution = None
        self.best_obj_value = None
        self.nodes_explored = 0
        self.iteration = 0
        self.tree_nodes = {}
        self.root_node = None
        self.optimal_path = []
        self.top_n = 1
        self.top_solutions = []
        self.show_details = False
    def get_user_input(self):
        print("\n" + "="*60)
        print("      BRANCH AND BOUND - INTEGER PROGRAMMING SOLVER")
        print("             (With Tree Visualization)")
        print("="*60)
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
                print("Invalid input.")
        while True:
            try:
                self.num_variables = int(input("\nEnter the number of decision variables: "))
                if self.num_variables > 0:
                    break
            except ValueError:
                print("Invalid input.")
        while True:
            try:
                self.num_constraints = int(input("Enter the number of constraints: "))
                if self.num_constraints > 0:
                    break
            except ValueError:
                print("Invalid input.")
        print(f"\n--- OBJECTIVE FUNCTION ---")
        print(f"Enter coefficients for Z = c1*x1 + c2*x2 + ... + c{self.num_variables}*x{self.num_variables}")
        for i in range(self.num_variables):
            while True:
                try:
                    coef = float(input(f"  Coefficient of x{i+1}: "))
                    self.objective.append(coef)
                    break
                except ValueError:
                    print("  Invalid input.")
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
                        print("  Invalid input.")
            self.constraints.append(constraint)
            while True:
                try:
                    ctype = int(input("  Constraint type (1=<=, 2=>=, 3==, 4=<, 5=>): "))
                    if ctype in [1, 2, 3, 4, 5]:
                        if ctype == 4:
                            print("  Note: '<' constraint will be treated as '<=' with small adjustment")
                            self.constraint_types.append(1)
                        elif ctype == 5:
                            print("  Note: '>' constraint will be treated as '>=' with small adjustment")
                            self.constraint_types.append(2)
                        else:
                            self.constraint_types.append(ctype)
                        break
                    print("  Please enter 1, 2, 3, 4, or 5")
                except ValueError:
                    print("  Invalid input.")
            while True:
                try:
                    rhs = float(input("  Right-hand side (RHS) value: "))
                    self.rhs.append(rhs)
                    break
                except ValueError:
                    print("  Invalid input.")
        print(f"\n--- INTEGER VARIABLES ---")
        print("Which variables must be integers?")
        print("1. All variables must be integers")
        print("2. Select specific variables")
        while True:
            try:
                choice = int(input("Enter choice (1 or 2): "))
                if choice == 1:
                    self.integer_vars = list(range(self.num_variables))
                    break
                elif choice == 2:
                    var_input = input(f"Enter variable numbers (1 to {self.num_variables}) separated by commas: ")
                    self.integer_vars = [int(x.strip()) - 1 for x in var_input.split(",")]
                    break
            except ValueError:
                print("Invalid input.")
        print(f"\n--- TOP SOLUTIONS ---")
        while True:
            try:
                self.top_n = int(input("How many top solutions to display? (default=1): ") or "1")
                if self.top_n > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Invalid input.")
        self.display_problem()
    def display_problem(self):
        print("\n" + "="*60)
        print("            FORMULATED ILP PROBLEM")
        print("="*60)
        obj_type = "Maximize" if self.is_maximization else "Minimize"
        terms = []
        for i, c in enumerate(self.objective):
            if c >= 0 and i > 0:
                terms.append(f"+ {c}x{i+1}")
            elif c < 0:
                terms.append(f"- {abs(c)}x{i+1}")
            else:
                terms.append(f"{c}x{i+1}")
        print(f"{obj_type} Z = " + " ".join(terms))
        print("\nSubject to:")
        type_symbols = {1: "<=", 2: ">=", 3: "=", 4: "<", 5: ">"}
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
        int_vars = ", ".join([f"x{i+1}" for i in self.integer_vars])
        print(f"\n  Integer constraint: {int_vars} must be integers")
        print("  x1, x2, ... >= 0")
    def is_integer_solution(self, solution):
        if solution is None:
            return False
        for i in self.integer_vars:
            val = solution[f"x{i+1}"]
            if abs(val - round(val)) > 1e-6:
                return False
        return True
    def find_branching_variable(self, solution):
        for i in self.integer_vars:
            val = solution[f"x{i+1}"]
            if abs(val - round(val)) > 1e-6:
                return i, val
        return None, None
    def solve_subproblem(self, extra_constraints, verbose=False):
        sorted_extra = sorted(extra_constraints, key=lambda c: c[2])
        all_constraints = [row[:] for row in self.constraints] + [c[0] for c in sorted_extra]
        all_rhs = self.rhs[:] + [c[1] for c in sorted_extra]
        all_types = self.constraint_types[:] + [c[2] for c in sorted_extra]
        solver = SimplexSolver(
            self.objective,
            all_constraints,
            all_rhs,
            all_types,
            self.is_maximization,
            verbose=verbose
        )
        return solver.solve()
    
    def display_constraint_set(self, extra_constraints, node_id=None):
        """Display the current constraint set and feasibility ranges"""
        print(f"\n  {'='*60}")
        if node_id is not None:
            print(f"  CONSTRAINT SET FOR NODE {node_id}")
        else:
            print(f"  CONSTRAINT SET")
        print(f"  {'='*60}")
        
        type_symbols = {1: "<=", 2: ">=", 3: "="}
        
        # Display original constraints
        print("\n  Original Constraints:")
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
            print(f"    [C{i+1}] " + " ".join(terms) + f" {symbol} {self.rhs[i]}")
        
        # Display branch constraints
        if extra_constraints:
            print("\n  Branch Constraints:")
            for idx, (coef, rhs, ctype) in enumerate(extra_constraints):
                terms = []
                for j, c in enumerate(coef):
                    if c != 0:
                        if c >= 0 and terms:
                            terms.append(f"+ {c}x{j+1}")
                        elif c < 0:
                            terms.append(f"- {abs(c)}x{j+1}")
                        else:
                            terms.append(f"{c}x{j+1}")
                symbol = type_symbols.get(ctype, "<=")
                new_marker = " (NEW)" if idx == len(extra_constraints) - 1 else ""
                print(f"    [B{idx+1}] " + " ".join(terms) + f" {symbol} {rhs}{new_marker}")
        
        # Calculate and display feasibility ranges
        print("\n  Feasibility Ranges (from constraints):")
        for var_idx in range(self.num_variables):
            lower_bound = 0  # Non-negativity
            upper_bound = float('inf')
            
            # Check original constraints
            for i in range(self.num_constraints):
                coef = self.constraints[i][var_idx]
                if coef != 0:
                    if self.constraint_types[i] == 1:  # <=
                        if coef > 0:
                            max_val = self.rhs[i] / coef
                            upper_bound = min(upper_bound, max_val)
                    elif self.constraint_types[i] == 2:  # >=
                        if coef > 0:
                            min_val = self.rhs[i] / coef
                            lower_bound = max(lower_bound, min_val)
            
            # Check branch constraints
            for coef_list, rhs, ctype in extra_constraints:
                coef = coef_list[var_idx]
                if coef != 0:
                    if ctype == 1:  # <=
                        if coef > 0:
                            max_val = rhs / coef
                            upper_bound = min(upper_bound, max_val)
                    elif ctype == 2:  # >=
                        if coef > 0:
                            min_val = rhs / coef
                            lower_bound = max(lower_bound, min_val)
            
            ub_str = f"{upper_bound:.2f}" if upper_bound != float('inf') else "+∞"
            print(f"    x{var_idx+1}: [{lower_bound:.2f}, {ub_str}]")
        
        print(f"  {'='*60}")
    
    def ask_solution_method(self, extra_constraints):
        """Ask user which method to use for solving the subproblem"""
        # Check if Big M is required
        all_types = self.constraint_types[:] + [c[2] for c in extra_constraints]
        has_ge_or_eq = any(t in [2, 3] for t in all_types)
        
        if has_ge_or_eq:
            print("\n  This subproblem has >= or = constraints.")
            print("  Big M Method is REQUIRED for this subproblem.")
            return True, True  # (use_big_m, show_tableau)
        
        print("\n  Choose solution method for this subproblem:")
        print("    1. Simplex Method (standard, for <= constraints)")
        print("    2. Big M Method (for >= or = constraints)")
        print("    3. Skip detailed steps (solve quietly)")
        
        while True:
            try:
                choice = input("  Enter choice (1, 2, or 3): ").strip()
                if choice == "1":
                    return False, True  # Simplex with tableau
                elif choice == "2":
                    return True, True   # Big M with tableau
                elif choice == "3":
                    return False, False  # Quick solve without tableau
                print("  Please enter 1, 2, or 3")
            except:
                print("  Invalid input.")
    
    def solve_subproblem_interactive(self, extra_constraints, node_id=None, show_details=True):
        """Solve subproblem with interactive method selection and constraint display"""
        if show_details:
            # Display constraint set
            self.display_constraint_set(extra_constraints, node_id)
            
            # Ask user which method to use
            use_big_m, show_tableau = self.ask_solution_method(extra_constraints)
            
            if show_tableau:
                # Solve with verbose output
                return self.solve_subproblem(extra_constraints, verbose=True)
            else:
                return self.solve_subproblem(extra_constraints, verbose=False)
        else:
            return self.solve_subproblem(extra_constraints, verbose=False)
    def draw_tree(self):
        if not self.tree_nodes:
            return
        print("\n" + "="*75)
        print("                       BRANCH AND BOUND TREE")
        print("="*75)
        print("\n+-------------------------------------------------------------------------+")
        print("|  LEGEND:                                                                |")
        print("|    [*] = OPTIMAL (Best Integer Solution)                                |")
        print("|    [I] = Integer Solution Found                                         |")
        print("|    [P] = Pruned (Bound worse than best)                                 |")
        print("|    [X] = Infeasible                                                     |")
        print("|    [B] = Branched (has children)                                        |")
        print("+-------------------------------------------------------------------------+")
        print()
        self._draw_tree_boxed()
        if self.optimal_path and self.best_solution:
            print("\n" + "-"*75)
            print("  SOLUTION PATH:")
            print("-"*75)
            path_str = " -> ".join([f"Node {nid}" for nid in self.optimal_path])
            print(f"  {path_str}")
            sol_vals = [f"x{i+1}={int(round(self.best_solution[f'x{i+1}']))}" for i in range(self.num_variables)]
            print(f"\n  Optimal: {', '.join(sol_vals)}")
            print(f"  Z* = {self.best_obj_value:.4f}")
    def _draw_tree_boxed(self):
        max_depth = max(node.depth for node in self.tree_nodes.values())
        for depth in range(max_depth + 1):
            nodes_at_depth = [(nid, node) for nid, node in self.tree_nodes.items() if node.depth == depth]
            nodes_at_depth.sort(key=lambda x: x[0])
            if depth == 0:
                print("  LEVEL 0 (Root):")
            else:
                print(f"\n  LEVEL {depth}:")
            for node_id, node in nodes_at_depth:
                self._draw_single_node_box(node_id, node)
    def _draw_single_node_box(self, node_id, node):
        if node.is_optimal:
            status_symbol = "[*]"
            status_text = "OPTIMAL"
        elif node.status == "INTEGER":
            status_symbol = "[I]"
            status_text = "INTEGER"
        elif node.status == "PRUNED":
            status_symbol = "[P]"
            status_text = "PRUNED"
        elif node.status == "INFEASIBLE":
            status_symbol = "[X]"
            status_text = "INFEASIBLE"
        elif node.status == "BRANCHED":
            status_symbol = "[B]"
            status_text = "BRANCHED"
        else:
            status_symbol = "[ ]"
            status_text = "PENDING"
        if node.depth == 0:
            constraint_info = "LP Relaxation (Root)"
            parent_info = ""
        else:
            constraint_info = node.branch_constraint
            parent_info = f" (from Node {node.parent_id})"
        if node.solution:
            sol_parts = [f"x{i+1}={node.solution[f'x{i+1}']:.4f}" for i in range(self.num_variables)]
            sol_str = ", ".join(sol_parts)
            z_str = f"Z = {node.obj_value:.4f}"
        else:
            sol_str = "No solution"
            z_str = ""
        print(f"  +{'-'*68}+")
        print(f"  | {status_symbol} Node {node_id}: {constraint_info}{parent_info}".ljust(69) + "|")
        print(f"  |   Solution: {sol_str}".ljust(69) + "|")
        if z_str:
            print(f"  |   {z_str}".ljust(69) + "|")
        print(f"  |   Status: {status_text}".ljust(69) + "|")
        print(f"  +{'-'*68}+")
    def _draw_node_recursive(self, node_id, prefix, is_last):
        if node_id not in self.tree_nodes:
            return
        node = self.tree_nodes[node_id]
        if node.is_optimal:
            marker = "[*]"
        elif node.status == "INTEGER":
            marker = "[I]"
        elif node.status == "PRUNED":
            marker = "[P]"
        elif node.status == "INFEASIBLE":
            marker = "[X]"
        elif node.status == "BRANCHED":
            marker = "[B]"
        else:
            marker = "[ ]"
        if node.depth == 0:
            connector = ""
            new_prefix = ""
        else:
            connector = "`-- " if is_last else "|-- "
            new_prefix = prefix + ("    " if is_last else "|   ")
        if node.depth == 0:
            info = f"ROOT NODE (LP Relaxation)"
        else:
            info = f"{node.branch_constraint}"
        if node.solution:
            sol_str = ", ".join([f"x{i+1}={node.solution[f'x{i+1}']:.2f}" for i in range(self.num_variables)])
            z_str = f"Z={node.obj_value:.2f}"
            print(f"{prefix}{connector}{marker} Node {node_id}: {info}")
            print(f"{new_prefix}     Solution: {sol_str}, {z_str}")
            print(f"{new_prefix}     Status: {node.status}")
        else:
            print(f"{prefix}{connector}{marker} Node {node_id}: {info}")
            print(f"{new_prefix}     Status: {node.status}")
        print(f"{new_prefix}")
        children = []
        if node.left_child is not None:
            children.append(node.left_child)
        if node.right_child is not None:
            children.append(node.right_child)
        for i, child_id in enumerate(children):
            is_last_child = (i == len(children) - 1)
            self._draw_node_recursive(child_id, new_prefix, is_last_child)
    def solve(self):
        print("\n" + "="*60)
        print("         SOLVING USING BRANCH AND BOUND")
        print("="*60)
        
        # Ask user if they want detailed steps
        print("\n  Show detailed steps at each iteration?")
        print("    1. Yes - Show constraint sets, feasibility ranges, and tableaux")
        print("    2. No - Quick solve without detailed output")
        
        while True:
            try:
                detail_choice = input("  Enter choice (1 or 2): ").strip()
                if detail_choice in ["1", "2"]:
                    self.show_details = (detail_choice == "1")
                    break
                print("  Please enter 1 or 2")
            except:
                print("  Invalid input.")
        
        print("\n" + "-"*50)
        print("STEP 1: Solve LP Relaxation (Root Node)")
        print("-"*50)
        
        if self.show_details:
            self.display_constraint_set([], node_id=0)
            print("\n  This is the LP Relaxation (no integer constraints).")
            print("  Solving with standard Simplex Method...")
            root_solution, root_obj = self.solve_subproblem([], verbose=True)
        else:
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
            self.draw_tree()
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
            self.draw_tree()
            self.display_final_solution()
            return
        root.status = "BRANCHED"
        queue = [([], root_obj, 0, "", 0)]
        if self.is_maximization:
            self.best_obj_value = float('-inf')
        else:
            self.best_obj_value = float('inf')
        print("\n" + "-"*50)
        print("STEP 2: Branch and Bound Iterations")
        print("-"*50)
        node_counter = 0
        while queue:
            self.iteration += 1
            if self.is_maximization:
                queue.sort(key=lambda x: x[1], reverse=True)
            else:
                queue.sort(key=lambda x: x[1])
            current_constraints, bound, parent_id, branch_info, depth = queue.pop(0)
            if depth == 0 and self.iteration > 1:
                continue
            print(f"\n{'*'*60}")
            print(f"ITERATION {self.iteration}")
            print(f"{'*'*60}")
            
            if depth > 0:
                node_counter += 1
                current_node_id = node_counter
                print(f"Node {current_node_id}: {branch_info}")
            else:
                current_node_id = 0
            
            # Solve with interactive method if details enabled
            if self.show_details:
                solution, obj_value = self.solve_subproblem_interactive(
                    current_constraints, 
                    node_id=current_node_id,
                    show_details=True
                )
            else:
                solution, obj_value = self.solve_subproblem(current_constraints)
            
            # Create tree node
            if depth > 0:
                node = TreeNode(current_node_id, parent_id, branch_info, depth)
                node.solution = solution
                node.obj_value = obj_value
                self.tree_nodes[current_node_id] = node
                parent_node = self.tree_nodes[parent_id]
                if parent_node.left_child is None:
                    parent_node.left_child = current_node_id
                else:
                    parent_node.right_child = current_node_id
            else:
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
            worst_in_top = self.top_solutions[-1][0] if len(self.top_solutions) >= self.top_n else None
            if self.is_maximization:
                if worst_in_top is not None and obj_value < worst_in_top:
                    print(f"  Result: PRUNED (bound {obj_value:.4f} < worst in top {worst_in_top:.4f})")
                    node.status = "PRUNED"
                    continue
            else:
                if worst_in_top is not None and obj_value > worst_in_top:
                    print(f"  Result: PRUNED (bound {obj_value:.4f} > worst in top {worst_in_top:.4f})")
                    node.status = "PRUNED"
                    continue
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
                print(f"  >>> Solution #{len([s for s in self.top_solutions if s[0] == obj_value])} with Z = {obj_value:.4f}")
                continue
            var_idx, frac_val = self.find_branching_variable(solution)
            floor_val = math.floor(frac_val)
            ceil_val = math.ceil(frac_val)
            node.status = "BRANCHED"
            print(f"\n  Branching on x{var_idx+1} = {frac_val:.4f}")
            print(f"    Left branch:  x{var_idx+1} <= {floor_val}")
            print(f"    Right branch: x{var_idx+1} >= {ceil_val}")
            coef = [0.0] * self.num_variables
            coef[var_idx] = 1.0
            left_constraints = current_constraints + [(coef[:], floor_val, 1)]
            left_info = f"x{var_idx+1} <= {floor_val}"
            queue.append((left_constraints, obj_value, current_node_id, left_info, depth + 1))
            right_constraints = current_constraints + [(coef[:], ceil_val, 2)]
            right_info = f"x{var_idx+1} >= {ceil_val}"
            queue.append((right_constraints, obj_value, current_node_id, right_info, depth + 1))
        self.draw_tree()
        self.display_final_solution()
    def display_final_solution(self):
        print("\n" + "="*60)
        if self.top_n > 1:
            print(f"           TOP {len(self.top_solutions)} INTEGER SOLUTIONS")
        else:
            print("              OPTIMAL INTEGER SOLUTION")
        print("="*60)
        if not self.top_solutions:
            print("\nNo feasible integer solution found!")
            return
        print(f"\nNodes Explored: {len(self.tree_nodes)}")
        print(f"Iterations: {self.iteration}")
        print(f"Solutions Found: {len(self.top_solutions)}")
        for rank, (obj_val, solution, path) in enumerate(self.top_solutions, 1):
            print("\n" + "-"*60)
            print(f"  SOLUTION #{rank}")
            print("-"*60)
            print("\n  Decision Variables:")
            for i in range(self.num_variables):
                val = solution[f"x{i+1}"]
                if i in self.integer_vars:
                    print(f"    x{i+1} = {int(round(val))} (integer)")
                else:
                    print(f"    x{i+1} = {val:.4f}")
            calc_z = sum(self.objective[i] * solution[f"x{i+1}"] for i in range(self.num_variables))
            print(f"\n  Objective Value Z = {calc_z:.4f}")
            path_str = " -> ".join([f"Node {nid}" for nid in path])
            print(f"  Solution Path: {path_str}")
            print("\n  Constraint Check:")
            type_symbols = {1: "<=", 2: ">=", 3: "="}
            
            for i in range(self.num_constraints):
                lhs = sum(self.constraints[i][j] * solution[f"x{j+1}"] for j in range(self.num_variables))
                symbol = type_symbols[self.constraint_types[i]]
                print(f"    Constraint {i+1}: {lhs:.4f} {symbol} {self.rhs[i]} [OK]")
        if self.top_n > 1 and len(self.top_solutions) > 1:
            print("\n" + "="*60)
            print("                  SOLUTIONS SUMMARY")
            print("="*60)
            print(f"\n  {'Rank':<6} {'Z Value':<15} {'Solution':<30}")
            print("  " + "-"*55)
            for rank, (obj_val, solution, _) in enumerate(self.top_solutions, 1):
                sol_str = ", ".join([f"x{i+1}={int(round(solution[f'x{i+1}']))}" for i in self.integer_vars])
                print(f"  {rank:<6} {obj_val:<15.4f} {sol_str:<30}")

class BinaryProgramming:
    def __init__(self):
        self.num_items = 0
        self.item_names = []
        self.item_values = []
        self.item_weights = []
        self.capacity = 0
        self.is_maximization = True
        self.extra_constraints = []
        self.extra_rhs = []
        self.extra_types = []
        self.best_solution = None
        self.best_value = None
        self.nodes_explored = 0
        self.tree_nodes = {}
        self.optimal_path = []
        self.top_n = 1
        self.top_solutions = []
    def get_user_input(self):
        print("\n" + "="*60)
        print("        BINARY PROGRAMMING (0-1 KNAPSACK) SOLVER")
        print("          Branch and Bound with Selection Output")
        print("="*60)
        print("\nSelect Problem Type:")
        print("1. Knapsack Problem (Maximize value with weight constraint)")
        print("2. Custom Binary Programming (Define your own constraints)")
        while True:
            try:
                problem_type = int(input("\nEnter choice (1 or 2): "))
                if problem_type in [1, 2]:
                    break
                print("Please enter 1 or 2")
            except ValueError:
                print("Invalid input.")
        if problem_type == 1:
            self._get_knapsack_input()
        else:
            self._get_custom_binary_input()
        self.display_problem()
    def _get_knapsack_input(self):
        self.is_maximization = True
        while True:
            try:
                self.num_items = int(input("\nEnter the number of items: "))
                if self.num_items > 0:
                    break
            except ValueError:
                print("Invalid input.")
        print("\n--- ITEM DETAILS ---")
        for i in range(self.num_items):
            print(f"\nItem {i+1}:")
            name = input(f"  Name (or press Enter for 'Item {i+1}'): ").strip()
            if not name:
                name = f"Item {i+1}"
            self.item_names.append(name)
            while True:
                try:
                    value = float(input(f"  Value/Profit: "))
                    self.item_values.append(value)
                    break
                except ValueError:
                    print("  Invalid input.")
            while True:
                try:
                    weight = float(input(f"  Weight/Cost: "))
                    self.item_weights.append(weight)
                    break
                except ValueError:
                    print("  Invalid input.")
        print("\n--- CONSTRAINT ---")
        while True:
            try:
                self.capacity = float(input("Enter the maximum capacity (weight limit): "))
                if self.capacity > 0:
                    break
            except ValueError:
                print("Invalid input.")
        print(f"\n--- TOP SOLUTIONS ---")
        while True:
            try:
                self.top_n = int(input("How many top solutions to display? (default=1): ") or "1")
                if self.top_n > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Invalid input.")
    def _get_custom_binary_input(self):
        print("\nSelect Optimization Type:")
        print("1. Maximization")
        print("2. Minimization")
        while True:
            try:
                choice = int(input("Enter choice (1 or 2): "))
                if choice in [1, 2]:
                    self.is_maximization = (choice == 1)
                    break
            except ValueError:
                print("Invalid input.")
        while True:
            try:
                self.num_items = int(input("\nEnter the number of binary (0-1) variables: "))
                if self.num_items > 0:
                    break
            except ValueError:
                print("Invalid input.")
        print("\n--- BINARY VARIABLES ---")
        for i in range(self.num_items):
            print(f"\nVariable {i+1}:")
            name = input(f"  Name (or press Enter for 'x{i+1}'): ").strip()
            if not name:
                name = f"x{i+1}"
            self.item_names.append(name)
            while True:
                try:
                    value = float(input(f"  Objective coefficient (value/cost): "))
                    self.item_values.append(value)
                    break
                except ValueError:
                    print("  Invalid input.")
            self.item_weights.append(1.0)
        while True:
            try:
                num_constraints = int(input("\nEnter the number of constraints: "))
                if num_constraints >= 0:
                    break
            except ValueError:
                print("Invalid input.")
        if num_constraints == 0:
            self.capacity = float('inf')
        else:
            print("\n--- CONSTRAINTS ---")
            print("Constraint types: 1 = <=, 2 = >=, 3 = =")
            for i in range(num_constraints):
                print(f"\nConstraint {i+1}:")
                constraint = []
                for j in range(self.num_items):
                    while True:
                        try:
                            coef = float(input(f"  Coefficient of {self.item_names[j]}: "))
                            constraint.append(coef)
                            break
                        except ValueError:
                            print("  Invalid input.")
                self.extra_constraints.append(constraint)
                while True:
                    try:
                        ctype = int(input("  Constraint type (1=<=, 2=>=, 3==): "))
                        if ctype in [1, 2, 3]:
                            self.extra_types.append(ctype)
                            break
                    except ValueError:
                        print("  Invalid input.")
                while True:
                    try:
                        rhs = float(input("  Right-hand side (RHS) value: "))
                        self.extra_rhs.append(rhs)
                        break
                    except ValueError:
                        print("  Invalid input.")
                if i == 0 and self.extra_types[0] == 1:
                    self.item_weights = constraint[:]
                    self.capacity = rhs
    def display_problem(self):
        print("\n" + "="*60)
        print("          FORMULATED BINARY PROGRAMMING PROBLEM")
        print("="*60)
        obj_type = "Maximize" if self.is_maximization else "Minimize"
        terms = []
        for i in range(self.num_items):
            v = self.item_values[i]
            if v >= 0 and i > 0:
                terms.append(f"+ {v}*{self.item_names[i]}")
            elif v < 0:
                terms.append(f"- {abs(v)}*{self.item_names[i]}")
            else:
                terms.append(f"{v}*{self.item_names[i]}")
        print(f"\n{obj_type} Z = {' '.join(terms)}")
        print("\nSubject to:")
        if self.capacity != float('inf'):
            terms = []
            for i in range(self.num_items):
                w = self.item_weights[i]
                if w >= 0 and i > 0:
                    terms.append(f"+ {w}*{self.item_names[i]}")
                elif w < 0:
                    terms.append(f"- {abs(w)}*{self.item_names[i]}")
                else:
                    terms.append(f"{w}*{self.item_names[i]}")
            print(f"  {' '.join(terms)} <= {self.capacity}")
        type_symbols = {1: "<=", 2: ">=", 3: "="}
        for idx, constraint in enumerate(self.extra_constraints):
            if idx == 0 and self.capacity != float('inf'):
                continue
            terms = []
            for i in range(self.num_items):
                c = constraint[i]
                if c >= 0 and i > 0:
                    terms.append(f"+ {c}*{self.item_names[i]}")
                elif c < 0:
                    terms.append(f"- {abs(c)}*{self.item_names[i]}")
                else:
                    terms.append(f"{c}*{self.item_names[i]}")
            print(f"  {' '.join(terms)} {type_symbols[self.extra_types[idx]]} {self.extra_rhs[idx]}")
        print(f"\n  Binary constraint: All variables ∈ {{0, 1}}")
        print("\n" + "-"*50)
        print("ITEM SUMMARY:")
        print("-"*50)
        print(f"{'Item':<20} {'Value/Profit':<15} {'Weight/Cost':<15}")
        print("-"*50)
        for i in range(self.num_items):
            print(f"{self.item_names[i]:<20} {self.item_values[i]:<15.2f} {self.item_weights[i]:<15.2f}")
        print("-"*50)
        if self.capacity != float('inf'):
            print(f"Capacity: {self.capacity}")
    def solve(self):
        print("\n" + "="*60)
        print("       SOLVING USING BRANCH AND BOUND (BINARY)")
        print("="*60)
        if self.is_maximization:
            self.best_value = float('-inf')
        else:
            self.best_value = float('inf')
        self.best_solution = None
        self.nodes_explored = 0
        print("\n" + "-"*50)
        print("BRANCH AND BOUND EXPLORATION")
        print("-"*50)
        initial_selection = [-1] * self.num_items
        self._branch_and_bound(initial_selection, 0, 0, 0)
        self.display_solution()
    def _calculate_upper_bound(self, selection, level, current_value, current_weight):
        if self.capacity == float('inf'):
            bound = current_value
            for i in range(level, self.num_items):
                if selection[i] == -1:
                    if self.is_maximization and self.item_values[i] > 0:
                        bound += self.item_values[i]
                    elif not self.is_maximization and self.item_values[i] < 0:
                        bound += self.item_values[i]
            return bound
        remaining_capacity = self.capacity - current_weight
        bound = current_value
        remaining = []
        for i in range(level, self.num_items):
            if selection[i] == -1 and self.item_weights[i] > 0:
                ratio = self.item_values[i] / self.item_weights[i]
                remaining.append((i, ratio, self.item_values[i], self.item_weights[i]))
        remaining.sort(key=lambda x: x[1], reverse=self.is_maximization)
        for i, ratio, value, weight in remaining:
            if weight <= remaining_capacity:
                bound += value
                remaining_capacity -= weight
            else:
                bound += ratio * remaining_capacity
                break
        return bound
    def _is_feasible(self, selection):
        current_weight = sum(self.item_weights[i] for i in range(self.num_items) if selection[i] == 1)
        if current_weight > self.capacity:
            return False
        for idx, constraint in enumerate(self.extra_constraints):
            if idx == 0 and self.capacity != float('inf'):
                continue
            lhs = sum(constraint[i] for i in range(self.num_items) if selection[i] == 1)
            rhs = self.extra_rhs[idx]
            ctype = self.extra_types[idx]
            if ctype == 1 and lhs > rhs:
                return False
            elif ctype == 2 and lhs < rhs:
                return False
            elif ctype == 3 and abs(lhs - rhs) > 1e-6:
                return False
        return True
    def _branch_and_bound(self, selection, level, current_value, current_weight):
        self.nodes_explored += 1
        if current_weight > self.capacity:
            return
        if level == self.num_items:
            if self._is_feasible(selection):
                solution_copy = selection[:]
                self.top_solutions.append((current_value, solution_copy))
                if self.is_maximization:
                    self.top_solutions.sort(key=lambda x: x[0], reverse=True)
                else:
                    self.top_solutions.sort(key=lambda x: x[0])
                if len(self.top_solutions) > self.top_n:
                    self.top_solutions = self.top_solutions[:self.top_n]
                if self.top_solutions:
                    self.best_value = self.top_solutions[0][0]
                    self.best_solution = self.top_solutions[0][1]
                print(f"\n  >>> Solution #{len(self.top_solutions)} found!")
                print(f"      Selection: {self._format_selection(solution_copy)}")
                print(f"      Value: {current_value:.2f}")
            return
        bound = self._calculate_upper_bound(selection, level, current_value, current_weight)
        worst_in_top = self.top_solutions[-1][0] if len(self.top_solutions) == self.top_n else (float('-inf') if self.is_maximization else float('inf'))
        if self.is_maximization:
            if bound <= worst_in_top:
                return
        else:
            if bound >= worst_in_top:
                return
        item_name = self.item_names[level]
        item_value = self.item_values[level]
        item_weight = self.item_weights[level]
        if self.is_maximization:
            if current_weight + item_weight <= self.capacity:
                selection[level] = 1
                self._branch_and_bound(selection, level + 1,
                                       current_value + item_value,
                                       current_weight + item_weight)
            selection[level] = 0
            self._branch_and_bound(selection, level + 1, current_value, current_weight)
        else:
            selection[level] = 0
            self._branch_and_bound(selection, level + 1, current_value, current_weight)
            if current_weight + item_weight <= self.capacity:
                selection[level] = 1
                self._branch_and_bound(selection, level + 1,
                                       current_value + item_value,
                                       current_weight + item_weight)
        selection[level] = -1
    def _format_selection(self, selection):
        return "[" + ", ".join(str(max(0, s)) for s in selection) + "]"
    def display_solution(self):
        print("\n" + "="*60)
        print("              OPTIMAL BINARY SOLUTION")
        print("="*60)
        if not self.top_solutions:
            print("\nNo feasible solution found!")
            return
        print(f"\nNodes Explored: {self.nodes_explored}")
        print(f"Solutions Found: {len(self.top_solutions)}")
        for rank, (obj_val, solution) in enumerate(self.top_solutions, 1):
            print("\n" + "-"*60)
            if self.top_n > 1:
                print(f"  SOLUTION #{rank}")
            else:
                print("  OPTIMAL SOLUTION")
            print("-"*60)
            print("\n  SELECTION SEQUENCE (1 = Selected, 0 = Not Selected)")
            selection_str = self._format_selection(solution)
            print(f"\n  Selection Vector: {selection_str}")
            print("\n  Detailed Selection:")
            print(f"  {'#':<5} {'Item':<20} {'Selected':<10} {'Value':<12} {'Weight':<12}")
            print("  " + "-"*59)
            total_value = 0
            total_weight = 0
            selected_items = []
            for i in range(self.num_items):
                selected = solution[i]
                selected_str = "YES (1)" if selected == 1 else "NO (0)"
                print(f"  {i+1:<5} {self.item_names[i]:<20} {selected_str:<10} {self.item_values[i]:<12.2f} {self.item_weights[i]:<12.2f}")
                if selected == 1:
                    total_value += self.item_values[i]
                    total_weight += self.item_weights[i]
                    selected_items.append(self.item_names[i])
            print("  " + "-"*59)
            print(f"  {'TOTAL':<5} {'':<20} {'':<10} {total_value:<12.2f} {total_weight:<12.2f}")
            print(f"\n  Selected Items: {', '.join(selected_items) if selected_items else 'None'}")
            print(f"  Total Value: {total_value:.2f}, Weight Used: {total_weight:.2f}")
            if self.capacity != float('inf'):
                print(f"  Remaining Capacity: {self.capacity - total_weight:.2f}")
        if self.top_n > 1 and len(self.top_solutions) > 1:
            print("\n" + "="*60)
            print("                  SOLUTIONS SUMMARY")
            print("="*60)
            print(f"\n  {'Rank':<6} {'Value':<12} {'Weight':<12} {'Selection':<30}")
            print("  " + "-"*60)
            for rank, (obj_val, solution) in enumerate(self.top_solutions, 1):
                sel_str = self._format_selection(solution)
                weight = sum(self.item_weights[i] for i in range(self.num_items) if solution[i] == 1)
                print(f"  {rank:<6} {obj_val:<12.2f} {weight:<12.2f} {sel_str:<30}")
        print("\n" + "="*60)
        print("                    FINAL ANSWER")
        print("="*60)
        selection_str = self._format_selection(self.best_solution)
        box_width = max(40, len(selection_str) + 4)
        print("\n  +" + "-"*(box_width-2) + "+")
        print(f"  | Best Selection: {selection_str}" + " "*(box_width - 18 - len(selection_str)) + "|")
        print(f"  | {'Maximum' if self.is_maximization else 'Minimum'} Value: {self.best_value:.2f}" + " "*(box_width - 20 - len(f'{self.best_value:.2f}')) + "|")
        print("  +" + "-"*(box_width-2) + "+")

def main():
    print("\n" + "="*60)
    print("|" + " "*10 + "BRANCH AND BOUND SOLVER" + " "*25 + "|")
    print("|" + " "*8 + "Integer Linear Programming" + " "*24 + "|")
    print("|" + " "*6 + "With Visual Tree Representation" + " "*19 + "|")
    print("="*60)
    while True:
        print("\nSelect Method:")
        print("1. Integer Linear Programming (ILP)")
        print("2. Binary Programming (0-1 Knapsack)")
        while True:
            try:
                method = int(input("\nEnter choice (1 or 2): "))
                if method in [1, 2]:
                    break
                print("Please enter 1 or 2")
            except ValueError:
                print("Invalid input.")
        if method == 1:
            solver = BranchAndBound()
            solver.get_user_input()
            input("\nPress Enter to start solving...")
            solver.solve()
        else:
            solver = BinaryProgramming()
            solver.get_user_input()
            input("\nPress Enter to start solving...")
            solver.solve()
        print("\n" + "-"*60)
        choice = input("\nSolve another problem? (y/n): ")
        if choice.lower() != 'y':
            print("\nThank you for using Branch and Bound Solver!")
            break

if __name__ == "__main__":
    main()