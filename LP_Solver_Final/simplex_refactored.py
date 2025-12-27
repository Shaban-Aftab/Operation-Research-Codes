
from fractions import Fraction
from copy import deepcopy


class LinearOptimizationEngine:
    
    
    def __init__(self):

        # Core problem parameters

        self.decision_count = 0           # Number of decision variables (x1, x2, ...)
        self.restriction_count = 0        # Number of constraints
        self.optimization_vector = []     # Coefficients of objective function
        self.restriction_matrix = []      # Coefficient matrix for constraints
        self.boundary_values = []         # Right-hand side values (RHS)
        self.restriction_types = []       # Constraint types: 1(<=), 2(>=), 3(=)
        self.maximize_mode = True         # True for maximization, False for minimization
        
        # Tableau and working data
        self.operational_matrix = None    # The simplex tableau
        self.foundation_indices = []      # Indices of basic variables
        self.variable_labels = []         # Names of all variables (x, s, e, a)
        self.cycle_counter = 0            # Iteration number
        self.penalty_coefficient = 1000   # Big-M value for artificial variables
        
        # Visual formatting constants
        self.SEPARATOR_HEAVY = "═" * 70
        self.SEPARATOR_LIGHT = "─" * 70
        self.SEPARATOR_DASH = "-" * 70
        
    def gather_problem_configuration(self):

        """
        Interactive input collection from user for the LP problem.
        Validates all inputs and constructs internal problem representation.
        """
        self._display_welcome_banner()
        
        # Step 1: Determine optimization direction

        self.maximize_mode = self._prompt_optimization_type()
        
        # Step 2: Get problem dimensions

        self.decision_count = self._prompt_positive_integer(
            "\nEnter the number of decision variables: ",
            "Number of variables must be positive"
        )
        
        self.restriction_count = self._prompt_positive_integer(

            "Enter the number of constraints: ",
            "Number of constraints must be positive"
        )
        
        # Step 3: Collect objective function coefficients

        self._collect_objective_coefficients()
        
        # Step 4: Collect constraint specifications
        self._collect_constraint_specifications()
        
        # Step 5: Show formulated problem
        self._exhibit_problem_formulation()
    
    def _display_welcome_banner(self):

        """Display the application header"""
        print(f"\n{self.SEPARATOR_HEAVY}")
        print("       LINEAR OPTIMIZATION ENGINE - SIMPLEX SOLVER")
        print(self.SEPARATOR_HEAVY)
    
    def _prompt_optimization_type(self):

        """Ask user to select maximization or minimization"""
        print("\n╔════ Select Optimization Goal ════╗")
        print("║  [1] Maximize Objective          ║")
        print("║  [2] Minimize Objective          ║")
        print("╚══════════════════════════════════╝")
        
        while True:

            try:
                selection = int(input("Your choice (1 or 2): "))
                if selection in [1, 2]:
                    return selection == 1
                print("⚠ Please enter 1 or 2")
            except ValueError:
                print("⚠ Invalid input. Enter a number.")
    
    def _prompt_positive_integer(self, message, error_msg):

        """Generic method to get a positive integer from user"""

        while True:
            try:
                value = int(input(message))
                if value > 0:
                    return value
                print(f"⚠ {error_msg}")
            except ValueError:
                print("⚠ Invalid input. Please enter a number.")
    
    def _prompt_float_value(self, message):

        """Generic method to get a float value from user"""
        while True:
            try:
                return float(input(message))
            except ValueError:
                print("  ⚠ Invalid input. Please enter a number.")
    
    def _collect_objective_coefficients(self):

        """Gather coefficients for the objective function Z"""
        print(f"\n{'▼'*35}")
        print("OBJECTIVE FUNCTION COEFFICIENTS")
        print(f"{'▼'*35}")
        
        var_list = " + ".join([f"c{i+1}*x{i+1}" for i in range(self.decision_count)])
        print(f"Enter coefficients for Z = {var_list}")
        
        self.optimization_vector = []
        for i in range(self.decision_count):
            coef = self._prompt_float_value(f"  → Coefficient c{i+1} (for x{i+1}): ")
            self.optimization_vector.append(coef)
    
    def _collect_constraint_specifications(self):

        """Gather all constraint details from user"""
        print(f"\n{'▼'*35}")
        print("CONSTRAINT SPECIFICATIONS")
        print(f"{'▼'*35}")
        print("Inequality Types: [1] ≤  [2] ≥  [3] =")
        
        for i in range(self.restriction_count):

            print(f"\n┌─ Constraint #{i+1} ─┐")
            
            # Collect coefficients for this constraint
            restriction_row = []

            for j in range(self.decision_count):
                coef = self._prompt_float_value(f"  → Coefficient of x{j+1}: ")
                restriction_row.append(coef)
            
            # Get constraint type
            while True:
                try:
                    ctype = int(input("  → Type (1=≤, 2=≥, 3==): "))
                    if ctype in [1, 2, 3]:
                        break
                    print("  ⚠ Please enter 1, 2, or 3")
                except ValueError:
                    print("  ⚠ Invalid input.")
            
            # Get RHS value
            rhs_value = self._prompt_float_value("  → Right-hand side (RHS): ")
            
            # Handle negative RHS by flipping the constraint
            if rhs_value < 0:

                print("  ⓘ Negative RHS detected - normalizing constraint...")
                restriction_row = [-c for c in restriction_row]
                rhs_value = -rhs_value
                # Flip inequality direction
                if ctype == 1:
                    ctype = 2
                elif ctype == 2:
                    ctype = 1
            
            self.restriction_matrix.append(restriction_row)
            self.restriction_types.append(ctype)
            self.boundary_values.append(rhs_value)
    
    def _exhibit_problem_formulation(self):

        """Display the complete problem in standard mathematical form"""
        print(f"\n{self.SEPARATOR_HEAVY}")
        print("           FORMULATED LINEAR PROGRAM")
        print(self.SEPARATOR_HEAVY)
        
        # Objective function
        action = "Maximize" if self.maximize_mode else "Minimize"
        print(f"\n{action} Z = {self._format_expression(self.optimization_vector)}")
        
        # Constraints
        print("\nSubject to:")
        inequality_symbols = {1: "≤", 2: "≥", 3: "="}
        
        for i in range(self.restriction_count):

            expr = self._format_expression(self.restriction_matrix[i])
            symbol = inequality_symbols[self.restriction_types[i]]
            print(f"  {expr} {symbol} {self.boundary_values[i]}")
        
        print("\n  Non-negativity: x₁, x₂, ..., xₙ ≥ 0")
    
    def _format_expression(self, coefficients):

        """Format a list of coefficients into a readable expression"""
        terms = []
        for idx, coef in enumerate(coefficients):
            var_name = f"x{idx+1}"
            
            if idx == 0:
                # First term doesn't need a sign prefix if positive
                terms.append(f"{coef}{var_name}")
            else:
                if coef >= 0:
                    terms.append(f"+ {coef}{var_name}")
                else:
                    terms.append(f"- {abs(coef)}{var_name}")
        
        return " ".join(terms) if terms else "0"
    
    def construct_canonical_matrix(self):

        """
        Transform the problem into canonical form and create initial tableau.
        
        Process:
        1. Add slack variables (s) for ≤ constraints
        2. Add surplus (e) and artificial (a) variables for ≥ constraints  
        3. Add artificial variables (a) for = constraints
        4. Apply Big-M penalty to artificial variables
        5. Eliminate artificial variables from objective row
        """
        print(f"\n{self.SEPARATOR_HEAVY}")
        print("        CONSTRUCTING CANONICAL FORM TABLEAU")
        print(self.SEPARATOR_HEAVY)
        
        # Calculate variable counts
        slack_count = sum(1 for t in self.restriction_types if t == 1)
        surplus_count = sum(1 for t in self.restriction_types if t == 2)
        artificial_count = sum(1 for t in self.restriction_types if t in [2, 3])
        
        total_columns = (self.decision_count + slack_count + 
                        surplus_count + artificial_count + 1)  # +1 for RHS
        total_rows = self.restriction_count + 1  # +1 for objective row
        
        # Initialize tableau with zeros
        self.operational_matrix = [[0.0 for _ in range(total_columns)] 
                                   for _ in range(total_rows)]
        
        # Build variable name registry
        self.variable_labels = [f"x{i+1}" for i in range(self.decision_count)]
        
        # Track column positions for each variable type
        slack_position = self.decision_count
        surplus_position = self.decision_count + slack_count
        artificial_position = self.decision_count + slack_count + surplus_count
        
        self.foundation_indices = []
        
        # Populate constraint rows with appropriate variables
        for row_idx in range(self.restriction_count):
            
            # Fill decision variable coefficients
            for col_idx in range(self.decision_count):
                self.operational_matrix[row_idx][col_idx] = \
                    self.restriction_matrix[row_idx][col_idx]
            
            # Add appropriate auxiliary variables based on constraint type
            if self.restriction_types[row_idx] == 1:  # ≤ constraint
               
                self.operational_matrix[row_idx][slack_position] = 1
                self.variable_labels.append(f"s{row_idx+1}")
                self.foundation_indices.append(slack_position)
                slack_position += 1
                
            elif self.restriction_types[row_idx] == 2:  # ≥ constraint
                
                self.operational_matrix[row_idx][surplus_position] = -1
                self.variable_labels.append(f"e{row_idx+1}")
                surplus_position += 1
                
                self.operational_matrix[row_idx][artificial_position] = 1
                self.variable_labels.append(f"a{row_idx+1}")
                self.foundation_indices.append(artificial_position)
                artificial_position += 1
                
            else:  # = constraint
                
                self.operational_matrix[row_idx][artificial_position] = 1
                self.variable_labels.append(f"a{row_idx+1}")
                self.foundation_indices.append(artificial_position)
                artificial_position += 1
            
            # Set RHS value
            self.operational_matrix[row_idx][-1] = self.boundary_values[row_idx]
        
        # Construct objective function row
        self._initialize_objective_row(slack_count, surplus_count, artificial_count)
        
        # Display variable summary
        self._show_variable_inventory(slack_count, surplus_count, artificial_count)
        
        # Show initial tableau
        self.visualize_current_tableau()
    
    def _initialize_objective_row(self, slack_count, surplus_count, artificial_count):
        
        """Set up the objective function row (Zj - Cj row)"""
        obj_row_idx = len(self.operational_matrix) - 1
        
        # Fill decision variable coefficients (negated for maximization)
        for j in range(self.decision_count):
            if self.maximize_mode:
                self.operational_matrix[obj_row_idx][j] = -self.optimization_vector[j]
            else:
                self.operational_matrix[obj_row_idx][j] = self.optimization_vector[j]
        
        # Apply Big-M penalties to artificial variables
        total_vars = self.decision_count + slack_count + surplus_count
        
        for constraint_idx in range(self.restriction_count):
           
            if self.restriction_types[constraint_idx] in [2, 3]:
                # Find the artificial variable column for this constraint
                for col_idx in range(total_vars, len(self.variable_labels)):
                    if self.operational_matrix[constraint_idx][col_idx] == 1:
                        # Set Big-M penalty in objective
                        if self.maximize_mode:
                            self.operational_matrix[obj_row_idx][col_idx] = self.penalty_coefficient
                        else:
                            self.operational_matrix[obj_row_idx][col_idx] = -self.penalty_coefficient
                        
                        # Eliminate artificial variable from objective row
                        self._eliminate_from_objective(constraint_idx, col_idx)
                        break
    
    def _eliminate_from_objective(self, pivot_row, pivot_col):
       
        """Eliminate a basic variable from the objective row"""
        obj_row_idx = len(self.operational_matrix) - 1
        
        for col_idx in range(len(self.operational_matrix[obj_row_idx])):
         
            if self.maximize_mode:
                self.operational_matrix[obj_row_idx][col_idx] -= \
                    self.penalty_coefficient * self.operational_matrix[pivot_row][col_idx]
            else:
                self.operational_matrix[obj_row_idx][col_idx] += \
                    self.penalty_coefficient * self.operational_matrix[pivot_row][col_idx]
    
    def _show_variable_inventory(self, slack_cnt, surplus_cnt, artificial_cnt):
   
        """Display summary of variables in the problem"""
        print("\n┌─ Variable Inventory ─┐")
        print(f"│ Decision vars: x₁ to x{self.decision_count}")
        if slack_cnt > 0:
            print(f"│ Slack vars: s₁ to s{slack_cnt} (for ≤ constraints)")
        if surplus_cnt > 0:
            print(f"│ Surplus vars: e₁ to e{surplus_cnt} (for ≥ constraints)")
        if artificial_cnt > 0:
            print(f"│ Artificial vars: a₁ to a{artificial_cnt} (Big-M method)")
        print("└───────────────────────┘")
    
    def visualize_current_tableau(self):
       
        """Render the current tableau in formatted tabular layout"""
        print(f"\n{self.SEPARATOR_LIGHT}")
        print(f"TABLEAU — Iteration {self.cycle_counter}")
        print(self.SEPARATOR_LIGHT)
        
        # Build header
        header_parts = ["Basis |"]
        for idx in range(len(self.operational_matrix[0]) - 1):
            if idx < len(self.variable_labels):
                header_parts.append(f"{self.variable_labels[idx]:>8}")
            else:
                header_parts.append(f"{'v'+str(idx):>8}")
        header_parts.append(" |      RHS")
        header_line = "".join(header_parts)
        
        print(header_line)
        print(self.SEPARATOR_DASH)
        
        # Print constraint rows
        for row_idx in range(len(self.operational_matrix) - 1):
            if row_idx < len(self.foundation_indices):
                basis_idx = self.foundation_indices[row_idx]
                if basis_idx < len(self.variable_labels):
                    basis_label = self.variable_labels[basis_idx]
                else:
                    basis_label = f"B{row_idx+1}"
            else:
                basis_label = f"B{row_idx+1}"
            
            row_parts = [f"{basis_label:>5} |"]
            for col_idx in range(len(self.operational_matrix[row_idx]) - 1):
                row_parts.append(f"{self.operational_matrix[row_idx][col_idx]:>8.3f}")
            row_parts.append(f" | {self.operational_matrix[row_idx][-1]:>8.3f}")
            
            print("".join(row_parts))
        
        # Print objective row
        print(self.SEPARATOR_DASH)
        obj_parts = ["Zj-Cj |"]
        obj_row = self.operational_matrix[-1]
        for col_idx in range(len(obj_row) - 1):
            obj_parts.append(f" {obj_row[col_idx]:7.3f}")
        obj_parts.append(f" | {obj_row[-1]:>8.3f}")
        
        print("".join(obj_parts))
        print(self.SEPARATOR_DASH)
        
        # Display basic variable values
        print("\n┌─ Current Basic Solution ─┐")
        for idx, basis_idx in enumerate(self.foundation_indices):
            if basis_idx < len(self.variable_labels):
                var_name = self.variable_labels[basis_idx]
                value = self.operational_matrix[idx][-1]
                print(f"│ {var_name} = {value:.4f}")
        print("└───────────────────────────┘")
    
    def identify_entering_candidate(self):
        """
        Determine which non-basic variable should enter the basis.
        Returns column index of entering variable, or -1 if optimal.
        """
        objective_row = self.operational_matrix[-1][:-1]
        
        if self.maximize_mode:
            # For maximization: find most negative Zj - Cj
            minimum_value = min(objective_row)
            if minimum_value >= -1e-10:  # Optimality reached
                return -1
            return objective_row.index(minimum_value)
        else:
            # For minimization: find most positive Zj - Cj
            maximum_value = max(objective_row)
            if maximum_value <= 1e-10:  # Optimality reached
                return -1
            return objective_row.index(maximum_value)
    
    def select_departing_variable(self, entering_col):
        """
        Apply minimum ratio test to find which basic variable leaves.
        Returns row index of leaving variable, or -1 if unbounded.
        """
        ratio_candidates = []
        
        for row_idx in range(len(self.operational_matrix) - 1):
            pivot_element = self.operational_matrix[row_idx][entering_col]
            
            if pivot_element > 1e-10:  # Only consider positive denominators
                rhs_value = self.operational_matrix[row_idx][-1]
                ratio = rhs_value / pivot_element
                ratio_candidates.append((ratio, row_idx))
        
        if not ratio_candidates:
            return -1  # Unbounded solution
        
        # Select minimum ratio (with ties broken by first occurrence)
        ratio_candidates.sort()
        return ratio_candidates[0][1]
    
    def execute_matrix_transformation(self, pivot_row, pivot_col):
        """
        Perform the pivot operation to transform the tableau.
        
        Steps:
        1. Normalize the pivot row (divide by pivot element)
        2. Eliminate the pivot column from all other rows
        3. Update the basis
        """
        pivot_value = self.operational_matrix[pivot_row][pivot_col]
        
        print(f"\n┌─ Pivot Operation Details ─┐")
        print(f"│ Location: Row {pivot_row+1}, Col {pivot_col+1}")
        print(f"│ Entering: {self.variable_labels[pivot_col]}")
        if self.foundation_indices[pivot_row] < len(self.variable_labels):
            print(f"│ Leaving:  {self.variable_labels[self.foundation_indices[pivot_row]]}")
        print(f"│ Pivot:    {pivot_value:.4f}")
        print("└───────────────────────────┘")
        
        # Update basis
        self.foundation_indices[pivot_row] = pivot_col
        
        # Step 1: Normalize pivot row
        print(f"\n→ Step 1: Scale Row {pivot_row+1} by 1/{pivot_value:.4f}")
        for col_idx in range(len(self.operational_matrix[pivot_row])):
            self.operational_matrix[pivot_row][col_idx] /= pivot_value
        
        # Step 2: Eliminate from other rows
        print("→ Step 2: Row operations for elimination")
        for row_idx in range(len(self.operational_matrix)):
            if row_idx != pivot_row:
                multiplier = self.operational_matrix[row_idx][pivot_col]
                
                if abs(multiplier) > 1e-10:
                    print(f"   R{row_idx+1} ← R{row_idx+1} - ({multiplier:.4f}) × R{pivot_row+1}")
                    
                    for col_idx in range(len(self.operational_matrix[row_idx])):
                        self.operational_matrix[row_idx][col_idx] -= \
                            multiplier * self.operational_matrix[pivot_row][col_idx]
    
    def validate_optimality_criteria(self):
        """Check if current solution is optimal"""
        entering = self.identify_entering_candidate()
        return entering == -1
    
    def check_solution_boundedness(self, entering_col):
        """Check if solution is unbounded given an entering variable"""
        departing = self.select_departing_variable(entering_col)
        return departing != -1
    
    def detect_artificial_residue(self):
        """
        Check if any artificial variables remain in basis with non-zero value.
        This indicates an infeasible problem.
        """
        artificial_labels = [label for label in self.variable_labels if label.startswith('a')]
        
        for idx, basis_idx in enumerate(self.foundation_indices):
            if basis_idx < len(self.variable_labels):
                var_name = self.variable_labels[basis_idx]
                if var_name in artificial_labels:
                    value = self.operational_matrix[idx][-1]
                    if abs(value) > 1e-6:
                        return True
        return False
    
    def orchestrate_simplex_iterations(self):
        """
        Main control loop for the simplex algorithm.
        Iterates until optimality, unboundedness, or infeasibility is detected.
        """
        print(f"\n{self.SEPARATOR_HEAVY}")
        print("         INITIATING SIMPLEX OPTIMIZATION PROCESS")
        print(self.SEPARATOR_HEAVY)
        
        maximum_cycles = 100
        
        while self.cycle_counter < maximum_cycles:
            self.cycle_counter += 1
            
            print(f"\n{'◆'*35}")
            print(f"         ITERATION {self.cycle_counter}")
            print(f"{'◆'*35}")
            
            # Phase 1: Identify entering variable
            entering_col = self.identify_entering_candidate()
            
            if entering_col == -1:
                print("\n✓ OPTIMAL SOLUTION REACHED!")
                print("  (No further improvement possible)")
                break
            
            print(f"\n▶ Finding Entering Variable")
            print(f"  Examining objective row: ", end="")
            for val in self.operational_matrix[-1][:-1]:
                print(f"{val:.3f} ", end="")
            print()
            
            if self.maximize_mode:
                print(f"  Most negative → Column {entering_col+1} ({self.variable_labels[entering_col]})")
            else:
                print(f"  Most positive → Column {entering_col+1} ({self.variable_labels[entering_col]})")
            
            # Phase 2: Identify leaving variable (minimum ratio test)
            print(f"\n▶ Minimum Ratio Test")
            print("  Computing RHS / Column ratios:")
            
            for row_idx in range(len(self.operational_matrix) - 1):
                denominator = self.operational_matrix[row_idx][entering_col]
                if denominator > 1e-10:
                    numerator = self.operational_matrix[row_idx][-1]
                    ratio = numerator / denominator
                    print(f"  Row {row_idx+1}: {numerator:.3f} / {denominator:.3f} = {ratio:.3f}")
                else:
                    print(f"  Row {row_idx+1}: (skipped - non-positive)")
            
            departing_row = self.select_departing_variable(entering_col)
            
            if departing_row == -1:
                print("\n✗ UNBOUNDED SOLUTION DETECTED!")
                print("  (Objective can increase indefinitely)")
                return
            
            print(f"\n  Minimum ratio → Row {departing_row+1}")
            
            # Phase 3: Pivot operation
            print(f"\n▶ Executing Pivot Transformation")
            self.execute_matrix_transformation(departing_row, entering_col)
            
            # Display updated tableau
            self.visualize_current_tableau()
        
        if self.cycle_counter >= maximum_cycles:
            print("\n⚠ ITERATION LIMIT EXCEEDED")
            print("  Solution may not be optimal.")
            return
        
        # Check for infeasibility (artificial variables in final basis)
        if self.detect_artificial_residue():
            print("\n✗ INFEASIBLE PROBLEM DETECTED!")
            print("  (Artificial variables remain in solution)")
            return
        
        # Display final solution
        self.present_optimal_solution()
    
    def extract_variable_assignments(self):
        """Extract values of decision variables from final tableau"""
        solution_vector = {}
        
        for i in range(self.decision_count):
            solution_vector[f"x{i+1}"] = 0.0
        
        for idx, basis_idx in enumerate(self.foundation_indices):
            if basis_idx < self.decision_count:
                var_key = f"x{basis_idx+1}"
                solution_vector[var_key] = self.operational_matrix[idx][-1]
        
        return solution_vector
    
    def present_optimal_solution(self):
        """Display the final solution with verification"""
        print(f"\n{self.SEPARATOR_HEAVY}")
        print("              ★ OPTIMAL SOLUTION FOUND ★")
        print(self.SEPARATOR_HEAVY)
        
        # Get solution values
        solution = self.extract_variable_assignments()
        
        print("\n┌─ Decision Variable Values ─┐")
        for i in range(self.decision_count):
            var_name = f"x{i+1}"
            print(f"│ {var_name} = {solution[var_name]:.6f}")
        print("└─────────────────────────────┘")
        
        # Calculate objective value
        # The RHS of objective row already contains the correct value
        obj_value = self.operational_matrix[-1][-1]
        
        print(f"\n┌─ Objective Function Value ─┐")
        print(f"│ Z = {obj_value:.6f}")
        print("└─────────────────────────────┘")
        
        # Verification section
        self._verify_solution(solution, obj_value)
    
    def _verify_solution(self, solution, reported_z):
        """Verify the solution satisfies all constraints and objective"""
        print(f"\n{self.SEPARATOR_DASH}")
        print("SOLUTION VERIFICATION")
        print(self.SEPARATOR_DASH)
        
        # Verify objective value
        calculated_z = sum(self.optimization_vector[i] * solution[f"x{i+1}"] 
                          for i in range(self.decision_count))
        
        print(f"\nObjective Function Check:")
        term_list = []
        for i in range(self.decision_count):
            coef = self.optimization_vector[i]
            val = solution[f"x{i+1}"]
            term_list.append(f"({coef}×{val:.4f})")
        
        print(f"  Z = {' + '.join(term_list)}")
        print(f"  Z = {calculated_z:.6f}")
        
        if abs(calculated_z - reported_z) < 1e-4:
            print("  ✓ Objective value confirmed")
        else:
            print(f"  ⚠ Discrepancy detected: {calculated_z:.6f} vs {reported_z:.6f}")
        
        # Verify constraints
        print(f"\nConstraint Satisfaction:")
        inequality_map = {1: "≤", 2: "≥", 3: "="}
        
        all_satisfied = True
        for i in range(self.restriction_count):
            lhs = sum(self.restriction_matrix[i][j] * solution[f"x{j+1}"] 
                     for j in range(self.decision_count))
            
            rhs = self.boundary_values[i]
            symbol = inequality_map[self.restriction_types[i]]
            
            # Check satisfaction with tolerance
            satisfied = False
            if self.restriction_types[i] == 1 and lhs <= rhs + 1e-6:
                satisfied = True
            elif self.restriction_types[i] == 2 and lhs >= rhs - 1e-6:
                satisfied = True
            elif self.restriction_types[i] == 3 and abs(lhs - rhs) < 1e-6:
                satisfied = True
            
            status = "✓" if satisfied else "✗"
            all_satisfied = all_satisfied and satisfied
            
            print(f"  [{status}] Constraint {i+1}: {lhs:.4f} {symbol} {rhs:.4f}")
        
        print()
        if all_satisfied:
            print("✓ All constraints satisfied!")
        else:
            print("⚠ Some constraints violated!")
    
    def export_solution_package(self):
        """
        Export comprehensive solution data for post-optimal analysis.
        Returns dictionary with tableau, basis, solution, and metadata.
        """
        return {
            'tableau': [row[:] for row in self.operational_matrix],
            'basic_indices': self.foundation_indices[:],
            'solution_values': self.extract_variable_assignments(),
            'objective_value': self.operational_matrix[-1][-1],
            'variable_names': self.variable_labels[:],
            'decision_count': self.decision_count,
            'constraint_count': self.restriction_count,
            'is_maximization': self.maximize_mode,
            'constraint_types': self.restriction_types[:],
            'rhs_values': self.boundary_values[:],
            'objective_coefficients': self.optimization_vector[:],
            'constraint_matrix': [row[:] for row in self.restriction_matrix]
        }
    
    def extract_basis_inverse_matrix(self):
        """
        Extract B^(-1) from the optimal tableau.
        The inverse appears in the columns corresponding to original slack/artificial variables.
        """
        n = self.restriction_count
        basis_inverse = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Find slack/artificial variable columns (start after decision variables)
        col_offset = self.decision_count
        
        for i in range(n):
            for j in range(n):
                if col_offset + j < len(self.operational_matrix[0]) - 1:
                    basis_inverse[i][j] = self.operational_matrix[i][col_offset + j]
        
        return basis_inverse
    
    def commence_solution_process(self):
        """Main entry point to solve the problem"""
        self.construct_canonical_matrix()
        self.orchestrate_simplex_iterations()


def application_entry_point():
    """Main driver function for the application"""
    print(f"\n{'═'*70}")
    print("┃" + " "*16 + "LINEAR OPTIMIZATION ENGINE" + " "*27 + "┃")
    print("┃" + " "*18 + "Simplex Method Solver" + " "*30 + "┃")
    print("┃" + " "*12 + "(Zero Dependencies - Pure Python!)" + " "*21 + "┃")
    print(f"{'═'*70}")
    
    while True:
        engine = LinearOptimizationEngine()
        engine.gather_problem_configuration()
        
        input("\n→ Press ENTER to begin optimization...")
        engine.commence_solution_process()
        
        print(f"\n{'-'*70}")
        user_choice = input("\nSolve another problem? (y/n): ")
        
        if user_choice.lower() != 'y':
            print("\n" + "="*70)
            print("Thank you for using the Linear Optimization Engine!")
            print("="*70 + "\n")
            break


if __name__ == "__main__":
    application_entry_point()
