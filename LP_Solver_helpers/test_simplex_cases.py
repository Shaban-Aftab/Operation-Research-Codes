"""
Test cases for Simplex Method Solver
These test various scenarios to find bugs and edge cases
"""

# Test Case 1: Standard Maximization with >= and = constraints
print("="*70)
print("TEST CASE 1: Maximization with Mixed Constraints")
print("="*70)
print("""
Maximize Z = 3x1 + 5x2
Subject to:
  x1 <= 4
  2x2 <= 12
  3x1 + 2x2 = 18
  x1, x2 >= 0

Expected: x1 = 2, x2 = 6, Z = 36
""")

# Test Case 2: Minimization Problem
print("\n" + "="*70)
print("TEST CASE 2: Minimization Problem")
print("="*70)
print("""
Minimize Z = 2x1 + 3x2
Subject to:
  x1 + x2 >= 5
  x1 >= 2
  x2 >= 1
  x1, x2 >= 0

Expected: x1 = 2, x2 = 3, Z = 13
""")

# Test Case 3: Degenerate Case (Multiple optimal solutions possible)
print("\n" + "="*70)
print("TEST CASE 3: Degenerate Case")
print("="*70)
print("""
Maximize Z = 3x1 + 3x2
Subject to:
  x1 + x2 <= 4
  x1 <= 2
  x2 <= 3
  x1, x2 >= 0

Expected: Multiple optimal solutions, Z = 12
""")

# Test Case 4: Infeasible Problem
print("\n" + "="*70)
print("TEST CASE 4: Infeasible Problem")
print("="*70)
print("""
Maximize Z = x1 + x2
Subject to:
  x1 + x2 <= 1
  x1 + x2 >= 2
  x1, x2 >= 0

Expected: No feasible solution
""")

# Test Case 5: Complex problem with many variables
print("\n" + "="*70)
print("TEST CASE 5: Complex Problem (3 variables)")
print("="*70)
print("""
Maximize Z = 5x1 + 4x2 + 3x3
Subject to:
  2x1 + 3x2 + x3 <= 5
  4x1 + x2 + 2x3 <= 11
  3x1 + 4x2 + 2x3 <= 8
  x1, x2, x3 >= 0

Expected: Optimal solution exists
""")

# Test Case 6: All equality constraints
print("\n" + "="*70)
print("TEST CASE 6: All Equality Constraints")
print("="*70)
print("""
Maximize Z = 4x1 + 3x2
Subject to:
  2x1 + x2 = 10
  x1 + x2 = 6
  x1, x2 >= 0

Expected: x1 = 4, x2 = 2, Z = 22
""")

print("\n" + "="*70)
print("Use these test cases to validate the solver")
print("="*70)
