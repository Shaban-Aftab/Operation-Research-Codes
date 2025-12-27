"""
Check LP5 constraint satisfaction manually
"""

x1, x2 = 4.0, 0.83

print("LP5 Solution: x1=4.0, x2=0.83")
print("\nChecking original constraints:")
print(f"  x1 + x2 = {x1 + x2} <= 5? {x1 + x2 <= 5}")
print(f"  10x1 + 6x2 = {10*x1 + 6*x2} <= 45? {10*x1 + 6*x2 <= 45}")
print(f"  x1 = {x1} >= 4? {x1 >= 4}")
print(f"  x2 = {x2} >= 1? {x2 >= 1}")

print("\nChecking converted constraints (>= flipped to <=):")
print(f"  x1 + x2 = {x1 + x2} <= 5? {x1 + x2 <= 5}")
print(f"  10x1 + 6x2 = {10*x1 + 6*x2} <= 45? {10*x1 + 6*x2 <= 45}")
print(f"  -x1 = {-x1} <= -4? {-x1 <= -4}")  # x1 >= 4 becomes -x1 <= -4
print(f"  -x2 = {-x2} <= -1? {-x2 <= -1}")  # x2 >= 1 becomes -x2 <= -1

if x1 >= 4 and x2 >= 1:
    print("\n✓ Solution satisfies ALL constraints")
else:
    print("\n✗ Solution VIOLATES constraints!")
    print("  The problem should be INFEASIBLE")
    print("\n  Let's check feasibility manually:")
    print("  If x1 >= 4 and x2 >= 1:")
    print("    Then x1 + x2 >= 5")
    print("    But x1 + x2 <= 5")
    print("    So x1 + x2 = 5 exactly")
    print("    This means x1=4, x2=1")
    print("    Check: 10(4) + 6(1) = 46 > 45")
    print("    VIOLATES second constraint!")
    print("\n  Therefore LP5 should indeed be INFEASIBLE")
