"""
Deep debug - Check what constraints are being passed
"""

from ilp_solver import SimplexSolver

print("DEEP DEBUG: Testing Simplex Solver Directly")
print("="*70)

# Test LP4: x1 >= 4, x2 <= 0
print("\nTest LP4: x1 >= 4, x2 <= 0")
print("Constraints:")
print("  x1 + x2 <= 5")
print("  10x1 + 6x2 <= 45")
print("  x1 >= 4")
print("  x2 <= 0")
print("\nExpected: x1=4.5, x2=0, z=22.5")

constraints = [
    [1, 1],      # x1 + x2 <= 5
    [10, 6],     # 10x1 + 6x2 <= 45
    [1, 0],      # x1 >= 4
    [0, 1]       # x2 <= 0
]
rhs = [5, 45, 4, 0]
types = [1, 1, 2, 1]  # <=, <=, >=, <=
objective = [5, 4]

solver = SimplexSolver(objective, constraints, rhs, types, is_maximization=True)
solution, obj = solver.solve()

if solution:
    print(f"\nResult: x1={solution['x1']:.2f}, x2={solution['x2']:.2f}, z={obj:.2f}")
    if abs(solution['x1'] - 4.5) < 0.1 and abs(solution['x2'] - 0) < 0.1:
        print("✓ CORRECT!")
    else:
        print("✗ WRONG!")
else:
    print("\nResult: INFEASIBLE")
    print("✗ WRONG - Should be feasible!")

print("\n" + "="*70)
print("\nTest LP5: x1 >= 4, x2 >= 1")
print("Constraints:")
print("  x1 + x2 <= 5")
print("  10x1 + 6x2 <= 45") 
print("  x1 >= 4")
print("  x2 >= 1")
print("\nExpected: INFEASIBLE")

constraints = [
    [1, 1],      # x1 + x2 <= 5
    [10, 6],     # 10x1 + 6x2 <= 45
    [1, 0],      # x1 >= 4
    [0,1]       # x2 >= 1
]
rhs = [5, 45, 4, 1]
types = [1, 1, 2, 2]  # <=, <=, >=, >=

solver = SimplexSolver(objective, constraints, rhs, types, is_maximization=True)
solution, obj = solver.solve()

if solution:
    print(f"\nResult: x1={solution['x1']:.2f}, x2={solution['x2']:.2f}, z={obj:.2f}")
    # Check if feasible
    x1, x2 = solution['x1'], solution['x2']
    if x1 + x2 <= 5.01 and 10*x1 + 6*x2 <= 45.01 and x1 >= 4 and x2 >= 1:
        print("Constraints satisfied - but SHOULD BE INFEASIBLE!")
        print(f"  x1 + x2 = {x1 + x2} <= 5? YES")
        print(f"  10x1 + 6x2 = {10*x1 + 6*x2} <= 45? YES")
        print(f"  x1 = {x1} >= 4? YES")  
        print(f"  x2 = {x2} >= 1? YES")
        print("\nWait - this is actually FEASIBLE! Let me re-check the image...")
    else:
        print("Constraints violated - solver gave wrong answer")
else:
    print("\nResult: INFEASIBLE")
    print("✓ CORRECT!")
