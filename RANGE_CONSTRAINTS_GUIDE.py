# HOW TO ADD RANGE CONSTRAINTS MANUALLY
# =======================================
# 
# For: 0 ≤ xⱼ ≤ 1, j = 1,2,...,5

print("""
╔═══════════════════════════════════════════════════════════════════════╗
║            HOW TO INPUT RANGE CONSTRAINTS MANUALLY                    ║
╚═══════════════════════════════════════════════════════════════════════╝

PROBLEM:
  Max z = 18x1 + 14x2 + 8x3 + 4x4
  Subject to:
    15x1 + 12x2 + 7x3 + 4x4 + x5 <= 37
    0 <= xj <= 1, j = 1,2,...,5

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

UNDERSTANDING THE RANGE CONSTRAINT:
───────────────────────────────────────────────────────────────────────

0 ≤ xⱼ ≤ 1  means TWO things:

1. Lower bound:  xⱼ ≥ 0  ← AUTOMATIC (all variables non-negative by default)
2. Upper bound:  xⱼ ≤ 1  ← Must add as constraints!

So you need to add 5 UPPER BOUND CONSTRAINTS:
  x1 <= 1
  x2 <= 1
  x3 <= 1
  x4 <= 1
  x5 <= 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

METHOD 1: Use Binary Variables Feature (RECOMMENDED)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is EASIER! The solver automatically adds x ≤ 1 constraints.

Number of constraints: 1              ← (Only the main constraint)
...
Binary variables: 1,2,3,4,5          ← (Automatically adds 0 ≤ xⱼ ≤ 1)

✓ This is what I showed you before!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

METHOD 2: Add Upper Bounds as Manual Constraints
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type this when running python ilp_solver.py:

STEP 1: Select Problem Type
────────────────────────────
Enter choice (1 or 2): 1                 ← Maximization

STEP 2: Variables & Constraints
────────────────────────────────
Number of decision variables: 5          ← 5 variables
Number of constraints: 6                 ← 1 main + 5 upper bounds

STEP 3: Objective Function
────────────────────────────
Coefficient of x1: 18
Coefficient of x2: 14
Coefficient of x3: 8
Coefficient of x4: 4
Coefficient of x5: 0

STEP 4: CONSTRAINT 1 (Main constraint)
────────────────────────────────────────
  Coefficient of x1: 15
  Coefficient of x2: 12
  Coefficient of x3: 7
  Coefficient of x4: 4
  Coefficient of x5: 1
  Constraint type: 1                     ← <=
  RHS value: 37

STEP 5: CONSTRAINT 2 (x1 <= 1)
────────────────────────────────────────
  Coefficient of x1: 1                   ← 1*x1
  Coefficient of x2: 0                   ← 0*x2
  Coefficient of x3: 0                   ← 0*x3
  Coefficient of x4: 0                   ← 0*x4
  Coefficient of x5: 0                   ← 0*x5
  Constraint type: 1                     ← <=
  RHS value: 1                           ← x1 <= 1

STEP 6: CONSTRAINT 3 (x2 <= 1)
────────────────────────────────────────
  Coefficient of x1: 0
  Coefficient of x2: 1                   ← 1*x2
  Coefficient of x3: 0
  Coefficient of x4: 0
  Coefficient of x5: 0
  Constraint type: 1                     ← <=
  RHS value: 1                           ← x2 <= 1

STEP 7: CONSTRAINT 4 (x3 <= 1)
────────────────────────────────────────
  Coefficient of x1: 0
  Coefficient of x2: 0
  Coefficient of x3: 1                   ← 1*x3
  Coefficient of x4: 0
  Coefficient of x5: 0
  Constraint type: 1                     ← <=
  RHS value: 1                           ← x3 <= 1

STEP 8: CONSTRAINT 5 (x4 <= 1)
────────────────────────────────────────
  Coefficient of x1: 0
  Coefficient of x2: 0
  Coefficient of x3: 0
  Coefficient of x4: 1                   ← 1*x4
  Coefficient of x5: 0
  Constraint type: 1                     ← <=
  RHS value: 1                           ← x4 <= 1

STEP 9: CONSTRAINT 6 (x5 <= 1)
────────────────────────────────────────
  Coefficient of x1: 0
  Coefficient of x2: 0
  Coefficient of x3: 0
  Coefficient of x4: 0
  Coefficient of x5: 1                   ← 1*x5
  Constraint type: 1                     ← <=
  RHS value: 1                           ← x5 <= 1

STEP 10: Integer Variables
────────────────────────────
Enter choice (1 or 2): 1                 ← All integers

STEP 11: Binary Variables
────────────────────────────
[Press ENTER to skip]                    ← Skip (already added manually)

STEP 12: Solutions
────────────────────────────
[Press ENTER]                            ← 1 solution

STEP 13: Solve
────────────────────────────
[Press ENTER]                            ← Solve!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUICK COPY-PASTE VALUES FOR METHOD 2:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1        ← Maximization
5        ← 5 variables
6        ← 6 constraints (1 main + 5 upper bounds)
18       ← x1 coef in objective
14       ← x2 coef in objective
8        ← x3 coef in objective
4        ← x4 coef in objective
0        ← x5 coef in objective

--- CONSTRAINT 1: 15x1 + 12x2 + 7x3 + 4x4 + x5 <= 37 ---
15, 12, 7, 4, 1, 1, 37

--- CONSTRAINT 2: x1 <= 1 ---
1, 0, 0, 0, 0, 1, 1

--- CONSTRAINT 3: x2 <= 1 ---
0, 1, 0, 0, 0, 1, 1

--- CONSTRAINT 4: x3 <= 1 ---
0, 0, 1, 0, 0, 1, 1

--- CONSTRAINT 5: x4 <= 1 ---
0, 0, 0, 1, 0, 1, 1

--- CONSTRAINT 6: x5 <= 1 ---
0, 0, 0, 0, 1, 1, 1

1        ← All integers
[ENTER]  ← Skip binary (already constrained)
[ENTER]  ← 1 solution
[ENTER]  ← Solve

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECOMMENDATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👉 USE METHOD 1 (Binary Variables Feature) - It's much easier!
   Just set "Binary variables: 1,2,3,4,5"

Method 2 is only if you want to understand what's happening behind the scenes.

""")

print("\n" + "="*70)
print("TIP: For 0 ≤ xⱼ ≤ 1, the easiest way is to use binary variables!")
print("="*70)
