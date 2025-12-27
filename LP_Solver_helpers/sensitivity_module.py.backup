"""
Post-Optimal Sensitivity Analysis Module
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Analyzes how changes in problem parameters affect the optimal solution
of linear programming problems solved by the simplex method.

Features:
► RHS perturbation analysis (shadow prices, dual values)
► Objective coefficient variation analysis
► New constraint impact evaluation
► New variable viability assessment
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
            raise TypeError(\"Engine must be a LinearOptimizationEngine instance\")
        
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
        self.DIVIDER_HEAVY = \"═\" * 70
        self.DIVIDER_LIGHT = \"─\" * 70
        self.DIVIDER_DASH = \"-\" * 70
    
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
        print(f\"\\n{self.DIVIDER_HEAVY}\")
        print(\"      SENSITIVITY ANALYSIS: RHS PERTURBATION\")
        print(self.DIVIDER_HEAVY)
        
        # Display current constraint bounds
        print(\"\\n┌─ Current Constraint Bounds ─┐\")
        inequality_markers = {1: \"≤\", 2: \"≥\", 3: \"=\"}
        
        for i in range(self.restriction_count):
            constraint_expr = self._format_constraint_expression(
                self.constraint_coefficients[i]
            )
            symbol = inequality_markers[self.restriction_categories[i]]
            print(f\"│ {i+1}. {constraint_expr} {symbol} {self.boundary_limits[i]}\")
        print(\"└──────────────────────────────┘\")
        
        # Select constraint to analyze
        while True:
            try:
                constraint_num = int(input(f\"\\n→ Select constraint (1-{self.restriction_count}): \"))
                if 1 <= constraint_num <= self.restriction_count:
                    break
                print(f\"⚠ Enter a number between 1 and {self.restriction_count}\")
            except ValueError:
                print(\"⚠ Invalid input\")
        
        constraint_idx = constraint_num - 1
        original_rhs = self.boundary_limits[constraint_idx]
        
        # Get new RHS value
        while True:
            try:
                new_rhs = float(input(f\"→ Enter new RHS value (current = {original_rhs}): \"))
                break
            except ValueError:
                print(\"⚠ Invalid input\")
        
        rhs_delta = new_rhs - original_rhs
        
        print(f\"\\n{self.DIVIDER_LIGHT}\")
        print(\"              ANALYSIS PROCEDURE\")
        print(self.DIVIDER_LIGHT)
        
        # Step 1: Calculate change
        print(f\"\\n▶ Step 1: Quantify RHS Modification\")
        print(f\"   Original b[{constraint_num}] = {original_rhs}\")\r\n        print(f\"   Modified b[{constraint_num}] = {new_rhs}\")\r\n        print(f\"   Δb[{constraint_num}] = {rhs_delta}\")\r\n        \r\n        # Step 2: Show basis inverse\r\n        print(f\"\\n▶ Step 2: Basis Inverse Matrix B^(-1)\")\r\n        self._display_matrix(self.basis_inverse_matrix, \"   B^(-1)\")\r\n        \r\n        # Step 3: Calculate new basic solution\r\n        print(f\"\\n▶ Step 3: Compute Updated Basic Solution\")\r\n        print(\"   Formula: x_B(new) = B^(-1) × b(new)\")\r\n        \r\n        # Create new RHS vector\r\n        new_rhs_vector = self.boundary_limits[:]\r\n        new_rhs_vector[constraint_idx] = new_rhs\r\n        \r\n        print(f\"\\n   Original RHS: {self.boundary_limits}\")\r\n        print(f\"   Modified RHS: {new_rhs_vector}\")\r\n        \r\n        # Calculate B^(-1) * new_rhs\r\n        updated_basic_values = []\r\n        for i in range(self.restriction_count):\r\n            value = sum(self.basis_inverse_matrix[i][j] * new_rhs_vector[j] \r\n                       for j in range(self.restriction_count))\r\n            updated_basic_values.append(value)\r\n        \r\n        print(f\"\\n   Updated basic variable values:\")\r\n        for i, val in enumerate(updated_basic_values):\r\n            var_idx = self.foundation_variable_set[i]\r\n            var_name = self.variable_registry[var_idx]\r\n            print(f\"      {var_name} = {val:.6f}\")\r\n        \r\n        # Step 4: Feasibility check\r\n        print(f\"\\n▶ Step 4: Feasibility Verification\")\r\n        is_feasible = True\r\n        for i, val in enumerate(updated_basic_values):\r\n            status_symbol = \"✓\" if val >= -1e-10 else \"✗\"\r\n            status_text = \"feasible\" if val >= -1e-10 else \"VIOLATED\"\r\n            print(f\"   [{status_symbol}] Row {i+1}: {val:.6f} ({status_text})\")\r\n            if val < -1e-10:\r\n                is_feasible = False\r\n        \r\n        # Step 5: Calculate new objective value\r\n        print(f\"\\n▶ Step 5: Objective Function Recalculation\")\r\n        \r\n        if is_feasible:\r\n            print(\"\\n   ✓ Solution remains FEASIBLE\")\r\n            \r\n            # Calculate using shadow prices\r\n            marginal_prices = self.compute_marginal_prices()\r\n            \r\n            print(f\"\\n   Shadow Prices (Marginal Values):\")\r\n            for i, price in enumerate(marginal_prices):\r\n                print(f\"      y[{i+1}] = {price:.6f}\")\r\n            \r\n            objective_delta = rhs_delta * marginal_prices[constraint_idx]\r\n            new_objective = self.optimal_objective + objective_delta\r\n            \r\n            print(f\"\\n   Objective Change:\")\r\n            print(f\"      ΔZ = Δb × y[{constraint_num}]\")\r\n            print(f\"         = {rhs_delta} × {marginal_prices[constraint_idx]:.6f}\")\r\n            print(f\"         = {objective_delta:.6f}\")\r\n            \r\n            print(f\"\\n   Updated Objective:\")\r\n            print(f\"      Z(new) = Z(old) + ΔZ\")\r\n            print(f\"             = {self.optimal_objective:.6f} + {objective_delta:.6f}\")\r\n            print(f\"             = {new_objective:.6f}\")\r\n            \r\n        else:\r\n            print(\"\\n   ✗ Solution becomes INFEASIBLE\")\r\n            print(\"\\n   The modification violates non-negativity constraints.\")\r\n            print(\"   Resolution: Re-optimize using Dual Simplex or Primal Simplex.\")\r\n            new_objective = None\r\n        \r\n        # Summary\r\n        print(f\"\\n{self.DIVIDER_DASH}\")\r\n        print(\"                    SUMMARY\")\r\n        print(self.DIVIDER_DASH)\r\n        print(f\"\\n  Constraint Modified: #{constraint_num}\")\r\n        print(f\"  RHS Change: {original_rhs} → {new_rhs} (Δ = {rhs_delta})\")\r\n        print(f\"  Original Objective: Z = {self.optimal_objective:.6f}\")\r\n        if is_feasible:\r\n            print(f\"  New Objective: Z = {new_objective:.6f}\")\r\n            print(f\"  Net Change: ΔZ = {objective_delta:.6f}\")\r\n        else:\r\n            print(\"  New Objective: Requires re-optimization (infeasible)\")\r\n    \r\n    def analyze_coefficient_variation(self):\r\n        \"\"\"\r\n        Analyze the impact of changing objective function coefficients.\r\n        Determines if basis remains optimal and calculates new objective value.\r\n        \"\"\"\r\n        print(f\"\\n{self.DIVIDER_HEAVY}\")\r\n        print(\"   SENSITIVITY ANALYSIS: OBJECTIVE COEFFICIENT VARIATION\")\r\n        print(self.DIVIDER_HEAVY)\r\n        \r\n        # Display current objective\r\n        print(\"\\n┌─ Current Objective Function ─┐\")\r\n        obj_type = \"Maximize\" if self.maximization_flag else \"Minimize\"\r\n        obj_expr = self._format_constraint_expression(self.objective_weights)\r\n        print(f\"│ {obj_type} Z = {obj_expr}\")\r\n        print(\"└───────────────────────────────┘\")\r\n        \r\n        print(\"\\n┌─ Coefficient Values ─┐\")\r\n        for i, coef in enumerate(self.objective_weights):\r\n            var_status = \"BASIC\" if self.optimal_assignments[f\"x{i+1}\"] > 1e-10 else \"NON-BASIC\"\r\n            print(f\"│ c[{i+1}] = {coef} ({var_status})\")\r\n        print(\"└───────────────────────┘\")\r\n        \r\n        # Select variable\r\n        while True:\r\n            try:\r\n                var_num = int(input(f\"\\n→ Select variable (1-{self.decision_variable_count}): \"))\r\n                if 1 <= var_num <= self.decision_variable_count:\r\n                    break\r\n                print(f\"⚠ Enter 1-{self.decision_variable_count}\")\r\n            except ValueError:\r\n                print(\"⚠ Invalid input\")\r\n        \r\n        var_idx = var_num - 1\r\n        original_coef = self.objective_weights[var_idx]\r\n        \r\n        # Get new coefficient\r\n        while True:\r\n            try:\r\n                new_coef = float(input(f\"→ New coefficient (current c[{var_num}] = {original_coef}): \"))\r\n                break\r\n            except ValueError:\r\n                print(\"⚠ Invalid input\")\r\n        \r\n        coef_delta = new_coef - original_coef\r\n        \r\n        print(f\"\\n{self.DIVIDER_LIGHT}\")\r\n        print(\"              ANALYSIS PROCEDURE\")\r\n        print(self.DIVIDER_LIGHT)\r\n        \r\n        # Determine if variable is basic\r\n        is_basic_var = self.optimal_assignments[f\"x{var_num}\"] > 1e-10\r\n        \r\n        print(f\"\\n▶ Step 1: Variable Classification\")\r\n        if is_basic_var:\r\n            print(f\"   x[{var_num}] is BASIC (in optimal basis)\")\r\n            print(f\"   Current value: x[{var_num}] = {self.optimal_assignments[f'x{var_num}']:.6f}\")\r\n        else:\r\n            print(f\"   x[{var_num}] is NON-BASIC (value = 0)\")\r\n        \r\n        print(f\"\\n▶ Step 2: Coefficient Modification\")\r\n        print(f\"   Original: c[{var_num}] = {original_coef}\")\r\n        print(f\"   Modified: c[{var_num}] = {new_coef}\")\r\n        print(f\"   Change: Δc[{var_num}] = {coef_delta}\")\r\n        \r\n        if is_basic_var:\r\n            print(f\"\\n▶ Step 3: Optimality Check (Basic Variable)\")\r\n            print(\"   Recalculating reduced costs (Zj - Cj) for all variables\")\r\n            \r\n            # Find which row contains this basic variable\r\n            basic_row_idx = -1\r\n            for i, bv_idx in enumerate(self.foundation_variable_set):\r\n                if bv_idx == var_idx:\r\n                    basic_row_idx = i\r\n                    break\r\n            \r\n            if basic_row_idx >= 0:\r\n                print(f\"\\n   x[{var_num}] located in tableau row {basic_row_idx + 1}\")\r\n                print(\"\\n   Updated reduced costs:\")\r\n                \r\n                optimality_maintained = True\r\n                for j in range(len(self.solution_tableau[0]) - 1):\r\n                    if j < len(self.variable_registry):\r\n                        # Check if current column is basic\r\n                        is_basic_column = j in self.foundation_variable_set\r\n                        \r\n                        if is_basic_column:\r\n                            new_reduced_cost = 0.0  # Basic variables always have 0 reduced cost\r\n                        else:\r\n                            # Calculate change in reduced cost\r\n                            old_reduced_cost = self.solution_tableau[-1][j]\r\n                            delta_rc = coef_delta * self.solution_tableau[basic_row_idx][j]\r\n                            \r\n                            if self.maximization_flag:\r\n                                new_reduced_cost = old_reduced_cost - delta_rc\r\n                            else:\r\n                                new_reduced_cost = old_reduced_cost + delta_rc\r\n                        \r\n                        # Check optimality condition\r\n                        is_optimal_val = ((self.maximization_flag and new_reduced_cost >= -1e-10) or\r\n                                        (not self.maximization_flag and new_reduced_cost <= 1e-10))\r\n                        \r\n                        status = \"✓\" if is_optimal_val else \"✗\"\r\n                        if not is_optimal_val:\r\n                            optimality_maintained = False\r\n                        \r\n                        print(f\"      [{status}] {self.variable_registry[j]}: {new_reduced_cost:.6f}\")\r\n                \r\n                if optimality_maintained:\r\n                    print(\"\\n   ✓ OPTIMALITY PRESERVED\")\r\n                    print(\"   Current basis remains optimal.\")\r\n                    \r\n                    # Calculate new objective\r\n                    new_obj = self.optimal_objective + coef_delta * self.optimal_assignments[f\"x{var_num}\"]\r\n                    \r\n                    print(f\"\\n▶ Step 4: Objective Recalculation\")\r\n                    print(f\"   Z(new) = Z(old) + Δc × x[{var_num}]\")\r\n                    print(f\"          = {self.optimal_objective:.6f} + {coef_delta} × {self.optimal_assignments[f'x{var_num}']:.6f}\")\r\n                    print(f\"          = {new_obj:.6f}\")\r\n                else:\r\n                    print(\"\\n   ✗ OPTIMALITY VIOLATED\")\r\n                    print(\"   Current basis no longer optimal. Re-optimization required.\")\r\n        \r\n        else:  # Non-basic variable\r\n            print(f\"\\n▶ Step 3: Optimality Check (Non-Basic Variable)\")\r\n            \r\n            # Check reduced cost change\r\n            old_reduced_cost = self.solution_tableau[-1][var_idx]\r\n            \r\n            if self.maximization_flag:\r\n                new_reduced_cost = old_reduced_cost + coef_delta\r\n            else:\r\n                new_reduced_cost = old_reduced_cost - coef_delta\r\n            \r\n            print(f\"   Previous reduced cost: {old_reduced_cost:.6f}\")\r\n            print(f\"   Updated reduced cost: {new_reduced_cost:.6f}\")\r\n            \r\n            if self.maximization_flag:\r\n                optimal_condition = new_reduced_cost >= -1e-10\r\n            else:\r\n                optimal_condition = new_reduced_cost <= 1e-10\r\n            \r\n            if optimal_condition:\r\n                print(f\"\\n   ✓ OPTIMALITY PRESERVED\")\r\n                print(\"   Current solution remains optimal.\")\r\n                print(f\"\\n▶ Step 4: Objective Value\")\r\n                print(f\"   Since x[{var_num}] = 0, coefficient change doesn't affect Z\")\r\n                print(f\"   Z(new) = {self.optimal_objective:.6f} (unchanged)\")\r\n            else:\r\n                print(f\"\\n   ✗ OPTIMALITY VIOLATED\")\r\n                print(f\"   x[{var_num}] should enter basis. Re-optimization required.\")\r\n    \r\n    def compute_allowable_ranges(self):\r\n        \"\"\"\r\n        Calculate allowable ranges for RHS values and objective coefficients\r\n        within which the current basis remains optimal.\r\n        \"\"\"\r\n        print(f\"\\n{self.DIVIDER_HEAVY}\")\r\n        print(\"        ALLOWABLE RANGE COMPUTATION\")\r\n        print(self.DIVIDER_HEAVY)\r\n        \r\n        print(\"\\n┌─ ALLOWABLE RHS RANGES ─┐\")\r\n        print(\"│ (Current basis remains optimal within these bounds)\")\r\n        print(\"└───────────────────────────────────────────────────┘\\n\")\r\n        \r\n        # Calculate RHS ranges using basis inverse\r\n        for constraint_idx in range(self.restriction_count):\r\n            print(f\"  Constraint {constraint_idx + 1}:\")\r\n            print(f\"    Current RHS: {self.boundary_limits[constraint_idx]}\")\r\n            \r\n            # Create unit vector for this constraint\r\n            unit_vector = [1 if i == constraint_idx else 0 \r\n                          for i in range(self.restriction_count)]\r\n            \r\n            # Calculate B^(-1) * unit vector\r\n            sensitivity_vector = []\r\n            for i in range(self.restriction_count):\r\n                val = sum(self.basis_inverse_matrix[i][j] * unit_vector[j]\r\n                         for j in range(self.restriction_count))\r\n                sensitivity_vector.append(val)\r\n            \r\n            # Find allowable range\r\n            current_basic_values = [ self.solution_tableau[i][-1] \r\n                                    for i in range(self.restriction_count)]\r\n            \r\n            # Calculate maximum increase and decrease\r\n            max_increase = float('inf')\r\n            max_decrease = float('inf')\r\n            \r\n            for i in range(self.restriction_count):\r\n                if abs(sensitivity_vector[i]) > 1e-10:\r\n                    if sensitivity_vector[i] > 0:\r\n                        max_increase = min(max_increase, \r\n                                          current_basic_values[i] / sensitivity_vector[i])\r\n                    else:\r\n                        max_decrease = min(max_decrease,\r\n                                          -current_basic_values[i] / sensitivity_vector[i])\r\n            \r\n            lower_bound = self.boundary_limits[constraint_idx] - max_decrease\r\n            upper_bound = self.boundary_limits[constraint_idx] + max_increase\r\n            \r\n            print(f\"    Allowable Range: [{lower_bound:.4f}, {upper_bound:.4f}]\")\r\n            print()\r\n        \r\n        print(\"\\n┌─ SHADOW PRICES (DUAL VALUES) ─┐\")\r\n        marginal_prices = self.compute_marginal_prices()\r\n        for i, price in enumerate(marginal_prices):\r\n            print(f\"│ Constraint {i+1}: y[{i+1}] = {price:.6f}\")\r\n        print(\"└─────────────────────────────────┘\")\r\n    \r\n    def post_optimal_menu(self):\r\n        \"\"\"\r\n        Interactive menu for post-optimal sensitivity analysis.\r\n        \"\"\"\r\n        while True:\r\n            print(f\"\\n{self.DIVIDER_HEAVY}\")\r\n            print(\"         POST-OPTIMAL SENSITIVITY ANALYSIS MENU\")\r\n            print(self.DIVIDER_HEAVY)\r\n            \r\n            print(\"\\n┌─ Available Analyses ─┐\")\r\n            print(\"│ 1. RHS Perturbation Analysis\")\r\n            print(\"│ 2. Objective Coefficient Variation\")\r\n            print(\"│ 3. Allowable Ranges Computation\")\r\n            print(\"│ 4. Display Optimal Solution\")\r\n            print(\"│ 5. Return to Main Menu\")\r\n            print(\"└─────────────────────────┘\")\r\n            \r\n            try:\r\n                selection = int(input(\"\\n→ Your choice: \"))\r\n                \r\n                if selection == 1:\r\n                    self.analyze_rhs_perturbation()\r\n                elif selection == 2:\r\n                    self.analyze_coefficient_variation()\r\n                elif selection == 3:\r\n                    self.compute_allowable_ranges()\r\n                elif selection == 4:\r\n                    self._display_optimal_solution()\r\n                elif selection == 5:\r\n                    break\r\n                else:\r\n                    print(\"⚠ Invalid choice. Select 1-5.\")\r\n            except ValueError:\r\n                print(\"⚠ Invalid input. Enter a number.\")\r\n    \r\n    def _display_optimal_solution(self):\r\n        \"\"\"Display the optimal solution summary\"\"\"\r\n        print(f\"\\n{self.DIVIDER_LIGHT}\")\r\n        print(\"           OPTIMAL SOLUTION SUMMARY\")\r\n        print(self.DIVIDER_LIGHT)\r\n        \r\n        print(\"\\n┌─ Decision Variables ─┐\")\r\n        for i in range(self.decision_variable_count):\r\n            var_name = f\"x{i+1}\"\r\n            value = self.optimal_assignments[var_name]\r\n            print(f\"│ {var_name} = {value:.6f}\")\r\n        print(\"└───────────────────────┘\")\r\n        \r\n        obj_type = \"Maximum\" if self.maximization_flag else \"Minimum\"\r\n        print(f\"\\n{obj_type} Z = {self.optimal_objective:.6f}\")\r\n        \r\n        print(\"\\n┌─ Basic Variables ─┐\")\r\n        for i, var_idx in enumerate(self.foundation_variable_set):\r\n            var_name = self.variable_registry[var_idx]\r\n            value = self.solution_tableau[i][-1]\r\n            print(f\"│ {var_name} = {value:.6f}\")\r\n        print(\"└────────────────────┘\")\r\n    \r\n    def _format_constraint_expression(self, coefficients):\r\n        \"\"\"Format coefficients into a readable expression\"\"\"\r\n        terms = []\r\n        for idx, coef in enumerate(coefficients):\r\n            if idx < self.decision_variable_count:\r\n                var_name = f\"x{idx+1}\"\r\n                if idx == 0:\r\n                    terms.append(f\"{coef}{var_name}\")\r\n                else:\r\n                    if coef >= 0:\r\n                        terms.append(f\"+ {coef}{var_name}\")\r\n                    else:\r\n                        terms.append(f\"- {abs(coef)}{var_name}\")\r\n        return \" \".join(terms) if terms else \"0\"\r\n    \r\n    def _display_matrix(self, matrix, title=\"Matrix\"):\r\n        \"\"\"Display a matrix in formatted layout\"\"\"\r\n        print(f\"{title}:\")\r\n        for row in matrix:\r\n            formatted_row = \"  [\"\r\n            formatted_row += \", \".join(f\"{val:8.4f}\" for val in row)\r\n            formatted_row += \" ]\"\r\n            print(formatted_row)\r\n\r\n\r\nif __name__ == \"__main__\":\r\n    print(\"\\nThis module provides post-optimal sensitivity analysis.\")\r\n    print(\"Use it by importing and creating a PostOptimalAnalyzer with a\")\r\n    print(\"solved LinearOptimizationEngine instance.\")\r\n    print(\"\\nExample:\")\r\n    print(\"  from simplex_refactored import LinearOptimizationEngine\")\r\n    print(\"  from sensitivity_module import PostOptimalAnalyzer\")\r\n    print(\"  \")\r\n    print(\"  # Solve problem\")\r\n    print(\"  engine = LinearOptimizationEngine()\")\r\n    print(\"  engine.gather_problem_configuration()\")\r\n    print(\"  engine.commence_solution_process()\")\r\n    print(\"  \")\r\n    print(\"  # Analyze sensitivity\")\r\n    print(\"  analyzer = PostOptimalAnalyzer(engine)\")\r\n    print(\"  analyzer.post_optimal_menu()\")\r\n
