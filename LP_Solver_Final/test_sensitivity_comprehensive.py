"""
COMPREHENSIVE SENSITIVITY ANALYSIS TEST
========================================
Demonstrates ALL 5 types of sensitivity analysis on a complex LP problem

Test Problem:
    Maximize Z = 3x1 + 2x2 + 5x3
    Subject to:
        2x1 + 3x2 + x3 <= 100  (Resource 1)
        x1 + 2x2 + 4x3 <= 80   (Resource 2)
        3x1 + x2 + 2x3 <= 90   (Resource 3)
        x1, x2, x3 >= 0
"""

from simplex_refactored import LinearOptimizationEngine
from sensitivity_module import PostOptimalAnalyzer

def run_comprehensive_sensitivity_test():
    print("="*70)
    print("     COMPREHENSIVE SENSITIVITY ANALYSIS TEST")
    print("="*70)
    
    print("\nTest Problem:")
    print("  Maximize Z = 3x1 + 2x2 + 5x3")
    print("\n  Subject to:")
    print("    2x1 + 3x2 + x3 <= 100")
    print("    x1 + 2x2 + 4x3 <= 80")
    print("    3x1 + x2 + 2x3 <= 90")
    print("    x1, x2, x3 >= 0")
    
    input("\nPress ENTER to solve...")
    
    # Create and configure solver
    solver = LinearOptimizationEngine()
    
    # Manually configure the problem
    solver.decision_variable_count = 3
    solver.restriction_count = 3
    solver.is_maximization_problem = True
    
    # Objective function: 3x1 + 2x2 + 5x3
    solver.objective_coefficients = [3, 2, 5]
    
    # Constraints
    solver.constraint_matrix = [
        [2, 3, 1],   # 2x1 + 3x2 + x3 <= 100
        [1, 2, 4],   # x1 + 2x2 + 4x3 <= 80
        [3, 1, 2]    # 3x1 + x2 + 2x3 <= 90
    ]
    
    solver.right_hand_side = [100, 80, 90]
    solver.restriction_categories = [1, 1, 1]  # All <=
    
    # Solve using simplex
    print("\n" + "="*70)
    print("          SOLVING USING SIMPLEX METHOD")
    print("="*70)
    
    solver.formulate_initial_tableau()
    solver.display_initial_configuration()
    solver.execute_optimization_algorithm()
    solver.present_optimal_solution()
    
    # Perform sensitivity analysis
    print("\n" + "="*70)
    print("       BEGINNING SENSITIVITY ANALYSIS")
    print("="*70)
    
    analyzer = PostOptimalAnalyzer(solver)
    
    # Interactive menu
    analyzer.post_optimal_menu()

if __name__ == "__main__":
    run_comprehensive_sensitivity_test()
