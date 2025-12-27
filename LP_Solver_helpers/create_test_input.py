# Test script for automated testing of the refactored simplex solver
# This will test the original problem from the terminal

test_input = """1
2
2
5
4
1
0
1
7
1
-1
1
8
"""

with open('test_input1.txt', 'w') as f:
    f.write(test_input)

print("Test input file created: test_input1.txt")
print("\nTest Case: Original problem from terminal")
print("Maximize Z = 5x1 + 4x2")
print("Subject to:")
print("  x1 <= 7")
print("  x1 - x2 <= 8")
print("\nExpected: UNBOUNDED solution")
