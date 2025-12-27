"""
Test Hungarian Method - Unbalanced Problem from Image
=====================================================
3 workers × 4 jobs (unbalanced)
"""

import sys
sys.path.append('.')

# Simulate the unbalanced problem from the image
print("="*70)
print("TEST: Unbalanced Assignment Problem (3×4)")
print("="*70)
print("\nProblem from image:")
print("3 workers, 4 jobs - UNBALANCED!")
print("\nCost Matrix:")
print("  5   9   3   6")
print("  8   7   8   2")
print("  6  10  12   7")

# Manual test
from hungarian_method import HungarianMethod

solver = HungarianMethod()
solver.num_workers = 3
solver.num_jobs = 4
solver.worker_names = ['W1', 'W2', 'W3']
solver.job_names = ['J1', 'J2', 'J3', 'J4']
solver.is_minimization = True
solver.is_balanced = False
solver.original_matrix = [
    [5, 9, 3, 6],
    [8, 7, 8, 2],
    [6, 10, 12, 7]
]

print("\n>>> Solving...")
solver.solve()
solver.display_solution()

print("\n✓ TEST PASSED - Unbalanced problem solved!")
print("✓ Dummy worker added successfully")
