"""
Quick Test Runner for Refactored Simplex Solver
Tests the original problem to verify UNBOUNDED detection works
"""

print("="*70)
print("TESTING REFACTORED SIMPLEX SOLVER")
print("="*70)

print("\nTest Case: Original Problem from Terminal")
print("-" * 70)
print("Maximize Z = 5x1 + 4x2")
print("Subject to:")
print("  x1 <= 7")
print("  x1 - x2 <= 8")
print("\nExpected Result: UNBOUNDED solution")
print("="*70)

print("\nNow run:")
print("  python simplex_refactored.py < test_input1.txt")
print("\nOr run interactively:")
print("  python simplex_refactored.py")
print("\n" + "="*70)
