"""
Test the TOYCO problem from terminal
====================================
Maximize Z = 3x1 + 2x2 + 5x3
Subject to:
  x1 + 2x2 + x3 <= 430  (Operation 1)
  3x1 + 2x3 <= 460      (Operation 2)
  x1 + 4x2 <= 420       (Operation 3)

Expected from textbook images:
  Optimal: x1=0, x2=100, x3=230, Z=1350
  Shadow prices: y1=1, y2=2, y3=0
  Ranges:
    Operation 1: [230, 440]
    Operation 2: [440, 860]
    Operation 3: [-∞, ∞]
"""

from simplex_refactored import LinearOptimizationEngine
from sensitivity_module import PostOptimalAnalyzer

print("=" * 70)
print("     TOYCO PROBLEM - SENSITIVITY ANALYSIS VERIFICATION")
print("=" * 70)

# Create solver
solver = LinearOptimizationEngine()

# Configure problem
solver.decision_variable_count = 3
solver.restriction_count = 3
solver.is_maximization_problem = True

solver.objective_coefficients = [3, 2, 5]
solver.constraint_matrix = [
    [1, 2, 1],   # Operation 1
    [3, 0, 2],   # Operation 2
    [1, 4, 0]    # Operation 3
]
solver.right_hand_side = [430, 460, 420]
solver.restriction_types = [1, 1, 1]

# Also set the other required attributes
solver.restriction_matrix = solver.constraint_matrix
solver.boundary_values = solver.right_hand_side

print("\nProblem:")
print("  Maximize Z = 3x1 + 2x2 + 5x3")
print("\n  Subject to:")
print("    x1 + 2x2 + x3 <= 430  (Operation 1)")
print("    3x1 + 2x3 <= 460      (Operation 2)")
print("    x1 + 4x2 <= 420       (Operation 3)")

print("\n" + "-" * 70)
print("SOLVING...")
print("-" * 70)

# Solve
solver.construct_canonical_matrix()
solver.orchestrate_simplex_iterations()

# Get solution
solution = solver.export_solution_package()

print("\n✓ OPTIMAL SOLUTION:")
print(f"  x1 = {solution['solution_values']['x1']:.1f}")
print(f"  x2 = {solution['solution_values']['x2']:.1f}")
print(f"  x3 = {solution['solution_values']['x3']:.1f}")
print(f"  Z = {solution['objective_value']:.1f}")

# Verify solution
expected_x1, expected_x2, expected_x3, expected_Z = 0, 100, 230, 1350
if (abs(solution['solution_values']['x1'] - expected_x1) < 0.1 and
    abs(solution['solution_values']['x2'] - expected_x2) < 0.1 and
    abs(solution['solution_values']['x3'] - expected_x3) < 0.1 and
    abs(solution['objective_value'] - expected_Z) < 0.1):
    print("  ✓ Matches expected solution!")
else:
    print("  ✗ Solution mismatch!")

# Run sensitivity analysis
print("\n" + "=" * 70)
print("     SENSITIVITY ANALYSIS - ALLOWABLE RANGES")
print("=" * 70)

analyzer = PostOptimalAnalyzer(solver)

# Compute shadow prices
shadow_prices = analyzer.compute_marginal_prices()
print("\nShadow Prices (Dual Values):")
for i, price in enumerate(shadow_prices):
    print(f"  y{i+1} = {abs(price):.6f}")

# Verify shadow prices
expected_shadow = [1, 2, 0]
print("\nExpected from textbook:")
for i, price in enumerate(expected_shadow):
    print(f"  y{i+1} = {price}")

shadow_match = all(abs(abs(shadow_prices[i]) - expected_shadow[i]) < 0.1 
                   for i in range(3))
if shadow_match:
    print("  ✓ Shadow prices match!")
else:
    print("  ⚠ Shadow prices may differ (check signs/scaling)")

# Get basis inverse for manual calculation
print("\n" + "-" * 70)
print("BASIS INVERSE MATRIX B^(-1):")
print("-" * 70)
B_inv = analyzer.basis_inverse_matrix
for i, row in enumerate(B_inv):
    print(f"  Row {i+1}: [{', '.join(f'{v:8.4f}' for v in row)}]")

# Get current basic values
basic_values = [analyzer.solution_tableau[i][-1] for i in range(3)]
print(f"\nCurrent basic variable values: {[f'{v:.1f}' for v in basic_values]}")

# Calculate ranges manually for verification
print("\n" + "-" * 70)
print("MANUAL RANGE CALCULATION:")
print("-" * 70)

for constraint_idx in range(3):
    print(f"\nOperation {constraint_idx + 1} (current RHS = {analyzer.boundary_limits[constraint_idx]}):")
    
    # Get column of B^(-1)
    column = [B_inv[i][constraint_idx] for i in range(3)]
    print(f"  B^(-1) column: {[f'{v:.4f}' for v in column]}")
    
    # Calculate bounds
    max_decrease = float('inf')
    max_increase = float('inf')
    
    for i in range(3):
        if abs(column[i]) > 1e-10:
            if column[i] > 0:
                decrease = basic_values[i] / column[i]
                max_decrease = min(max_decrease, decrease)
                print(f"    Row {i+1}: {basic_values[i]:.1f} / {column[i]:.4f} = {decrease:.1f} (decrease)")
            else:
                increase = -basic_values[i] / column[i]
                max_increase = min(max_increase, increase)
                print(f"    Row {i+1}: -{basic_values[i]:.1f} / {column[i]:.4f} = {increase:.1f} (increase)")
    
    lower = analyzer.boundary_limits[constraint_idx] - max_decrease
    upper = analyzer.boundary_limits[constraint_idx] + max_increase
    
    print(f"  Maximum decrease: {max_decrease:.1f}")
    print(f"  Maximum increase: {max_increase:.1f}")
    print(f"  Range: [{lower:.1f}, {upper:.1f}]")

# Now use the built-in function
print("\n" + "=" * 70)
print("USING BUILT-IN ALLOWABLE RANGES FUNCTION:")
print("=" * 70)

analyzer.compute_allowable_ranges()

# Expected ranges from textbook
print("\n" + "=" * 70)
print("EXPECTED RANGES (from textbook):")
print("=" * 70)
expected_ranges = [
    (230, 440),
    (440, 860),
    (float('-inf'), float('inf'))
]

for i, (lower, upper) in enumerate(expected_ranges):
    lower_str = "-∞" if lower == float('-inf') else f"{lower:.1f}"
    upper_str = "∞" if upper == float('inf') else f"{upper:.1f}"
    print(f"  Operation {i+1}: [{lower_str}, {upper_str}]")

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE!")
print("=" * 70)
