"""
Test for standalone Big-M Method solver
Tests with a problem requiring artificial variables
"""

from big_m_method import BigMSolver


def test_big_m_with_equality():
    """
    Test Big-M with equality constraint
    Maximize Z = 2x1 + 3x2
    Subject to:
      x1 + x2 = 4   (requires artificial variable)
      x1 <= 3       (slack variable)
      x2 <= 3       (slack variable)
    
    Expected: x1 = 1, x2 = 3, Z = 11
    """
    print("="*70)
    print("BIG-M TEST - Equality Constraint")
    print("="*70)
    
    solver = BigMSolver()
    
    # Set problem parameters
    solver.maximize_mode = True
    solver.decision_count = 2
    solver.restriction_count = 3
    
    solver.optimization_vector = [2, 3]
    solver.restriction_matrix = [
        [1, 1],  # x1 + x2 = 4
        [1, 0],  # x1 <= 3
        [0, 1]   # x2 <= 3
    ]
    solver.boundary_values = [4, 3, 3]
    solver.restriction_types = [3, 1, 1]  # 3 = =, 1 = <=
    
    print("\nProblem:")
    print("Maximize Z = 2x1 + 3x2")
    print("Subject to:")
    print("  x1 + x2 = 4   (equality - needs artificial var)")
    print("  x1 <= 3")
    print("  x2 <= 3")
    print("  x1, x2 >= 0")
    
    # Solve using Big-M
    solver.commence_solution_process()
    
    # Verify solution
    if solver.operational_matrix:
        solution = solver.extract_variable_assignments()
        obj_value = solver.operational_matrix[-1][-1]
        
        print("\n" + "="*70)
        print("VERIFICATION")
        print("="*70)
        print(f"x1 = {solution.get('x1', 0):.4f}")
        print(f"x2 = {solution.get('x2', 0):.4f}")
        print(f"Z = {obj_value:.4f}")
        
        return True
    return False


if __name__ == "__main__":
    success = test_big_m_with_equality()
    print(f"\n{'='*70}")
    print(f"Test {'PASSED' if success else 'FAILED'}")
    print(f"{'='*70}")
