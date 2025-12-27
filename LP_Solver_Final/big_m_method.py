"""
BIG-M METHOD SOLVER
================================================================================
Specialized solver for Linear Programming problems with >= and = constraints.
Uses the Big-M technique with artificial variables to find optimal solutions.

The Big-M method works by:
1. Adding artificial variables to >= and = constraints
2. Assigning a large penalty (M) to these variables in the objective
3. Using simplex method to drive artificial variables out of the basis
4. Finding the optimal solution (or detecting infeasibility)

This implementation extends the LinearOptimizationEngine with Big-M emphasis.
================================================================================
"""

from simplex_refactored import LinearOptimizationEngine


class BigMSolver(LinearOptimizationEngine):
    """
    Big-M Method solver for LP problems requiring artificial variables.
    
    Inherits from LinearOptimizationEngine and adds Big-M specific features:
    - Emphasized Big-M visualization
    - Detailed artificial variable tracking
    - Educational step-by-step display
    """
    
    def __init__(self):
        """Initialize Big-M solver with enhanced display options."""
        super().__init__()
        self.penalty_coefficient = 1000  # Big-M value (already in parent)
        self.artificial_var_count = 0
        self.artificial_var_indices = []
    
    def display_big_m_banner(self):
        """Display Big-M method welcome banner."""
        print("\n" + "="*70)
        print("┃" + " "*20 + "BIG-M METHOD SOLVER" + " "*27 + "┃")
        print("┃" + " "*15 + "For LP with >= and = Constraints" + " "*19 + "┃")
        print("="*70)
        
        print("\n┌─ BIG-M METHOD EXPLANATION ─┐")
        print("│")
        print("│ The Big-M method handles >= and = constraints by:")
        print("│  1. Adding ARTIFICIAL variables to these constraints")
        print("│  2. Assigning large penalty M to artificial vars")
        print("│  3. Using Simplex to minimize artificial variables")
        print("│  4. If all artificials become 0 → Optimal solution")
        print("│  5. If artificials remain > 0 → Infeasible problem")
        print("│")
        print(f"│ Current M value: {self.penalty_coefficient}")
        print("└────────────────────────────────┘\n")
    
    def track_artificial_variables(self):
        """Track which variables are artificial for Big-M analysis."""
        self.artificial_var_indices = []
        
        # Find artificial variables in variable labels
        for idx, var_name in enumerate(self.variable_labels):
            if var_name.startswith('a'):  # Artificial variables start with 'a'
                self.artificial_var_indices.append(idx)
        
        self.artificial_var_count = len(self.artificial_var_indices)
    
    def display_big_m_status(self):
        """Display current status of artificial variables."""
        if not self.artificial_var_indices:
            print("\n✓ No artificial variables in current basis (Good!)")
            return
        
        print("\n" + "─"*70)
        print("BIG-M STATUS: Artificial Variables")
        print("─"*70)
        
        artificials_in_basis = []
        for idx in self.foundation_indices:
            if idx in self.artificial_var_indices:
                var_name = self.variable_labels[idx]
                # Find value in tableau
                row_idx = self.foundation_indices.index(idx)
                value = self.operational_matrix[row_idx][-1]
                artificials_in_basis.append((var_name, value))
        
        if artificials_in_basis:
            print("⚠ WARNING: Artificial variables in basis:")
            for var_name, value in artificials_in_basis:
                print(f"   {var_name} = {value:.6f}")
            print("\n   These must reach 0 for a feasible solution!")
        else:
            print("✓ All artificial variables have left the basis")
            print("  Solution is feasible!")
    
    def commence_solution_process(self):
        """
        Override parent method to add Big-M specific displays.
        """
        # Display Big-M banner first
        self.display_big_m_banner()
        
        # Build canonical form (tableau with artificial variables)
        self.construct_canonical_matrix()
        
        # Track artificial variables
        self.track_artificial_variables()
        
        if self.artificial_var_count > 0:
            print(f"\n🔴 BIG-M ACTIVATED: {self.artificial_var_count} artificial variable(s) added")
            print(f"   Penalty coefficient M = {self.penalty_coefficient}")
        else:
            print("\n✓ No artificial variables needed (all <= constraints)")
        
        # Run simplex with Big-M penalties
        print("\n" + "="*70)
        print("         INITIATING SIMPLEX WITH BIG-M METHOD")
        print("="*70)
        
        maximum_cycles = 50
        iteration_num = 0
        while iteration_num < maximum_cycles:
            # Phase 1: Identify entering variable
            entering_col = self.identify_entering_candidate()
            if entering_col == -1:
                iteration_num += 1
                self.cycle_counter = iteration_num
                # Optimal solution reached
                print(f"\n{'◆'*35}")
                print(f"         ITERATION {iteration_num}")
                print(f"{'◆'*35}\n")
                print("✓ OPTIMAL SOLUTION REACHED!")
                print("  (No further improvement possible)")
                
                # Check Big-M feasibility
                self.display_big_m_status()
                
                # Check if artificial variables remain
                artificials_in_basis = [idx for idx in self.foundation_indices 
                                       if idx in self.artificial_var_indices]
                
                if artificials_in_basis:
                    print("\n✗ INFEASIBLE PROBLEM DETECTED!")
                    print("  (Artificial variables remain in solution)")
                    print("\n🔴 This means the constraint set has NO feasible solution!")
                else:
                    self.assemble_final_solution()
                break
            
            # Increment iteration counter
            iteration_num += 1
            self.cycle_counter = iteration_num
            
            # Phase 2: Identify leaving variable (minimum ratio test)
            departing_row = self.select_departing_variable(entering_col)
            if departing_row == -1:
                # Unbounded solution
                print("\n✗ UNBOUNDED SOLUTION!")
                print("  The objective function can increase indefinitely.")
                return
            
            # Phase 3: Pivot operation
            self.execute_matrix_transformation(departing_row, entering_col)
            
            # Display tableau after pivot
            self.visualize_current_tableau()
            
            # Display Big-M status after each iteration
            if iteration_num > 0 and self.artificial_var_count > 0:
                self.display_big_m_status()
        
        if iteration_num >= maximum_cycles:
            print(f"\n⚠ Maximum iterations ({maximum_cycles}) reached!")
    
    def assemble_final_solution(self):
        """Override to add Big-M specific success message."""
        print("\n" + "="*70)
        print("              ★ OPTIMAL SOLUTION FOUND (BIG-M) ★")
        print("="*70)
        
        # Call parent's solution display method
        self.present_optimal_solution()
        
        print("\n✓ BIG-M METHOD SUCCESSFUL!")
        print("  All artificial variables have been eliminated.")


def application_entry_point():
    """
    Main entry point for Big-M Method solver application.
    """
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " "*15 + "WELCOME TO BIG-M METHOD SOLVER" + " "*22 + "║")
    print("║" + " "*10 + "Solve LP Problems with >= and = Constraints" + " "*12 + "║")
    print("╚" + "═"*68 + "╝\n")
    
    solver = BigMSolver()
    solver.gather_problem_configuration()
    
    input("\n→ Press ENTER to solve using Big-M method...")
    solver.commence_solution_process()


if __name__ == "__main__":
    application_entry_point()
