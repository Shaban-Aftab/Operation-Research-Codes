"""
Debug ILP - Trace constraint handling
"""

from ilp_solver import ILPSolver

solver = ILPSolver()
solver.num_variables = 2
solver.num_constraints = 2
solver.objective = [5, 4]
solver.constraints = [[1, 1], [10, 6]]
solver.rhs = [5, 45]
solver.constraint_types = [1, 1]
solver.is_maximization = True
solver.ilp_type = 1
solver.integer_vars = [0, 1]
solver.binary_vars = []
solver.top_n = 1

print("Testing LP4: x1 >= 4, x2 <= 0")
print("Expected: x1=4.5, x2=0, z=22.5")

# Simulate LP4 constraints
extra = [
    ([1, 0], 4, 2),  # x1 >= 4
    ([0, 1], 0, 1)   # x2 <= 0
]

solution, obj = solver.solve_subproblem(extra)
if solution:
    print(f"Result: x1={solution['x1']:.2f}, x2={solution['x2']:.2f}, z={obj:.2f}")
else:
    print("Result: INFEASIBLE")

print("\nTesting LP5: x1 >= 4, x2 >= 1")
print("Expected: INFEASIBLE")

extra = [
    ([1, 0], 4, 2),  # x1 >= 4
    ([0, 1], 1, 2)   # x2 >= 1
]

solution, obj = solver.solve_subproblem(extra)
if solution:
    print(f"Result: x1={solution['x1']:.2f}, x2={solution['x2']:.2f}, z={obj:.2f}")
    print("ERROR: Should be infeasible!")
else:
    print("Result: INFEASIBLE ✓")
