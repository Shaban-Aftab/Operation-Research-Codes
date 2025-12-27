# STEP-BY-STEP INPUT GUIDE FOR ILP SOLVER
# =========================================
# 
# Problem from your image:
# Max z = 18x1 + 14x2 + 8x3 + 4x4
# Subject to:
#   15x1 + 12x2 + 7x3 + 4x4 + x5 <= 37
#   0 <= xj <= 1, j = 1,2,...,5

"""
When you run: python ilp_solver.py

Follow these steps EXACTLY:
"""

print("""
╔═══════════════════════════════════════════════════════════════════════╗
║           HOW TO INPUT YOUR BINARY PROGRAMMING PROBLEM                ║
╚═══════════════════════════════════════════════════════════════════════╝

PROBLEM:
  Max z = 18x1 + 14x2 + 8x3 + 4x4
  Subject to: 15x1 + 12x2 + 7x3 + 4x4 + x5 <= 37
  0 <= xj <= 1, j = 1,2,...,5

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Select Problem Type
──────────────────────────────────────
Prompt: "Enter choice (1 or 2):"
Type:   1                              ← (Maximization)
Press:  ENTER

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 2: Number of Variables
──────────────────────────────────────
Prompt: "Enter the number of decision variables:"
Type:   5                              ← (x1, x2, x3, x4, x5)
Press:  ENTER

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 3: Number of Constraints
──────────────────────────────────────
Prompt: "Enter the number of constraints:"
Type:   1                              ← (Only one constraint)
Press:  ENTER

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 4: Objective Function Coefficients
──────────────────────────────────────
Prompt: "Coefficient of x1:"
Type:   18                             ← (coefficient of x1)
Press:  ENTER

Prompt: "Coefficient of x2:"
Type:   14                             ← (coefficient of x2)
Press:  ENTER

Prompt: "Coefficient of x3:"
Type:   8                              ← (coefficient of x3)
Press:  ENTER

Prompt: "Coefficient of x4:"
Type:   4                              ← (coefficient of x4)
Press:  ENTER

Prompt: "Coefficient of x5:"
Type:   0                              ← (x5 not in objective)
Press:  ENTER

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 5: Constraint Coefficients
──────────────────────────────────────
For the constraint: 15x1 + 12x2 + 7x3 + 4x4 + x5 <= 37

Prompt: "Coefficient of x1:"
Type:   15                             ← (coefficient of x1)
Press:  ENTER

Prompt: "Coefficient of x2:"
Type:   12                             ← (coefficient of x2)
Press:  ENTER

Prompt: "Coefficient of x3:"
Type:   7                              ← (coefficient of x3)
Press:  ENTER

Prompt: "Coefficient of x4:"
Type:   4                              ← (coefficient of x4)
Press:  ENTER

Prompt: "Coefficient of x5:"
Type:   1                              ← (coefficient of x5)
Press:  ENTER

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 6: Constraint Type
──────────────────────────────────────
Prompt: "Constraint type (1=<=, 2=>=, 3==, 4=<, 5=>):"
Type:   1                              ← (<= constraint)
Press:  ENTER

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 7: Right-Hand Side Value
──────────────────────────────────────
Prompt: "Right-hand side (RHS) value:"
Type:   37                             ← (RHS = 37)
Press:  ENTER

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 8: Integer Variables
──────────────────────────────────────
Prompt: "Enter choice (1 or 2):"
Type:   1                              ← (All variables are integers)
Press:  ENTER

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 9: Binary Variables (IMPORTANT!)
──────────────────────────────────────
Prompt: "Enter variable numbers (1-5) separated by commas..."
Type:   1,2,3,4,5                      ← (All are binary: 0 or 1)
Press:  ENTER

NOTE: This is CRITICAL for your problem! It enforces 0 <= xj <= 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 10: Number of Solutions
──────────────────────────────────────
Prompt: "How many top solutions to display? (default=1):"
Type:   [just press ENTER]             ← (default = 1 solution)
Press:  ENTER

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 11: Start Solving
──────────────────────────────────────
Prompt: "Press ENTER to solve..."
Press:  ENTER                          ← (Start solving!)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXPECTED RESULT:
  x1 = 1, x2 = 1, x3 = 1, x4 = 0, x5 = 0
  Maximum Z = 40

╔═══════════════════════════════════════════════════════════════════════╗
║                         QUICK REFERENCE                               ║
╚═══════════════════════════════════════════════════════════════════════╝

Just copy and paste these numbers in order:

1        ← Maximization
5        ← 5 variables
1        ← 1 constraint
18       ← x1 coefficient in objective
14       ← x2 coefficient in objective
8        ← x3 coefficient in objective
4        ← x4 coefficient in objective
0        ← x5 coefficient in objective
15       ← x1 coefficient in constraint
12       ← x2 coefficient in constraint
7        ← x3 coefficient in constraint
4        ← x4 coefficient in constraint
1        ← x5 coefficient in constraint
1        ← Constraint type (<=)
37       ← RHS value
1        ← All variables are integers
1,2,3,4,5  ← All variables are binary (0/1)
[ENTER]  ← Use default (1 solution)
[ENTER]  ← Start solving

""")

print("\n" + "="*70)
print("TIP: Just copy each number/value above and paste when prompted!")
print("="*70)
