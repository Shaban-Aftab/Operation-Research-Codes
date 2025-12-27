"""
Test Maximization Transportation Problem
========================================
Test the maximization solver with profit maximization example
"""

import sys
sys.path.append('.')

from maximization import MaximizationSolver

print("="*70)
print("TEST: Maximization Transportation Problem")
print("="*70)
print("\nExample: Maximize profit instead of minimize cost")

# Create solver
solver = MaximizationSolver()

# Configure problem (from the uploaded image example)
solver.num_sources = 3
solver.num_destinations = 4
solver.source_names = ['X', 'Y', 'Z']
solver.dest_names = ['1', '2', '3', '4']
solver.supply = [200.0, 500.0, 300.0]
solver.demand = [180.0, 320.0, 100.0, 400.0]
solver.cost_matrix = [  # These are PROFITS to maximize
    [12.0, 18.0, 6.0, 25.0],
    [8.0, 7.0, 10.0, 18.0],
    [14.0, 3.0, 11.0, 20.0]
]

print("\nOriginal Problem (MAXIMIZE PROFIT):")
solver.display_problem_summary()

# Balance
solver.balance_problem()

# Solve
print("\n>>> Solving Maximization Problem...")
result = solver.solve_maximization()

if result:
    print("\n" + "="*70)
    print("✓ TEST PASSED - Maximization problem solved!")
    print("="*70)
else:
    print("\n✗ TEST FAILED")
