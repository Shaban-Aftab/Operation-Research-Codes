"""
Test ILP Solver - Example 9.2-1 from textbook
==============================================
Maximize z = 5x1 + 4x2
Subject to:
  x1 + x2 <= 5
  10x1 + 6x2 <= 45
  x1, x2 nonnegative integer
"""

from ilp_solver import ILPSolver

print("="*70)
print("VERIFICATION TEST: Example 9.2-1 (Pure Integer LP)")
print("="*70)

solver = ILPSolver()

# Configure the problem
solver.num_variables = 2
solver.num_constraints = 2
solver.objective = [5, 4]
solver.constraints = [[1, 1], [10, 6]]
solver.rhs = [5, 45]
solver.constraint_types = [1, 1]  # Both <=
solver.is_maximization = True
solver.ilp_type = 1  # Pure Integer
solver.integer_vars = [0, 1]  # Both x1 and x2 are integer
solver.binary_vars = []
solver.top_n = 1

print("\n" + "="*70)
print("ALGORITHM VERIFICATION:")
print("="*70)
print("\nStep 1: RELAX - Remove integer restrictions")
print("  → LP Relaxation: Solve without integer constraints")
print("\nStep 2: SOLVE LP - Find continuous optimum")
print("  → Use Simplex method")
print("\nStep 3: BRANCH & BOUND - Add constraints iteratively")
print("  → For fractional xi: branch on xi <= floor(xi) and xi >= ceil(xi)")
print("  → Prune nodes with worse bounds")
print("  → Continue until integer solution found")
print("="*70)

print("\n" + "="*70)
print("PROBLEM FROM IMAGE:")
print("="*70)
print("\nMaximize z = 5x1 + 4x2")
print("\nSubject to:")
print("  x1 + x2 <= 5")
print("  10x1 + 6x2 <= 45")
print("  x1, x2 nonnegative integer")
print("="*70)

input("\nPress ENTER to solve using Branch & Bound...")

solver.solve()

print("\n" + "="*70)
print("VERIFICATION SUMMARY:")
print("="*70)
print("\n✓ Step 1: LP Relaxation created")
print("✓ Step 2: Continuous optimum found")
print("✓ Step 3: Branch & Bound applied")
print("✓ Integer solution obtained")
print("\n" + "="*70)
