"""
Test Binary Programming Problem from User's Image
==================================================
Max z = 18x1 + 14x2 + 8x3 + 4x4
Subject to:
  15x1 + 12x2 + 7x3 + 4x4 + x5 <= 37
  0 <= xj <= 1, j = 1,2,...,5
"""

from ilp_solver import ILPSolver

print("="*70)
print("TEST: Binary Programming Problem (5 variables)")
print("="*70)

solver = ILPSolver()

# Configure problem
solver.num_variables = 5
solver.num_constraints = 1
solver.objective = [18, 14, 8, 4, 0]  # x5 has coefficient 0 in objective
solver.constraints = [[15, 12, 7, 4, 1]]
solver.rhs = [37]
solver.constraint_types = [1]  # <=
solver.is_maximization = True
solver.ilp_type = 3  # Binary
solver.integer_vars = [0, 1, 2, 3, 4]  # All are integer
solver.binary_vars = [0, 1, 2, 3, 4]  # All are binary (0/1)
solver.top_n = 1

print("\nProblem:")
print("Max z = 18x1 + 14x2 + 8x3 + 4x4")
print("\nSubject to:")
print("  15x1 + 12x2 + 7x3 + 4x4 + x5 <= 37")
print("  0 <= xj <= 1, j = 1,2,...,5")

solver.display_problem()

input("\n>>> Press ENTER to solve...")
solver.solve()

print("\n✓ TEST COMPLETE")
