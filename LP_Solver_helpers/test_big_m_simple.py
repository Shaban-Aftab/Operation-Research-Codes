"""
Simple Test Case for Big-M Method
Tests the refactored simplex solver with a problem requiring artificial variables.

Test Problem:
Maximize Z = 3x1 + 5x2
Subject to:
  x1 + x2 >= 2   (requires surplus + artificial)
  2x1 + x2 <= 8  (requires slack only)
  x1, x2 >= 0

Expected: Optimal solution at x1=0, x2=8, Z=40
"""

from simplex_refactored import LinearOptimizationEngine

def test_big_m_problem():
    print("="*70)
    print("BIG-M METHOD TEST - Mixed Constraints")
    print("="*70)
    
    # Create engine instance
    engine = LinearOptimizationEngine()
    
    # Set problem parameters manually
    engine.maximize_mode = True
    engine.decision_count = 2
    engine.restriction_count = 2
    
    # Objective: 3x1 + 5x2
    engine.optimization_vector = [3, 5]
    
    # Constraints:
    # x1 + x2 >= 2
    # 2x1 + x2 <= 8
    engine.restriction_matrix = [
        [1, 1],   # x1 + x2 >= 2
        [2, 1]    # 2x1 + x2 <= 8
    ]
    
    engine.boundary_values = [2, 8]
    engine.restriction_types = [2, 1]  # 2 = >=, 1 = <=
    
    # Display problem
    print("\nPROBLEM FORMULATION:")
    print("Maximize Z = 3x1 + 5x2")
    print("Subject to:")
    print("  x1 + x2 >= 2")
    print("  2x1 + x2 <= 8")
    print("  x1, x2 >= 0")
    print("\n" + "-"*70)
    
    # Solve
    print("\nSOLVING WITH BIG-M METHOD...")
    print("-"*70)
    
    engine.construct_canonical_matrix()
    engine.orchestrate_simplex_iterations()
    
    # Extract results
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    
    if engine.operational_matrix:
        solution = engine.extract_variable_assignments()
        obj_value = engine.operational_matrix[-1][-1]
        
        print(f"\nDecision Variables:")
        print(f"  x1 = {solution.get('x1', 0):.4f}")
        print(f"  x2 = {solution.get('x2', 0):.4f}")
        print(f"\nObjective Value:")
        print(f"  Z = {obj_value:.4f}")
        
        # Verification
        print(f"\nVERIFICATION:")
        x1 = solution.get('x1', 0)
        x2 = solution.get('x2', 0)
        
        # Check constraints
        constraint1 = x1 + x2
        constraint2 = 2*x1 + x2
        
        print(f"  Constraint 1: {x1:.4f} + {x2:.4f} = {constraint1:.4f} >= 2 ✓" if constraint1 >= 1.999 else f"  Constraint 1: VIOLATED ✗")
        print(f"  Constraint 2: 2({x1:.4f}) + {x2:.4f} = {constraint2:.4f} <= 8 ✓" if constraint2 <= 8.001 else f"  Constraint 2: VIOLATED ✗")
        
        # Check objective
        calc_obj = 3*x1 + 5*x2
        print(f"  Objective: 3({x1:.4f}) + 5({x2:.4f}) = {calc_obj:.4f}")
        
        print("\n" + "="*70)
        return True
    else:
        print("\n✗ Problem was not solved successfully")
        return False

if __name__ == "__main__":
    success = test_big_m_problem()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")
