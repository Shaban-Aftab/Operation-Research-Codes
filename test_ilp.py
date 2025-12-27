"""
Test ILP Solver - Mixed Integer Example
========================================
"""

import sys
sys.path.append('.')

print("="*70)
print("TEST: Mixed Integer Linear Programming")
print("="*70)

# Test problem:
# Maximize Z = 3x1 + 2x2
# Subject to:
#   2x1 + x2 <= 10
#   x1 + 2x2 <= 8
#   x1, x2 >= 0
#   x1 integer, x2 continuous

from ilp_solver import ILPSolver

solver = ILPSolver()
solver.num_variables = 2
solver.num_constraints = 2
solver.objective = [3, 2]
solver.constraints = [[2, 1], [1, 2]]
solver.rhs = [10, 8]
solver.constraint_types = [1, 1]  # Both <=
solver.is_maximization = True
solver.ilp_type = 2  # Mixed Integer
solver.integer_vars = [0]  # Only x1 is integer
solver.binary_vars = []
solver.top_n = 1

print("\nProblem: Mixed Integer LP")
print("Maximize Z = 3x1 + 2x2")
print("Subject to:")
print("  2x1 + x2 <= 10")
print("  x1 + 2x2 <= 8")
print("  x1 integer, x2 continuous")

solver.display_problem()

print("\n>>> Solving...")
solver.solve()

print("\n✓ TEST COMPLETE")
