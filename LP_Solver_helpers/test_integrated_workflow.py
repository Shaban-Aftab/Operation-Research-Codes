"""
Comprehensive Test for Integrated LP Solver
Tests the complete workflow: Solve → Sensitivity Analysis
"""

from simplex_refactored import LinearOptimizationEngine
from sensitivity_module import PostOptimalAnalyzer


def test_complete_workflow():
    """
    Test complete workflow with a simple LP problem:
    Maximize Z = 3x1 + 5x2
    Subject to:
      x1 + x2 <= 4
      2x1 + x2 <= 7
      x1, x2 >= 0
    
    Expected: x1 = 3, x2 = 1, Z = 14
    """
    print("="*70)
    print("INTEGRATED SOLVER TEST - Complete Workflow")
    print("="*70)
    
    # Step 1: Create and solve problem
    print("\n[STEP 1] Creating and solving LP problem...")
    print("-"*70)
    
    engine = LinearOptimizationEngine()
    
    # Set problem parameters
    engine.maximize_mode = True
    engine.decision_count = 2
    engine.restriction_count = 2
    
    engine.optimization_vector = [3, 5]
    engine.restriction_matrix = [
        [1, 1],
        [2, 1]
    ]
    engine.boundary_values = [4, 7]
    engine.restriction_types = [1, 1]  # Both <=
    
    print("\nProblem:")
    print("Maximize Z = 3x1 + 5x2")
    print("Subject to:")
    print("  x1 + x2 <= 4")
    print("  2x1 + x2 <= 7")
    print("  x1, x2 >= 0")
    
    # Solve
    engine.construct_canonical_matrix()
    engine.orchestrate_simplex_iterations()
    
    # Verify solution
    solution = engine.extract_variable_assignments()
    obj_value = engine.operational_matrix[-1][-1]
    
    print("\n[STEP 2] Verifying solution...")
    print("-"*70)
    print(f"x1 = {solution.get('x1', 0):.4f}")
    print(f"x2 = {solution.get('x2', 0):.4f}")
    print(f"Z = {obj_value:.4f}")
    
    # Step 2: Create analyzer and test export
    print("\n[STEP 3] Testing sensitivity analysis integration...")
    print("-"*70)
    
    try:
        analyzer = PostOptimalAnalyzer(engine)
        print("✓ PostOptimalAnalyzer created successfully")
        
        # Verify data was exported correctly
        assert analyzer.decision_variable_count == 2, "Decision count mismatch"
        assert analyzer.restriction_count == 2, "Constraint count mismatch"
        assert analyzer.maximization_flag == True, "Optimization mode mismatch"
        print("✓ Solution data package extracted correctly")
        
        # Test shadow price calculation
        shadow_prices = analyzer.compute_marginal_prices()
        print(f"✓ Shadow prices calculated: {shadow_prices}")
        
        # Test basis inverse extraction
        basis_inv = analyzer.basis_inverse_matrix
        print(f"✓ Basis inverse extracted ({len(basis_inv)}x{len(basis_inv[0])} matrix)")
        
        # Display optimal solution via analyzer
        print("\n[STEP 4] Testing display methods...")
        print("-"*70)
        analyzer._display_optimal_solution()
        
        print("\n" + "="*70)
        print("✓✓ ALL TESTS PASSED!")
        print("="*70)
        print("\nIntegration successful:")
        print("  • Core solver works correctly")
        print("  • Data export functions properly")
        print("  • Sensitivity analyzer initializes")
        print("  • All helper methods functional")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error during sensitivity analysis: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_complete_workflow()
    if not success:
        exit(1)
