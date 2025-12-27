"""
Sensitivity Analysis for Linear Programming
Complete Implementation with Step-by-Step Visualization
Like Pen-and-Paper Analysis!
Pure Python - No external libraries required!

Features:
1. Change RHS values (constraint bounds)
2. Modify objective function coefficients
3. Add new constraints
4. Add new variables
5. Check feasibility and optimality
6. Calculate allowable ranges
"""

import copy
from fractions import Fraction


class SensitivityAnalysis:
    """Comprehensive Sensitivity Analysis for Linear Programming"""
    
    def __init__(self):
        # Original problem data
        self.num_variables = 0
        self.num_constraints = 0
        self.objective = []
        self.constraints = []
        self.rhs = []
        self.constraint_types = []  # 1: <=, 2: >=, 3: =
        self.is_maximization = True
        
        # Tableau data
        self.tableau = []
        self.var_names = []
        self.basic_vars = []
        self.M = 10000
        
        # Tracking
        self.num_slack = 0
        self.num_surplus = 0
        self.num_artificial = 0
        self.artificial_indices = []
        
        # Optimal solution storage
        self.optimal_tableau = None
        self.optimal_basic_vars = None
        self.optimal_solution = {}
        self.optimal_z = None
        
        # Basis inverse (B^-1) for sensitivity
        self.B_inverse = None
        
    def get_user_input(self):
        """Get all inputs from user"""
        print("\n" + "="*70)
        print("           SENSITIVITY ANALYSIS - LINEAR PROGRAMMING")
        print("                   Complete Step-by-Step Solution")
        print("="*70)
        
        # Problem type
        print("\nSelect Problem Type:")
        print("1. Maximization")
        print("2. Minimization")
        while True:
            try:
                choice = int(input("\nEnter choice (1 or 2): "))
                if choice in [1, 2]:
                    self.is_maximization = (choice == 1)
                    break
                print("Please enter 1 or 2")
            except ValueError:
                print("Invalid input.")
        
        # Number of variables
        while True:
            try:
                self.num_variables = int(input("\nEnter the number of decision variables: "))
                if self.num_variables > 0:
                    break
                print("Must be positive")
            except ValueError:
                print("Invalid input.")
        
        # Number of constraints
        while True:
            try:
                self.num_constraints = int(input("Enter the number of constraints: "))
                if self.num_constraints > 0:
                    break
                print("Must be positive")
            except ValueError:
                print("Invalid input.")
        
        # Objective function
        print(f"\n--- OBJECTIVE FUNCTION ---")
        obj_type = "Maximize" if self.is_maximization else "Minimize"
        print(f"{obj_type} Z = c1*x1 + c2*x2 + ... + c{self.num_variables}*x{self.num_variables}")
        print("Enter the coefficients:")
        
        for i in range(self.num_variables):
            while True:
                try:
                    coef = float(input(f"  Coefficient of x{i+1} (c{i+1}): "))
                    self.objective.append(coef)
                    break
                except ValueError:
                    print("  Invalid input.")
        
        # Constraints
        print(f"\n--- CONSTRAINTS ---")
        print("Constraint types: 1 = <=, 2 = >=, 3 = =")
        
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
                    ctype = int(input("  Constraint type (1=<=, 2=>=, 3==): "))
                    if ctype in [1, 2, 3]:
                        self.constraint_types.append(ctype)
                        break
                    print("  Please enter 1, 2, or 3")
                except ValueError:
                    print("  Invalid input.")
            
            while True:
                try:
                    rhs = float(input("  Right-hand side (RHS) value (b): "))
                    if rhs < 0:
                        print(f"  Note: Converting negative RHS by multiplying constraint by -1.")
                        constraint = [-c for c in constraint]
                        self.constraints[-1] = constraint
                        rhs = -rhs
                        if self.constraint_types[-1] == 1:
                            self.constraint_types[-1] = 2
                        elif self.constraint_types[-1] == 2:
                            self.constraint_types[-1] = 1
                    self.rhs.append(rhs)
                    break
                except ValueError:
                    print("  Invalid input.")
        
        self.display_problem()
    
    def display_problem(self):
        """Display the formulated problem"""
        print("\n" + "="*70)
        print("                    FORMULATED LP PROBLEM")
        print("="*70)
        
        obj_type = "Maximize" if self.is_maximization else "Minimize"
        
        # Objective function
        terms = []
        for i, c in enumerate(self.objective):
            if c >= 0 and i > 0:
                terms.append(f"+ {c}x{i+1}")
            elif c < 0:
                terms.append(f"- {abs(c)}x{i+1}")
            else:
                terms.append(f"{c}x{i+1}")
        print(f"\n{obj_type} Z = " + " ".join(terms))
        
        # Constraints
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
            print(f"  " + " ".join(terms) + f" {type_symbols[self.constraint_types[i]]} {self.rhs[i]}")
        
        print(f"\n  x1, x2, ..., x{self.num_variables} >= 0")
    
    def create_initial_tableau(self):
        """Create the initial simplex tableau"""
        # Count different variable types
        self.num_slack = sum(1 for t in self.constraint_types if t == 1)
        self.num_surplus = sum(1 for t in self.constraint_types if t == 2)
        self.num_artificial = sum(1 for t in self.constraint_types if t in [2, 3])
        
        # Total columns
        total_vars = self.num_variables + self.num_slack + self.num_surplus + self.num_artificial
        num_rows = self.num_constraints + 1
        num_cols = total_vars + 1
        
        # Initialize tableau
        self.tableau = [[0.0 for _ in range(num_cols)] for _ in range(num_rows)]
        self.var_names = [f"x{i+1}" for i in range(self.num_variables)]
        
        slack_idx = self.num_variables
        surplus_idx = self.num_variables + self.num_slack
        artificial_idx = self.num_variables + self.num_slack + self.num_surplus
        
        self.basic_vars = []
        self.artificial_indices = []
        
        # Fill constraint rows
        for i in range(self.num_constraints):
            for j in range(self.num_variables):
                self.tableau[i][j] = self.constraints[i][j]
            
            if self.constraint_types[i] == 1:  # <=
                self.tableau[i][slack_idx] = 1
                self.var_names.append(f"s{i+1}")
                self.basic_vars.append(slack_idx)
                slack_idx += 1
                
            elif self.constraint_types[i] == 2:  # >=
                self.tableau[i][surplus_idx] = -1
                self.var_names.append(f"e{i+1}")
                surplus_idx += 1
                
                self.tableau[i][artificial_idx] = 1
                self.var_names.append(f"a{i+1}")
                self.basic_vars.append(artificial_idx)
                self.artificial_indices.append(artificial_idx)
                artificial_idx += 1
                
            else:  # =
                self.tableau[i][artificial_idx] = 1
                self.var_names.append(f"a{i+1}")
                self.basic_vars.append(artificial_idx)
                self.artificial_indices.append(artificial_idx)
                artificial_idx += 1
            
            self.tableau[i][-1] = self.rhs[i]
        
        # Fill objective row
        for j in range(self.num_variables):
            if self.is_maximization:
                self.tableau[-1][j] = -self.objective[j]
            else:
                self.tableau[-1][j] = self.objective[j]
        
        # Big M for artificial variables
        for art_idx in self.artificial_indices:
            if self.is_maximization:
                self.tableau[-1][art_idx] = self.M
            else:
                self.tableau[-1][art_idx] = -self.M
        
        # Eliminate artificial variables from objective row
        for i, bv in enumerate(self.basic_vars):
            if bv in self.artificial_indices:
                coef = self.tableau[-1][bv]
                if abs(coef) > 1e-10:
                    for j in range(len(self.tableau[-1])):
                        self.tableau[-1][j] -= coef * self.tableau[i][j]
    
    def find_pivot_column(self):
        """Find the entering variable"""
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
        """Find the leaving variable"""
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
        pivot_element = self.tableau[pivot_row][pivot_col]
        
        # Make pivot element 1
        for j in range(len(self.tableau[pivot_row])):
            self.tableau[pivot_row][j] /= pivot_element
        
        # Make other elements in pivot column 0
        for i in range(len(self.tableau)):
            if i != pivot_row:
                factor = self.tableau[i][pivot_col]
                if abs(factor) > 1e-10:
                    for j in range(len(self.tableau[i])):
                        self.tableau[i][j] -= factor * self.tableau[pivot_row][j]
        
        self.basic_vars[pivot_row] = pivot_col
    
    def display_tableau(self, title="Current Tableau"):
        """Display the tableau"""
        num_cols = len(self.tableau[0])
        col_width = 10
        
        print(f"\n{'-'*70}")
        print(f"  {title}")
        print(f"{'-'*70}")
        
        # Header
        print(" "*12, end="")
        for j in range(num_cols - 1):
            if j < len(self.var_names):
                print(f"{self.var_names[j]:^{col_width}}", end="")
        print(f"{'RHS':^{col_width}}")
        
        print("-" * (12 + col_width * num_cols))
        
        # Rows
        for i in range(len(self.tableau) - 1):
            bv_name = self.var_names[self.basic_vars[i]] if i < len(self.basic_vars) else "?"
            print(f"{bv_name:^10} |", end="")
            
            for j in range(num_cols):
                val = self.tableau[i][j]
                if abs(val) < 1e-10:
                    val = 0
                if abs(val - round(val)) < 1e-10:
                    print(f"{int(round(val)):^{col_width}}", end="")
                else:
                    print(f"{val:^{col_width}.3f}", end="")
            print()
        
        print("-" * (12 + col_width * num_cols))
        
        # Objective row
        print(f"{'Zj-Cj':^10} |", end="")
        for j in range(num_cols):
            val = self.tableau[-1][j]
            if abs(val) < 1e-10:
                val = 0
            if abs(val - round(val)) < 1e-10:
                print(f"{int(round(val)):^{col_width}}", end="")
            else:
                print(f"{val:^{col_width}.3f}", end="")
        print()
    
    def solve_initial_problem(self):
        """Solve the initial LP to get optimal tableau"""
        print("\n" + "="*70)
        print("               STEP 1: SOLVE INITIAL LP PROBLEM")
        print("="*70)
        
        self.create_initial_tableau()
        
        print("\n>>> Creating initial simplex tableau...")
        self.display_tableau("Initial Tableau")
        
        max_iterations = 100
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            pivot_col = self.find_pivot_column()
            if pivot_col == -1:
                break
            
            pivot_row = self.find_pivot_row(pivot_col)
            if pivot_row == -1:
                print("\n>>> PROBLEM IS UNBOUNDED!")
                return False
            
            self.perform_pivot(pivot_row, pivot_col)
        
        # Check for infeasibility
        for i, bv in enumerate(self.basic_vars):
            if bv in self.artificial_indices:
                if self.tableau[i][-1] > 1e-6:
                    print("\n>>> PROBLEM IS INFEASIBLE!")
                    return False
        
        print(f"\n>>> Optimal solution found in {iteration} iterations!")
        
        # Store optimal data
        self.optimal_tableau = [row[:] for row in self.tableau]
        self.optimal_basic_vars = self.basic_vars[:]
        
        # Extract solution
        self.optimal_solution = {}
        for i in range(self.num_variables):
            self.optimal_solution[f"x{i+1}"] = 0.0
        
        for i, bv in enumerate(self.basic_vars):
            if bv < self.num_variables:
                self.optimal_solution[f"x{bv+1}"] = self.tableau[i][-1]
        
        self.optimal_z = sum(self.objective[i] * self.optimal_solution[f"x{i+1}"] 
                            for i in range(self.num_variables))
        
        # Extract B inverse
        self.extract_B_inverse()
        
        self.display_optimal_solution()
        return True
    
    def extract_B_inverse(self):
        """Extract basis inverse from the optimal tableau"""
        n = self.num_constraints
        total_added = self.num_slack + self.num_surplus + self.num_artificial
        
        # B^-1 appears in the columns of slack/artificial variables
        self.B_inverse = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # For <= constraints, B^-1 is in slack columns
        # For >= or = constraints, B^-1 is in artificial columns
        col_offset = self.num_variables
        
        for i in range(n):
            for j in range(n):
                if col_offset + j < len(self.tableau[0]) - 1:
                    self.B_inverse[i][j] = self.optimal_tableau[i][col_offset + j]
    
    def display_optimal_solution(self):
        """Display  the optimal solution"""
        print("\n" + "-"*70)
        print("                    OPTIMAL SOLUTION")
        print("-"*70)
        
        self.display_tableau("Optimal Tableau")
        
        print("\n  Decision Variables:")
        for i in range(self.num_variables):
            val = self.optimal_solution[f"x{i+1}"]
            if abs(val - round(val)) < 1e-6:
                print(f"    x{i+1} = {int(round(val))}")
            else:
                print(f"    x{i+1} = {val:.4f}")
        
        opt_type = "Maximum" if self.is_maximization else "Minimum"
        print(f"\n  {opt_type} Z = {self.optimal_z:.4f}")
        
        # Show basic variables
        print("\n  Basic Variables in Optimal Solution:")
        for i, bv in enumerate(self.optimal_basic_vars):
            print(f"    {self.var_names[bv]} = {self.optimal_tableau[i][-1]:.4f}")
    
    def sensitivity_menu(self):
        """Display sensitivity analysis menu"""
        while True:
            print("\n" + "="*70)
            print("              SENSITIVITY ANALYSIS MENU")
            print("="*70)
            print("\nChoose an analysis to perform:")
            print("-"*50)
            print("  1. Change RHS value (constraint bound)")
            print("  2. Modify objective function coefficient")
            print("  3. Add a new constraint")
            print("  4. Add a new variable")
            print("  5. Calculate allowable ranges")
            print("  6. Re-display optimal solution")
            print("  7. Solve new problem")
            print("  0. Exit")
            print("-"*50)
            
            try:
                choice = int(input("\nEnter your choice: "))
                
                if choice == 0:
                    print("\nThank you for using Sensitivity Analysis!")
                    break
                elif choice == 1:
                    self.analyze_rhs_change()
                elif choice == 2:
                    self.analyze_objective_change()
                elif choice == 3:
                    self.analyze_new_constraint()
                elif choice == 4:
                    self.analyze_new_variable()
                elif choice == 5:
                    self.calculate_allowable_ranges()
                elif choice == 6:
                    self.display_optimal_solution()
                elif choice == 7:
                    return True  # Signal to restart
                else:
                    print("Invalid choice. Please try again.")
                    
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        return False
    
    def analyze_rhs_change(self):
        """Analyze the effect of changing RHS values"""
        print("\n" + "="*70)
        print("        SENSITIVITY ANALYSIS: RHS CHANGE (Constraint Bound)")
        print("="*70)
        
        # Display current constraints
        print("\nCurrent Constraints:")
        print("-"*50)
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
            print(f"  {i+1}. " + " ".join(terms) + f" {type_symbols[self.constraint_types[i]]} {self.rhs[i]}")
        
        # Select constraint
        while True:
            try:
                con_num = int(input(f"\nWhich constraint to modify? (1-{self.num_constraints}): "))
                if 1 <= con_num <= self.num_constraints:
                    break
                print(f"Please enter a number between 1 and {self.num_constraints}")
            except ValueError:
                print("Invalid input.")
        
        con_idx = con_num - 1
        old_rhs = self.rhs[con_idx]
        
        while True:
            try:
                new_rhs = float(input(f"Enter new RHS value (current = {old_rhs}): "))
                break
            except ValueError:
                print("Invalid input.")
        
        delta_b = new_rhs - old_rhs
        
        print("\n" + "-"*70)
        print("                    ANALYSIS STEPS")
        print("-"*70)
        
        print(f"\n>>> STEP 1: Calculate change in RHS")
        print(f"    Original b{con_num} = {old_rhs}")
        print(f"    New b{con_num} = {new_rhs}")
        print(f"    Δb{con_num} = {new_rhs} - {old_rhs} = {delta_b}")
        
        print(f"\n>>> STEP 2: Identify B^(-1) (Basis Inverse)")
        print("    B^(-1) from optimal tableau:")
        self.print_matrix(self.B_inverse, "    B^(-1)")
        
        print(f"\n>>> STEP 3: Calculate new RHS values")
        print("    New RHS = B^(-1) × (Original b + Δb)")
        
        # Calculate new RHS vector
        new_b_vector = self.rhs[:]
        new_b_vector[con_idx] = new_rhs
        
        print(f"\n    Original b vector: {self.rhs}")
        print(f"    New b vector: {new_b_vector}")
        
        # Calculate B^-1 * new_b
        new_tableau_rhs = []
        for i in range(self.num_constraints):
            val = 0
            for j in range(self.num_constraints):
                val += self.B_inverse[i][j] * new_b_vector[j]
            new_tableau_rhs.append(val)
        
        print(f"\n    New RHS in optimal tableau: B^(-1) × new_b =")
        for i, val in enumerate(new_tableau_rhs):
            print(f"      Row {i+1}: {val:.4f}")
        
        print(f"\n>>> STEP 4: Check Feasibility")
        is_feasible = True
        for i, val in enumerate(new_tableau_rhs):
            status = "OK (≥ 0)" if val >= -1e-10 else "VIOLATED (< 0)"
            print(f"    Row {i+1}: {val:.4f} {status}")
            if val < -1e-10:
                is_feasible = False
        
        print(f"\n>>> STEP 5: Calculate New Optimal Z")
        
        if is_feasible:
            print("\n    ✓ FEASIBILITY: Solution remains FEASIBLE!")
            
            # Calculate new Z using shadow prices
            # Shadow price is the coefficient in objective row for slack/surplus
            shadow_prices = []
            col_offset = self.num_variables
            for i in range(self.num_constraints):
                if col_offset + i < len(self.optimal_tableau[-1]) - 1:
                    sp = self.optimal_tableau[-1][col_offset + i]
                    if self.is_maximization:
                        sp = -sp
                    shadow_prices.append(sp)
                else:
                    shadow_prices.append(0)
            
            print(f"\n    Shadow Prices (Dual Values):")
            for i, sp in enumerate(shadow_prices):
                print(f"      y{i+1} = {sp:.4f}")
            
            new_z = self.optimal_z + delta_b * shadow_prices[con_idx]
            
            print(f"\n    Change in Z = Δb × y{con_num}")
            print(f"                = {delta_b} × {shadow_prices[con_idx]:.4f}")
            print(f"                = {delta_b * shadow_prices[con_idx]:.4f}")
            
            print(f"\n    New Optimal Z = Old Z + ΔZ")
            print(f"                  = {self.optimal_z:.4f} + {delta_b * shadow_prices[con_idx]:.4f}")
            print(f"                  = {new_z:.4f}")
            
            # Show new solution
            print("\n    New Basic Variable Values:")
            for i in range(self.num_constraints):
                bv = self.optimal_basic_vars[i]
                print(f"      {self.var_names[bv]} = {new_tableau_rhs[i]:.4f}")
            
        else:
            print("\n    ✗ FEASIBILITY: Solution becomes INFEASIBLE!")
            print("\n    The change violates the non-negativity constraints.")
            print("    To find a new optimal solution, re-solve using Dual Simplex")
            print("    or the Primal Simplex method from the beginning.")
        
        print("\n" + "-"*70)
        print("                    SUMMARY")
        print("-"*70)
        print(f"\n  Original RHS: b{con_num} = {old_rhs}")
        print(f"  New RHS: b{con_num} = {new_rhs}")
        print(f"  Change: Δb = {delta_b}")
        print(f"\n  Original Optimal Z = {self.optimal_z:.4f}")
        if is_feasible:
            print(f"  New Optimal Z = {new_z:.4f}")
            print(f"  Change in Z = {new_z - self.optimal_z:.4f}")
        else:
            print("  New Optimal Z = Need to re-solve (infeasible)")
    
    def analyze_objective_change(self):
        """Analyze the effect of changing objective function coefficients"""
        print("\n" + "="*70)
        print("      SENSITIVITY ANALYSIS: OBJECTIVE FUNCTION COEFFICIENT")
        print("="*70)
        
        # Display current objective
        print("\nCurrent Objective Function:")
        obj_type = "Maximize" if self.is_maximization else "Minimize"
        terms = []
        for i, c in enumerate(self.objective):
            if c >= 0 and i > 0:
                terms.append(f"+ {c}x{i+1}")
            elif c < 0:
                terms.append(f"- {abs(c)}x{i+1}")
            else:
                terms.append(f"{c}x{i+1}")
        print(f"  {obj_type} Z = " + " ".join(terms))
        
        print("\nCurrent Coefficients:")
        for i, c in enumerate(self.objective):
            status = "(BASIC)" if self.optimal_solution[f"x{i+1}"] > 1e-10 else "(NON-BASIC)"
            print(f"  c{i+1} = {c} {status}")
        
        # Select variable
        while True:
            try:
                var_num = int(input(f"\nWhich variable's coefficient to modify? (1-{self.num_variables}): "))
                if 1 <= var_num <= self.num_variables:
                    break
                print(f"Please enter a number between 1 and {self.num_variables}")
            except ValueError:
                print("Invalid input.")
        
        var_idx = var_num - 1
        old_coef = self.objective[var_idx]
        
        while True:
            try:
                new_coef = float(input(f"Enter new coefficient (current c{var_num} = {old_coef}): "))
                break
            except ValueError:
                print("Invalid input.")
        
        delta_c = new_coef - old_coef
        
        print("\n" + "-"*70)
        print("                    ANALYSIS STEPS")
        print("-"*70)
        
        print(f"\n>>> STEP 1: Identify Variable Type")
        is_basic = self.optimal_solution[f"x{var_num}"] > 1e-10
        
        if is_basic:
            print(f"    x{var_num} is a BASIC variable (in the optimal basis)")
            print(f"    Current value: x{var_num} = {self.optimal_solution[f'x{var_num}']:.4f}")
        else:
            print(f"    x{var_num} is a NON-BASIC variable (not in the optimal basis)")
            print(f"    Current value: x{var_num} = 0")
        
        print(f"\n>>> STEP 2: Calculate Coefficient Change")
        print(f"    Original c{var_num} = {old_coef}")
        print(f"    New c{var_num} = {new_coef}")
        print(f"    Δc{var_num} = {new_coef} - {old_coef} = {delta_c}")
        
        if is_basic:
            print(f"\n>>> STEP 3: For BASIC Variable - Check Optimality")
            print("    Need to recalculate all (Cj - Zj) values")
            
            # Find which row contains this variable
            basic_row = -1
            for i, bv in enumerate(self.optimal_basic_vars):
                if bv == var_idx:
                    basic_row = i
                    break
            
            if basic_row >= 0:
                # Calculate new Zj-Cj for non-basic variables
                print(f"\n    x{var_num} is in row {basic_row + 1} of the optimal tableau")
                print("\n    New (Zj - Cj) for each variable:")
                
                all_optimal = True
                for j in range(len(self.optimal_tableau[0]) - 1):
                    if j < len(self.var_names):
                        # Check if this is a basic variable
                        is_basic_col = j in self.optimal_basic_vars
                        
                        if is_basic_col:
                            new_zj_cj = 0  # Always 0 for basic variables
                        else:
                            # Zj = sum(cb_i * a_ij)
                            old_zj_cj = self.optimal_tableau[-1][j]
                            # Change in Zj due to coefficient change
                            delta_zj = delta_c * self.optimal_tableau[basic_row][j]
                            if self.is_maximization:
                                new_zj_cj = old_zj_cj - delta_zj
                            else:
                                new_zj_cj = old_zj_cj + delta_zj
                        
                        status = "OK" if (self.is_maximization and new_zj_cj >= -1e-10) or \
                                        (not self.is_maximization and new_zj_cj <= 1e-10) else "VIOLATES"
                        if status == "VIOLATES":
                            all_optimal = False
                        print(f"      {self.var_names[j]}: {new_zj_cj:.4f} [{status}]")
                
                if all_optimal:
                    print("\n    ✓ OPTIMALITY: All (Zj-Cj) conditions satisfied!")
                    print("    Current basis remains optimal.")
                    
                    # Calculate new Z
                    new_z = self.optimal_z + delta_c * self.optimal_solution[f"x{var_num}"]
                    print(f"\n>>> STEP 4: Calculate New Optimal Z")
                    print(f"    New Z = Old Z + Δc × x{var_num}")
                    print(f"          = {self.optimal_z:.4f} + {delta_c} × {self.optimal_solution[f'x{var_num}']:.4f}")
                    print(f"          = {new_z:.4f}")
                else:
                    print("\n    ✗ OPTIMALITY: Conditions violated!")
                    print("    Current basis is no longer optimal. Need to re-optimize.")
        else:
            print(f"\n>>> STEP 3: For NON-BASIC Variable - Check Optimality")
            
            # For non-basic, just check if its reduced cost changes sign
            old_reduced_cost = self.optimal_tableau[-1][var_idx]
            if self.is_maximization:
                new_reduced_cost = old_reduced_cost + delta_c
            else:
                new_reduced_cost = old_reduced_cost - delta_c
            
            print(f"    Old reduced cost (Zj-Cj) for x{var_num}: {old_reduced_cost:.4f}")
            print(f"    New reduced cost after Δc = {delta_c}:")
            print(f"    New (Zj-Cj) = {new_reduced_cost:.4f}")
            
            if self.is_maximization:
                is_optimal = new_reduced_cost >= -1e-10
            else:
                is_optimal = new_reduced_cost <= 1e-10
            
            if is_optimal:
                print(f"\n    ✓ OPTIMALITY: Reduced cost condition still satisfied!")
                print("    Current solution remains optimal with same basis.")
                print(f"\n>>> STEP 4: Calculate New Optimal Z")
                print(f"    Since x{var_num} = 0, the change in c{var_num} does not affect Z")
                print(f"    New Optimal Z = {self.optimal_z:.4f} (unchanged)")
            else:
                print(f"\n    ✗ OPTIMALITY: Reduced cost condition violated!")
                print(f"    x{var_num} should enter the basis. Need to re-optimize.")
        
        print("\n" + "-"*70)
        print("                    SUMMARY")
        print("-"*70)
        print(f"\n  Variable: x{var_num}")
        print(f"  Original coefficient: c{var_num} = {old_coef}")
        print(f"  New coefficient: c{var_num} = {new_coef}")
        print(f"  Change: Δc = {delta_c}")
    
    def analyze_new_constraint(self):
        """Analyze the effect of adding a new constraint"""
        print("\n" + "="*70)
        print("         SENSITIVITY ANALYSIS: ADD NEW CONSTRAINT")
        print("="*70)
        
        print("\nCurrent optimal solution:")
        for i in range(self.num_variables):
            print(f"  x{i+1} = {self.optimal_solution[f'x{i+1}']:.4f}")
        print(f"\n  Optimal Z = {self.optimal_z:.4f}")
        
        print("\n" + "-"*50)
        print("Enter the new constraint:")
        print("-"*50)
        
        # Get new constraint coefficients
        new_constraint = []
        for j in range(self.num_variables):
            while True:
                try:
                    coef = float(input(f"  Coefficient of x{j+1}: "))
                    new_constraint.append(coef)
                    break
                except ValueError:
                    print("  Invalid input.")
        
        while True:
            try:
                ctype = int(input("  Constraint type (1=<=, 2=>=, 3==): "))
                if ctype in [1, 2, 3]:
                    break
                print("  Please enter 1, 2, or 3")
            except ValueError:
                print("  Invalid input.")
        
        while True:
            try:
                new_rhs = float(input("  Right-hand side (RHS) value: "))
                break
            except ValueError:
                print("  Invalid input.")
        
        type_symbols = {1: "<=", 2: ">=", 3: "="}
        
        # Display new constraint
        terms = []
        for j, c in enumerate(new_constraint):
            if c >= 0 and j > 0:
                terms.append(f"+ {c}x{j+1}")
            elif c < 0:
                terms.append(f"- {abs(c)}x{j+1}")
            else:
                terms.append(f"{c}x{j+1}")
        print(f"\nNew Constraint: " + " ".join(terms) + f" {type_symbols[ctype]} {new_rhs}")
        
        print("\n" + "-"*70)
        print("                    ANALYSIS STEPS")
        print("-"*70)
        
        print(f"\n>>> STEP 1: Check if Current Solution Satisfies New Constraint")
        
        # Calculate LHS of new constraint with current solution
        lhs = sum(new_constraint[j] * self.optimal_solution[f"x{j+1}"] 
                  for j in range(self.num_variables))
        
        print(f"\n    Substituting current optimal values:")
        terms = []
        for j in range(self.num_variables):
            terms.append(f"({new_constraint[j]} × {self.optimal_solution[f'x{j+1}']:.4f})")
        print(f"    LHS = " + " + ".join(terms))
        print(f"        = {lhs:.4f}")
        
        print(f"\n    Constraint: LHS {type_symbols[ctype]} {new_rhs}")
        
        # Check satisfaction
        is_satisfied = False
        if ctype == 1:  # <=
            is_satisfied = lhs <= new_rhs + 1e-10
            print(f"    Check: {lhs:.4f} <= {new_rhs} ?")
        elif ctype == 2:  # >=
            is_satisfied = lhs >= new_rhs - 1e-10
            print(f"    Check: {lhs:.4f} >= {new_rhs} ?")
        else:  # =
            is_satisfied = abs(lhs - new_rhs) < 1e-10
            print(f"    Check: {lhs:.4f} = {new_rhs} ?")
        
        if is_satisfied:
            print(f"\n    ✓ SATISFIED: Current solution satisfies the new constraint!")
            print(f"\n>>> STEP 2: Conclusion")
            print("    The current optimal solution remains optimal.")
            print("    Adding this constraint does not change the solution.")
            print(f"\n    Optimal Z = {self.optimal_z:.4f} (unchanged)")
        else:
            print(f"\n    ✗ VIOLATED: Current solution violates the new constraint!")
            print(f"\n>>> STEP 2: New Optimization Required")
            print("    The current solution is no longer feasible.")
            print("    Need to add the constraint and re-solve the problem.")
            
            print(f"\n>>> STEP 3: Re-solving with New Constraint")
            
            # Create new problem
            new_solver = SensitivityAnalysis()
            new_solver.num_variables = self.num_variables
            new_solver.num_constraints = self.num_constraints + 1
            new_solver.objective = self.objective[:]
            new_solver.constraints = [row[:] for row in self.constraints]
            new_solver.constraints.append(new_constraint)
            new_solver.rhs = self.rhs[:] + [new_rhs]
            new_solver.constraint_types = self.constraint_types[:] + [ctype]
            new_solver.is_maximization = self.is_maximization
            new_solver.M = self.M
            
            success = new_solver.solve_initial_problem()
            
            if success:
                print("\n>>> STEP 4: Compare Solutions")
                print(f"\n    Original Optimal Z = {self.optimal_z:.4f}")
                print(f"    New Optimal Z = {new_solver.optimal_z:.4f}")
                print(f"    Change in Z = {new_solver.optimal_z - self.optimal_z:.4f}")
                
                print("\n    Change in Decision Variables:")
                for i in range(self.num_variables):
                    old_val = self.optimal_solution[f"x{i+1}"]
                    new_val = new_solver.optimal_solution[f"x{i+1}"]
                    print(f"      x{i+1}: {old_val:.4f} → {new_val:.4f} (Δ = {new_val - old_val:.4f})")
        
        print("\n" + "-"*70)
        print("                    SUMMARY")
        print("-"*70)
        print(f"\n  New Constraint: " + " ".join(terms) + f" {type_symbols[ctype]} {new_rhs}")
        if is_satisfied:
            print(f"  Status: Constraint is SATISFIED by current solution")
            print(f"  Result: Optimal solution UNCHANGED")
        else:
            print(f"  Status: Constraint is VIOLATED by current solution")
            print(f"  Result: Re-optimization required")
    
    def analyze_new_variable(self):
        """Analyze the effect of adding a new variable"""
        print("\n" + "="*70)
        print("          SENSITIVITY ANALYSIS: ADD NEW VARIABLE")
        print("="*70)
        
        new_var_num = self.num_variables + 1
        
        print(f"\nAdding new variable: x{new_var_num}")
        print("-"*50)
        
        # Get coefficient in objective function
        while True:
            try:
                obj_coef = float(input(f"  Coefficient in objective function (c{new_var_num}): "))
                break
            except ValueError:
                print("  Invalid input.")
        
        # Get coefficients in each constraint
        constraint_coefs = []
        print(f"\n  Coefficients in constraints (a_i{new_var_num}):")
        for i in range(self.num_constraints):
            while True:
                try:
                    coef = float(input(f"    Coefficient in constraint {i+1}: "))
                    constraint_coefs.append(coef)
                    break
                except ValueError:
                    print("    Invalid input.")
        
        print("\n" + "-"*70)
        print("                    ANALYSIS STEPS")
        print("-"*70)
        
        print(f"\n>>> STEP 1: New Variable Information")
        print(f"    Variable: x{new_var_num}")
        print(f"    Objective coefficient: c{new_var_num} = {obj_coef}")
        print(f"    Constraint coefficients: {constraint_coefs}")
        
        print(f"\n>>> STEP 2: Calculate Reduced Cost (Zj - Cj)")
        print("    For new variable, reduced cost = CB × column - c_new")
        
        # Get CB (coefficients of basic variables in objective)
        cb = []
        for bv in self.optimal_basic_vars:
            if bv < self.num_variables:
                cb.append(self.objective[bv])
            else:
                cb.append(0)
        
        print(f"\n    CB (objective coefficients of basic variables):")
        for i, bv in enumerate(self.optimal_basic_vars):
            print(f"      {self.var_names[bv]}: {cb[i]}")
        
        # Calculate B^-1 * a (column in optimal tableau)
        column_in_tableau = []
        for i in range(self.num_constraints):
            val = 0
            for j in range(self.num_constraints):
                val += self.B_inverse[i][j] * constraint_coefs[j]
            column_in_tableau.append(val)
        
        print(f"\n    New column in optimal tableau (B^-1 × a):")
        for i, val in enumerate(column_in_tableau):
            print(f"      Row {i+1}: {val:.4f}")
        
        # Calculate Zj
        zj = sum(cb[i] * column_in_tableau[i] for i in range(self.num_constraints))
        
        print(f"\n    Zj = CB × (B^-1 × a)")
        terms = [f"({cb[i]} × {column_in_tableau[i]:.4f})" for i in range(self.num_constraints)]
        print(f"       = " + " + ".join(terms))
        print(f"       = {zj:.4f}")
        
        # Calculate reduced cost
        if self.is_maximization:
            reduced_cost = zj - obj_coef
            print(f"\n    Reduced Cost = Zj - Cj = {zj:.4f} - {obj_coef} = {reduced_cost:.4f}")
            should_enter = reduced_cost < -1e-10
        else:
            reduced_cost = zj - obj_coef
            print(f"\n    Reduced Cost = Zj - Cj = {zj:.4f} - {obj_coef} = {reduced_cost:.4f}")
            should_enter = reduced_cost > 1e-10
        
        print(f"\n>>> STEP 3: Check Optimality Condition")
        
        opt_type = "Maximize" if self.is_maximization else "Minimize"
        if self.is_maximization:
            condition = "Zj - Cj >= 0 for optimality"
        else:
            condition = "Zj - Cj <= 0 for optimality"
        
        print(f"    For {opt_type}: {condition}")
        print(f"    Current Zj - Cj = {reduced_cost:.4f}")
        
        if not should_enter:
            print(f"\n    ✓ OPTIMAL: Condition satisfied!")
            print(f"    Current solution remains optimal with x{new_var_num} = 0")
            print(f"\n    Optimal Z = {self.optimal_z:.4f} (unchanged)")
        else:
            print(f"\n    ✗ NOT OPTIMAL: Condition violated!")
            print(f"    x{new_var_num} should enter the basis.")
            print("    Need to continue simplex iterations with the new variable.")
        
        print("\n" + "-"*70)
        print("                    SUMMARY")
        print("-"*70)
        print(f"\n  New Variable: x{new_var_num}")
        print(f"  Objective Coefficient: c{new_var_num} = {obj_coef}")
        print(f"  Reduced Cost: {reduced_cost:.4f}")
        if not should_enter:
            print(f"  Decision: x{new_var_num} stays out of basis (= 0)")
            print(f"  Optimal Z remains: {self.optimal_z:.4f}")
        else:
            print(f"  Decision: x{new_var_num} should enter basis")
            print("  Re-optimization needed")
    
    def calculate_allowable_ranges(self):
        """Calculate allowable ranges for sensitivity analysis"""
        print("\n" + "="*70)
        print("              ALLOWABLE RANGES CALCULATION")
        print("="*70)
        
        print("\n>>> This analysis calculates the range of values over which")
        print(">>> the current optimal basis remains optimal.")
        
        # RHS ranges
        print("\n" + "-"*70)
        print("  1. ALLOWABLE RANGES FOR RHS VALUES (Right-Hand Sides)")
        print("-"*70)
        
        print("\n  For each constraint, the allowable range is:")
        print("  [Current Value - Allowable Decrease, Current Value + Allowable Increase]")
        
        for con in range(self.num_constraints):
            print(f"\n  Constraint {con+1} (b{con+1} = {self.rhs[con]}):")
            
            # Calculate allowable decrease and increase
            min_ratio_inc = float('inf')
            min_ratio_dec = float('inf')
            
            for i in range(self.num_constraints):
                b_inv_val = self.B_inverse[i][con]
                current_rhs = self.optimal_tableau[i][-1]
                
                if b_inv_val > 1e-10:
                    ratio = current_rhs / b_inv_val
                    min_ratio_dec = min(min_ratio_dec, ratio)
                elif b_inv_val < -1e-10:
                    ratio = -current_rhs / b_inv_val
                    min_ratio_inc = min(min_ratio_inc, ratio)
            
            if min_ratio_dec == float('inf'):
                print(f"    Allowable Decrease: ∞")
            else:
                print(f"    Allowable Decrease: {min_ratio_dec:.4f}")
            
            if min_ratio_inc == float('inf'):
                print(f"    Allowable Increase: ∞")
            else:
                print(f"    Allowable Increase: {min_ratio_inc:.4f}")
            
            lower = self.rhs[con] - min_ratio_dec if min_ratio_dec != float('inf') else float('-inf')
            upper = self.rhs[con] + min_ratio_inc if min_ratio_inc != float('inf') else float('inf')
            
            if lower == float('-inf'):
                lower_str = "-∞"
            else:
                lower_str = f"{lower:.4f}"
            if upper == float('inf'):
                upper_str = "+∞"
            else:
                upper_str = f"{upper:.4f}"
            
            print(f"    Allowable Range: [{lower_str}, {upper_str}]")
        
        # Objective coefficient ranges
        print("\n" + "-"*70)
        print("  2. ALLOWABLE RANGES FOR OBJECTIVE COEFFICIENTS")
        print("-"*70)
        
        for var in range(self.num_variables):
            var_name = f"x{var+1}"
            current_coef = self.objective[var]
            is_basic = self.optimal_solution[f"x{var+1}"] > 1e-10
            
            print(f"\n  {var_name} (c{var+1} = {current_coef}) - {'BASIC' if is_basic else 'NON-BASIC'}:")
            
            if is_basic:
                # Find row containing this variable
                basic_row = -1
                for i, bv in enumerate(self.optimal_basic_vars):
                    if bv == var:
                        basic_row = i
                        break
                
                if basic_row >= 0:
                    min_inc = float('inf')
                    min_dec = float('inf')
                    
                    for j in range(len(self.optimal_tableau[0]) - 1):
                        if j not in self.optimal_basic_vars:
                            zj_cj = self.optimal_tableau[-1][j]
                            coef = self.optimal_tableau[basic_row][j]
                            
                            if abs(coef) > 1e-10:
                                ratio = zj_cj / coef
                                if self.is_maximization:
                                    if coef > 0:
                                        min_inc = min(min_inc, ratio)
                                    else:
                                        min_dec = min(min_dec, -ratio)
                                else:
                                    if coef < 0:
                                        min_inc = min(min_inc, -ratio)
                                    else:
                                        min_dec = min(min_dec, ratio)
                    
                    if min_dec == float('inf'):
                        print(f"    Allowable Decrease: ∞")
                    else:
                        print(f"    Allowable Decrease: {min_dec:.4f}")
                    
                    if min_inc == float('inf'):
                        print(f"    Allowable Increase: ∞")
                    else:
                        print(f"    Allowable Increase: {min_inc:.4f}")
            else:
                # Non-basic: allowable change based on reduced cost
                reduced_cost = self.optimal_tableau[-1][var]
                
                if self.is_maximization:
                    print(f"    Allowable Decrease: ∞ (stays non-basic)")
                    if reduced_cost >= 0:
                        print(f"    Allowable Increase: {reduced_cost:.4f}")
                    else:
                        print(f"    Allowable Increase: 0 (should already be in basis)")
                else:
                    print(f"    Allowable Increase: ∞ (stays non-basic)")
                    if reduced_cost <= 0:
                        print(f"    Allowable Decrease: {abs(reduced_cost):.4f}")
                    else:
                        print(f"    Allowable Decrease: 0 (should already be in basis)")
        
        # Shadow prices
        print("\n" + "-"*70)
        print("  3. SHADOW PRICES (DUAL VALUES)")
        print("-"*70)
        
        col_offset = self.num_variables
        for i in range(self.num_constraints):
            if col_offset + i < len(self.optimal_tableau[-1]) - 1:
                sp = self.optimal_tableau[-1][col_offset + i]
                if self.is_maximization:
                    sp = -sp
                print(f"\n  Constraint {i+1}: y{i+1} = {sp:.4f}")
                print(f"    Interpretation: If b{i+1} increases by 1 unit,")
                if self.is_maximization:
                    print(f"                    Z will increase by {sp:.4f}")
                else:
                    print(f"                    Z will decrease by {-sp:.4f}")
    
    def print_matrix(self, matrix, name="Matrix"):
        """Print a matrix nicely"""
        print(f"\n{name}:")
        for row in matrix:
            print("    [" + "  ".join([f"{val:8.4f}" for val in row]) + "]")
    
    def run(self):
        """Main method to run the sensitivity analysis"""
        while True:
            self.__init__()  # Reset
            self.get_user_input()
            
            input("\nPress Enter to solve the initial LP problem...")
            
            success = self.solve_initial_problem()
            
            if success:
                restart = self.sensitivity_menu()
                if not restart:
                    break
            else:
                choice = input("\nWould you like to try a different problem? (y/n): ")
                if choice.lower() != 'y':
                    break


def main():
    """Main function"""
    print("\n" + "="*70)
    print("|" + " "*15 + "SENSITIVITY ANALYSIS SOLVER" + " "*26 + "|")
    print("|" + " "*12 + "Linear Programming Post-Optimality" + " "*21 + "|")
    print("|" + " "*10 + "Step-by-Step Like Pen and Paper!" + " "*24 + "|")
    print("="*70)
    
    solver = SensitivityAnalysis()
    solver.run()


if __name__ == "__main__":
    main()
