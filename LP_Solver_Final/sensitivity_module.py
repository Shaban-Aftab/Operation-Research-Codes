"""
Post-Optimal Sensitivity Analysis Module
================================================================================
Analyzes how changes in problem parameters affect the optimal solution
of linear programming problems solved by the simplex method.

Features:
► RHS perturbation analysis (shadow prices, dual values)
► Objective coefficient variation analysis  
► Allowable range computation

Built entirely with Python standard library - NO external dependencies!
Integrates seamlessly with LinearOptimizationEngine through imports.
"""

from simplex_refactored import LinearOptimizationEngine
from copy import deepcopy


class PostOptimalAnalyzer:
    """
    Advanced sensitivity analysis engine for examining optimal LP solutions.
    
    This class performs various post-optimality analyses without resolving
    the problem from scratch, using dual values and basis inverse calculations.
    """
    
    def __init__(self, optimization_engine):
        """
        Initialize analyzer with a solved optimization engine instance.
        
        Args:
            optimization_engine: A solved LinearOptimizationEngine instance
        """
        if not isinstance(optimization_engine, LinearOptimizationEngine):
            raise TypeError("Engine must be a LinearOptimizationEngine instance")
        
        # Store reference to the solver engine
        self.solver_engine = optimization_engine
        
        # Extract solution data package
        self.solution_package = optimization_engine.export_solution_package()
        
        # Unpack frequently accessed data
        self.solution_tableau = self.solution_package['tableau']
        self.foundation_variable_set = self.solution_package['basic_indices']
        self.optimal_assignments = self.solution_package['solution_values']
        self.optimal_objective = self.solution_package['objective_value']
        self.variable_registry = self.solution_package['variable_names']
        
        # Problem parameters
        self.decision_variable_count = self.solution_package['decision_count']
        self.restriction_count = self.solution_package['constraint_count']
        self.maximization_flag = self.solution_package['is_maximization']
        self.restriction_categories = self.solution_package['constraint_types']
        self.boundary_limits = self.solution_package['rhs_values']
        self.objective_weights = self.solution_package['objective_coefficients']
        self.constraint_coefficients = self.solution_package['constraint_matrix']
        
        # Extract basis inverse for sensitivity calculations
        self.basis_inverse_matrix = optimization_engine.extract_basis_inverse_matrix()
        
        # Visual formatting
        self.DIVIDER_HEAVY = "=" * 70
        self.DIVIDER_LIGHT = "-" * 70
        self.DIVIDER_DASH = "-" * 70
    
    def compute_marginal_prices(self):
        """
        Calculate shadow prices (dual values/marginal prices) for each constraint.
        These indicate how much the objective function would improve per unit
        increase in the RHS of each constraint.
        """
        marginal_prices = []
        column_offset = self.decision_variable_count
        
        for i in range(self.restriction_count):
            if column_offset + i < len(self.solution_tableau[-1]) - 1:
                dual_value = self.solution_tableau[-1][column_offset + i]
                # Adjust sign for maximization
                if self.maximization_flag:
                    dual_value = -dual_value
                marginal_prices.append(dual_value)
            else:
                marginal_prices.append(0.0)
        
        return marginal_prices
    
    def analyze_rhs_perturbation(self):
        """
        Analyze the impact of changing right-hand side (RHS) values.
        Examines how modifying constraint bounds affects the optimal solution.
        """
        print(f"\n{self.DIVIDER_HEAVY}")
        print("      SENSITIVITY ANALYSIS: RHS PERTURBATION")
        print(self.DIVIDER_HEAVY)
        
        # Display current constraint bounds
        print("\n┌─ Current Constraint Bounds ─┐")
        inequality_markers = {1: "<=", 2: ">=", 3: "="}
        
        for i in range(self.restriction_count):
            constraint_expr = self._format_constraint_expression(
                self.constraint_coefficients[i]
            )
            symbol = inequality_markers[self.restriction_categories[i]]
            print(f"│ {i+1}. {constraint_expr} {symbol} {self.boundary_limits[i]}")
        print("└──────────────────────────────┘")
        
        # Select constraint to analyze
        while True:
            try:
                constraint_num = int(input(f"\n→ Select constraint (1-{self.restriction_count}): "))
                if 1 <= constraint_num <= self.restriction_count:
                    break
                print(f"⚠ Enter a number between 1 and {self.restriction_count}")
            except ValueError:
                print("⚠ Invalid input")
        
        constraint_idx = constraint_num - 1
        original_rhs = self.boundary_limits[constraint_idx]
        
        # Get new RHS value
        while True:
            try:
                new_rhs = float(input(f"→ Enter new RHS value (current = {original_rhs}): "))
                break
            except ValueError:
                print("⚠ Invalid input")
        
        rhs_delta = new_rhs - original_rhs
        
        print(f"\n{self.DIVIDER_LIGHT}")
        print("              ANALYSIS PROCEDURE")
        print(self.DIVIDER_LIGHT)
        
        # Step 1: Calculate change
        print(f"\n▶ Step 1: Quantify RHS Modification")
        print(f"   Original b[{constraint_num}] = {original_rhs}")
        print(f"   Modified b[{constraint_num}] = {new_rhs}")
        print(f"   Δb[{constraint_num}] = {rhs_delta}")
        
        # Step 2: Show basis inverse
        print(f"\n▶ Step 2: Basis Inverse Matrix B^(-1)")
        self._display_matrix(self.basis_inverse_matrix, "   B^(-1)")
        
        # Step 3: Calculate new basic solution
        print(f"\n▶ Step 3: Compute Updated Basic Solution")
        print("   Formula: x_B(new) = B^(-1) × b(new)")
        
        # Create new RHS vector
        new_rhs_vector = self.boundary_limits[:]
        new_rhs_vector[constraint_idx] = new_rhs
        
        print(f"\n   Original RHS: {self.boundary_limits}")
        print(f"   Modified RHS: {new_rhs_vector}")
        
        # Calculate B^(-1) * new_rhs
        updated_basic_values = []
        for i in range(self.restriction_count):
            value = sum(self.basis_inverse_matrix[i][j] * new_rhs_vector[j] 
                       for j in range(self.restriction_count))
            updated_basic_values.append(value)
        
        print(f"\n   Updated basic variable values:")
        for i, val in enumerate(updated_basic_values):
            var_idx = self.foundation_variable_set[i]
            var_name = self.variable_registry[var_idx]
            print(f"      {var_name} = {val:.6f}")
        
        # Step 4: Feasibility check
        print(f"\n▶ Step 4: Feasibility Verification")
        is_feasible = True
        for i, val in enumerate(updated_basic_values):
            status_symbol = "✓" if val >= -1e-10 else "✗"
            status_text = "feasible" if val >= -1e-10 else "VIOLATED"
            print(f"   [{status_symbol}] Row {i+1}: {val:.6f} ({status_text})")
            if val < -1e-10:
                is_feasible = False
        
        # Step 5: Calculate new objective value
        print(f"\n▶ Step 5: Objective Function Recalculation")
        
        if is_feasible:
            print("\n   ✓ Solution remains FEASIBLE")
            
            # Calculate using shadow prices
            marginal_prices = self.compute_marginal_prices()
            
            print(f"\n   Shadow Prices (Marginal Values):")
            for i, price in enumerate(marginal_prices):
                print(f"      y[{i+1}] = {price:.6f}")
            
            objective_delta = rhs_delta * marginal_prices[constraint_idx]
            new_objective = self.optimal_objective + objective_delta
            
            print(f"\n   Objective Change:")
            print(f"      ΔZ = Δb × y[{constraint_num}]")
            print(f"         = {rhs_delta} × {marginal_prices[constraint_idx]:.6f}")
            print(f"         = {objective_delta:.6f}")
            
            print(f"\n   Updated Objective:")
            print(f"      Z(new) = Z(old) + ΔZ")
            print(f"             = {self.optimal_objective:.6f} + {objective_delta:.6f}")
            print(f"             = {new_objective:.6f}")
            
        else:
            print("\n   ✗ Solution becomes INFEASIBLE")
            print("\n   The modification violates non-negativity constraints.")
            print("   Resolution: Re-optimize using Dual Simplex or Primal Simplex.")
            new_objective = None
        
        # Summary
        print(f"\n{self.DIVIDER_DASH}")
        print("                    SUMMARY")
        print(self.DIVIDER_DASH)
        print(f"\n  Constraint Modified: #{constraint_num}")
        print(f"  RHS Change: {original_rhs} → {new_rhs} (Δ = {rhs_delta})")
        print(f"  Original Objective: Z = {self.optimal_objective:.6f}")
        if is_feasible:
            print(f"  New Objective: Z = {new_objective:.6f}")
            print(f"  Net Change: ΔZ = {objective_delta:.6f}")
        else:
            print("  New Objective: Requires re-optimization (infeasible)")
    
    def analyze_coefficient_variation(self):
        """
        Analyze the impact of changing objective function coefficients.
        Determines if basis remains optimal and calculates new objective value.
        """
        print(f"\n{self.DIVIDER_HEAVY}")
        print("   SENSITIVITY ANALYSIS: OBJECTIVE COEFFICIENT VARIATION")
        print(self.DIVIDER_HEAVY)
        
        # Display current objective
        print("\n┌─ Current Objective Function ─┐")
        obj_type = "Maximize" if self.maximization_flag else "Minimize"
        obj_expr = self._format_constraint_expression(self.objective_weights)
        print(f"│ {obj_type} Z = {obj_expr}")
        print("└───────────────────────────────┘")
        
        print("\n┌─ Coefficient Values ─┐")
        for i, coef in enumerate(self.objective_weights):
            var_status = "BASIC" if self.optimal_assignments[f"x{i+1}"] > 1e-10 else "NON-BASIC"
            print(f"│ c[{i+1}] = {coef} ({var_status})")
        print("└───────────────────────┘")
        
        # Select variable
        while True:
            try:
                var_num = int(input(f"\n→ Select variable (1-{self.decision_variable_count}): "))
                if 1 <= var_num <= self.decision_variable_count:
                    break
                print(f"⚠ Enter 1-{self.decision_variable_count}")
            except ValueError:
                print("⚠ Invalid input")
        
        var_idx = var_num - 1
        original_coef = self.objective_weights[var_idx]
        
        # Get new coefficient
        while True:
            try:
                new_coef = float(input(f"→ New coefficient (current c[{var_num}] = {original_coef}): "))
                break
            except ValueError:
                print("⚠ Invalid input")
        
        coef_delta = new_coef - original_coef
        
        print(f"\n{self.DIVIDER_LIGHT}")
        print("              ANALYSIS PROCEDURE")
        print(self.DIVIDER_LIGHT)
        
        # Determine if variable is basic
        is_basic_var = self.optimal_assignments[f"x{var_num}"] > 1e-10
        
        print(f"\n▶ Step 1: Variable Classification")
        if is_basic_var:
            print(f"   x[{var_num}] is BASIC (in optimal basis)")
            print(f"   Current value: x[{var_num}] = {self.optimal_assignments[f'x{var_num}']:.6f}")
        else:
            print(f"   x[{var_num}] is NON-BASIC (value = 0)")
        
        print(f"\n▶ Step 2: Coefficient Modification")
        print(f"   Original: c[{var_num}] = {original_coef}")
        print(f"   Modified: c[{var_num}] = {new_coef}")
        print(f"   Change: Δc[{var_num}] = {coef_delta}")
        
        if is_basic_var:
            print(f"\n▶ Step 3: Optimality Check (Basic Variable)")
            print("   Recalculating reduced costs (Zj - Cj) for all variables")
            
            # Find which row contains this basic variable
            basic_row_idx = -1
            for i, bv_idx in enumerate(self.foundation_variable_set):
                if bv_idx == var_idx:
                    basic_row_idx = i
                    break
            
            if basic_row_idx >= 0:
                print(f"\n   x[{var_num}] located in tableau row {basic_row_idx + 1}")
                print("\n   Updated reduced costs:")
                
                optimality_maintained = True
                for j in range(len(self.solution_tableau[0]) - 1):
                    if j < len(self.variable_registry):
                        # Check if current column is basic
                        is_basic_column = j in self.foundation_variable_set
                        
                        if is_basic_column:
                            new_reduced_cost = 0.0  # Basic variables always have 0 reduced cost
                        else:
                            # Calculate change in reduced cost
                            old_reduced_cost = self.solution_tableau[-1][j]
                            delta_rc = coef_delta * self.solution_tableau[basic_row_idx][j]
                            
                            if self.maximization_flag:
                                new_reduced_cost = old_reduced_cost - delta_rc
                            else:
                                new_reduced_cost = old_reduced_cost + delta_rc
                        
                        # Check optimality condition
                        is_optimal_val = ((self.maximization_flag and new_reduced_cost >= -1e-10) or
                                        (not self.maximization_flag and new_reduced_cost <= 1e-10))
                        
                        status = "✓" if is_optimal_val else "✗"
                        if not is_optimal_val:
                            optimality_maintained = False
                        
                        print(f"      [{status}] {self.variable_registry[j]}: {new_reduced_cost:.6f}")
                
                if optimality_maintained:
                    print("\n   ✓ OPTIMALITY PRESERVED")
                    print("   Current basis remains optimal.")
                    
                    # Calculate new objective
                    new_obj = self.optimal_objective + coef_delta * self.optimal_assignments[f"x{var_num}"]
                    
                    print(f"\n▶ Step 4: Objective Recalculation")
                    print(f"   Z(new) = Z(old) + Δc × x[{var_num}]")
                    print(f"          = {self.optimal_objective:.6f} + {coef_delta} × {self.optimal_assignments[f'x{var_num}']:.6f}")
                    print(f"          = {new_obj:.6f}")
                else:
                    print("\n   ✗ OPTIMALITY VIOLATED")
                    print("   Current basis no longer optimal. Re-optimization required.")
        
        else:  # Non-basic variable
            print(f"\n▶ Step 3: Optimality Check (Non-Basic Variable)")
            
            # Check reduced cost change
            old_reduced_cost = self.solution_tableau[-1][var_idx]
            
            if self.maximization_flag:
                new_reduced_cost = old_reduced_cost + coef_delta
            else:
                new_reduced_cost = old_reduced_cost - coef_delta
            
            print(f"   Previous reduced cost: {old_reduced_cost:.6f}")
            print(f"   Updated reduced cost: {new_reduced_cost:.6f}")
            
            if self.maximization_flag:
                optimal_condition = new_reduced_cost >= -1e-10
            else:
                optimal_condition = new_reduced_cost <= 1e-10
            
            if optimal_condition:
                print(f"\n   ✓ OPTIMALITY PRESERVED")
                print("   Current solution remains optimal.")
                print(f"\n▶ Step 4: Objective Value")
                print(f"   Since x[{var_num}] = 0, coefficient change doesn't affect Z")
                print(f"   Z(new) = {self.optimal_objective:.6f} (unchanged)")
            else:
                print(f"\n   ✗ OPTIMALITY VIOLATED")
                print(f"   x[{var_num}] should enter basis. Re-optimization required.")
    
    def compute_allowable_ranges(self):
        """
        Calculate allowable ranges for RHS values and objective coefficients
        within which the current basis remains optimal.
        """
        print(f"\n{self.DIVIDER_HEAVY}")
        print("        ALLOWABLE RANGE COMPUTATION")
        print(self.DIVIDER_HEAVY)
        
        print("\n┌─ ALLOWABLE RHS RANGES ─┐")
        print("│ (Current basis remains optimal within these bounds)")
        print("└───────────────────────────────────────────────────┘\n")
        
        # Calculate RHS ranges using basis inverse
        for constraint_idx in range(self.restriction_count):
            print(f"  Constraint {constraint_idx + 1}:")
            print(f"    Current RHS: {self.boundary_limits[constraint_idx]}")
            
            # Create unit vector for this constraint
            unit_vector = [1 if i == constraint_idx else 0 
                          for i in range(self.restriction_count)]
            
            # Calculate B^(-1) * unit vector
            sensitivity_vector = []
            for i in range(self.restriction_count):
                val = sum(self.basis_inverse_matrix[i][j] * unit_vector[j]
                         for j in range(self.restriction_count))
                sensitivity_vector.append(val)
            
            # Find allowable range
            current_basic_values = [ self.solution_tableau[i][-1] 
                                    for i in range(self.restriction_count)]
            
            # Calculate maximum increase and decrease
            max_increase = float('inf')
            max_decrease = float('inf')
            
            for i in range(self.restriction_count):
                if abs(sensitivity_vector[i]) > 1e-10:
                    if sensitivity_vector[i] > 0:
                        max_increase = min(max_increase, 
                                          current_basic_values[i] / sensitivity_vector[i])
                    else:
                        max_decrease = min(max_decrease,
                                          -current_basic_values[i] / sensitivity_vector[i])
            
            lower_bound = self.boundary_limits[constraint_idx] - max_decrease
            upper_bound = self.boundary_limits[constraint_idx] + max_increase
            
            print(f"    Allowable Range: [{lower_bound:.4f}, {upper_bound:.4f}]")
            print()
        
        print("\n┌─ SHADOW PRICES (DUAL VALUES) ─┐")
        marginal_prices = self.compute_marginal_prices()
        for i, price in enumerate(marginal_prices):
            print(f"│ Constraint {i+1}: y[{i+1}] = {price:.6f}")
        print("└─────────────────────────────────┘")
    
    def post_optimal_menu(self):
        """
        Interactive menu for post-optimal sensitivity analysis.
        """
        while True:
            print(f"\n{self.DIVIDER_HEAVY}")
            print("         POST-OPTIMAL SENSITIVITY ANALYSIS MENU")
            print(self.DIVIDER_HEAVY)
            
            print("\n┌─ Available Analyses ─┐")
            print("│ 1. RHS Perturbation Analysis")
            print("│ 2. Objective Coefficient Variation")
            print("│ 3. Allowable Ranges Computation")
            print("│ 4. Display Optimal Solution")
            print("│ 5. Return to Main Menu")
            print("└─────────────────────────┘")
            
            try:
                selection = int(input("\n→ Your choice: "))
                
                if selection == 1:
                    self.analyze_rhs_perturbation()
                elif selection == 2:
                    self.analyze_coefficient_variation()
                elif selection == 3:
                    self.compute_allowable_ranges()
                elif selection == 4:
                    self._display_optimal_solution()
                elif selection == 5:
                    break
                else:
                    print("⚠ Invalid choice. Select 1-5.")
            except ValueError:
                print("⚠ Invalid input. Enter a number.")
    
    def _display_optimal_solution(self):
        """Display the optimal solution summary"""
        print(f"\n{self.DIVIDER_LIGHT}")
        print("           OPTIMAL SOLUTION SUMMARY")
        print(self.DIVIDER_LIGHT)
        
        print("\n┌─ Decision Variables ─┐")
        for i in range(self.decision_variable_count):
            var_name = f"x{i+1}"
            value = self.optimal_assignments[var_name]
            print(f"│ {var_name} = {value:.6f}")
        print("└───────────────────────┘")
        
        obj_type = "Maximum" if self.maximization_flag else "Minimum"
        print(f"\n{obj_type} Z = {self.optimal_objective:.6f}")
        
        print("\n┌─ Basic Variables ─┐")
        for i, var_idx in enumerate(self.foundation_variable_set):
            var_name = self.variable_registry[var_idx]
            value = self.solution_tableau[i][-1]
            print(f"│ {var_name} = {value:.6f}")
        print("└────────────────────┘")
    
    def _format_constraint_expression(self, coefficients):
        """Format coefficients into a readable expression"""
        terms = []
        for idx, coef in enumerate(coefficients):
            if idx < self.decision_variable_count:
                var_name = f"x{idx+1}"
                if idx == 0:
                    terms.append(f"{coef}{var_name}")
                else:
                    if coef >= 0:
                        terms.append(f"+ {coef}{var_name}")
                    else:
                        terms.append(f"- {abs(coef)}{var_name}")
        return " ".join(terms) if terms else "0"
    
    def _display_matrix(self, matrix, title="Matrix"):
        """Display a matrix in formatted layout"""
        print(f"{title}:")
        for row in matrix:
            formatted_row = "  ["
            formatted_row += ", ".join(f"{val:8.4f}" for val in row)
            formatted_row += " ]"
            print(formatted_row)


if __name__ == "__main__":
    print("\nThis module provides post-optimal sensitivity analysis.")
    print("Use it by importing and creating a PostOptimalAnalyzer with a")
    print("solved LinearOptimizationEngine instance.")
    print("\nExample:")
    print("  from simplex_refactored import LinearOptimizationEngine")
    print("  from sensitivity_module import PostOptimalAnalyzer")
    print("  ")
    print("  # Solve problem")
    print("  engine = LinearOptimizationEngine()")
    print("  engine.gather_problem_configuration()")
    print("  engine.commence_solution_process()")
    print("  ")
    print("  # Analyze sensitivity")
    print("  analyzer = PostOptimalAnalyzer(engine)")
    print("  analyzer.post_optimal_menu()")
