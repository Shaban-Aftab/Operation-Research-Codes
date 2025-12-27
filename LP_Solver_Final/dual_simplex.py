"""
Dual Simplex Method Implementation
===================================
Solves LP problems that are initially infeasible but dual-feasible.
Used after adding new constraints to maintain optimality.

Key Difference from Primal Simplex:
- Primal: Feasible → Optimal (minimize objective while maintaining feasibility)
- Dual: Infeasible but optimal → Feasible optimal (maintain optimality while getting feasible)

Selection Rules:
1. Leaving variable: Most negative RHS value (most infeasible basic variable)
2. Entering variable: Minimum positive ratio in ratio row

Built with zero external dependencies!
"""

class DualSimplexSolver:
    """
    Dual Simplex Method solver for linear programming.
    Handles problems that are infeasible but dual-feasible.
    """
    
    def __init__(self):
        self.tableau = []
        self.basic_vars = []
        self.var_names = []
        self.is_maximization = True
        self.iteration = 0
        self.max_iterations = 100
        
        # Visual formatting
        self.DIVIDER_HEAVY = "=" * 70
        self.DIVIDER_LIGHT = "-" * 70
    
    def solve_dual_simplex(self, tableau, basic_vars, var_names, is_maximization=True):
        """
        Execute dual simplex iterations starting from given tableau.
        
        Args:
            tableau: Initial simplex tableau (infeasible but dual-feasible)
            basic_vars: List of basic variable indices
            var_names: List of variable names
            is_maximization: True for max, False for min
        
        Returns:
            tuple: (optimal_tableau, basic_vars, is_optimal)
        """
        self.tableau = [row[:] for row in tableau]
        self.basic_vars = basic_vars[:]
        self.var_names = var_names[:]
        self.is_maximization = is_maximization
        self.iteration = 0
        
        print(f"\n{self.DIVIDER_HEAVY}")
        print("        DUAL SIMPLEX METHOD - RESTORING FEASIBILITY")
        print(self.DIVIDER_HEAVY)
        
        print("\n▶ Starting Condition:")
        print("  • Solution is INFEASIBLE (negative RHS values)")
        print("  • Solution is DUAL FEASIBLE (optimal objective row)")
        print("  • Goal: Restore feasibility while maintaining optimality")
        
        while self.iteration < self.max_iterations:
            self.iteration += 1
            
            print(f"\n{self.DIVIDER_LIGHT}")
            print(f"         DUAL SIMPLEX ITERATION {self.iteration}")
            print(self.DIVIDER_LIGHT)
            
            # Check if feasible
            if self._is_feasible():
                print("\n✓ FEASIBILITY RESTORED!")
                print("  All basic variables are non-negative.")
                return self.tableau, self.basic_vars, True
            
            # Find leaving variable (most negative RHS)
            leaving_row = self._find_leaving_variable()
            if leaving_row == -1:
                print("\n✗ PROBLEM IS INFEASIBLE!")
                print("  Cannot restore feasibility.")
                return self.tableau, self.basic_vars, False
            
            print(f"\n▶ Step 1: Select Leaving Variable")
            print(f"  Most negative RHS in row {leaving_row + 1}")
            print(f"  Leaving: {self.var_names[self.basic_vars[leaving_row]]}")
            print(f"  Current value: {self.tableau[leaving_row][-1]:.6f}")
            
            # Find entering variable (minimum ratio test in objective row)
            entering_col = self._find_entering_variable(leaving_row)
            if entering_col == -1:
                print("\n✗ PROBLEM IS INFEASIBLE!")
                print("  No valid entering variable found.")
                return self.tableau, self.basic_vars, False
            
            print(f"\n▶ Step 2: Select Entering Variable")
            print(f"  Minimum positive ratio in objective row")
            print(f"  Entering: {self.var_names[entering_col]}")
            
            # Perform pivot
            print(f"\n▶ Step 3: Pivot Operation")
            print(f"  Pivot element: Row {leaving_row + 1}, Column {entering_col + 1}")
            print(f"  Value: {self.tableau[leaving_row][entering_col]:.6f}")
            
            self._pivot(leaving_row, entering_col)
            
            # Update basic variables
            old_var = self.basic_vars[leaving_row]
            self.basic_vars[leaving_row] = entering_col
            
            print(f"  {self.var_names[old_var]} leaves, {self.var_names[entering_col]} enters")
            
            # Display current tableau
            self._display_tableau()
        
        print("\n⚠ Maximum iterations reached!")
        return self.tableau, self.basic_vars, False
    
    def _is_feasible(self):
        """Check if all basic variables are non-negative"""
        num_constraints = len(self.tableau) - 1
        for i in range(num_constraints):
            if self.tableau[i][-1] < -1e-10:
                return False
        return True
    
    def _find_leaving_variable(self):
        """
        Find leaving variable: row with most negative RHS
        Returns row index or -1 if none found
        """
        num_constraints = len(self.tableau) - 1
        most_negative = 0
        leaving_row = -1
        
        for i in range(num_constraints):
            rhs = self.tableau[i][-1]
            if rhs < most_negative:
                most_negative = rhs
                leaving_row = i
        
        return leaving_row
    
    def _find_entering_variable(self, leaving_row):
        """
        Find entering variable using minimum ratio test in objective row.
        For dual simplex: ratio = |z_j - c_j| / |a_ij|
        Only consider negative elements in leaving row.
        Returns column index or -1 if none found.
        """
        num_cols = len(self.tableau[0]) - 1
        obj_row = len(self.tableau) - 1
        
        min_ratio = float('inf')
        entering_col = -1
        
        print("\n  Ratio Test (Objective Row / Leaving Row):")
        
        for j in range(num_cols):
            pivot_element = self.tableau[leaving_row][j]
            
            # Only consider negative pivot elements
            if pivot_element < -1e-10:
                obj_coef = self.tableau[obj_row][j]
                
                # For maximization with dual simplex
                if self.is_maximization:
                    # We want obj_coef >= 0 (dual feasibility)
                    # Ratio = obj_coef / |pivot_element|
                    ratio = obj_coef / abs(pivot_element)
                else:
                    ratio = -obj_coef / abs(pivot_element)
                
                print(f"    Col {j+1} ({self.var_names[j]}): {obj_coef:.4f} / |{pivot_element:.4f}| = {ratio:.4f}")
                
                if ratio >= 0 and ratio < min_ratio:
                    min_ratio = ratio
                    entering_col = j
        
        if entering_col != -1:
            print(f"  → Minimum ratio: {min_ratio:.4f} at column {entering_col + 1}")
        
        return entering_col
    
    def _pivot(self, pivot_row, pivot_col):
        """Perform pivot operation"""
        pivot_element = self.tableau[pivot_row][pivot_col]
        
        # Scale pivot row
        for j in range(len(self.tableau[0])):
            self.tableau[pivot_row][j] /= pivot_element
        
        # Eliminate from other rows
        for i in range(len(self.tableau)):
            if i != pivot_row:
                multiplier = self.tableau[i][pivot_col]
                for j in range(len(self.tableau[0])):
                    self.tableau[i][j] -= multiplier * self.tableau[pivot_row][j]
    
    def _display_tableau(self):
        """Display current tableau"""
        num_constraints = len(self.tableau) - 1
        num_vars = len(self.var_names)
        
        print(f"\n  Current Tableau:")
        print("  " + "-" * 60)
        
        # Header
        header = "  Basis | "
        for name in self.var_names:
            header += f"{name:>8s} "
        header += "|      RHS"
        print(header)
        print("  " + "-" * 60)
        
        # Constraint rows
        for i in range(num_constraints):
            row_str = f"  {self.var_names[self.basic_vars[i]]:>5s} | "
            for j in range(num_vars):
                row_str += f"{self.tableau[i][j]:>8.3f} "
            row_str += f"| {self.tableau[i][-1]:>8.3f}"
            print(row_str)
        
        # Objective row
        print("  " + "-" * 60)
        row_str = "  Z-row | "
        for j in range(num_vars):
            row_str += f"{self.tableau[-1][j]:>8.3f} "
        row_str += f"| {self.tableau[-1][-1]:>8.3f}"
        print(row_str)
        print("  " + "-" * 60)


if __name__ == "__main__":
    print("\nDual Simplex Method Module")
    print("="*70)
    print("\nThis module implements the Dual Simplex algorithm.")
    print("Use it by importing and calling DualSimplexSolver.")
    print("\nExample:")
    print("  from dual_simplex import DualSimplexSolver")
    print("  solver = DualSimplexSolver()")
    print("  tableau, basis, success = solver.solve_dual_simplex(...)")
