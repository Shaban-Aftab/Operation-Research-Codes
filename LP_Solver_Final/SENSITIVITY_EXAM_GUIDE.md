# SENSITIVITY ANALYSIS EXAM GUIDE

===================================

COMPLETE GUIDE FOR ALL 5 TYPES OF SENSITIVITY ANALYSIS

## Problem Setup

Test Problem:

```
Maximize Z = 3x1 + 2x2 + 5x3
Subject to:
  2x1 + 3x2 + x3 <= 100
  x1 + 2x2 + 4x3 <= 80
  3x1 + x2 + 2x3 <= 90
  x1, x2, x3 >= 0
```

---

## TYPE 1: Changes in RHS / Resource Availability

**When to Use:** When resource quantities change  
**Example:** What if Resource 1 changes from 100 to 110?

**Steps:**

1. Select Analysis Option 1
2. Choose the constraint (e.g., Constraint 1)
3. Enter new RHS value (e.g., 110)

**What to Look For:**

- Shadow price (marginal value of resource)
- New objective value
- Feasibility check
- Allowable range for RHS

**Exam Tip:** Shadow price tells you how much Z improves per unit increase in RHS

---

## TYPE 2: Changes in Objective Function Coefficients

**When to Use:** When profit/cost coefficients change  
**Example:** What if profit from x1 changes from 3 to 4?

**Steps:**

1. Select Analysis Option 2
2. Choose the variable (e.g., x1)
3. Enter new coefficient (e.g., 4)

**What to Look For:**

- Is variable basic or non-basic?
- Does basis remain optimal?
- New objective value
- Reduced cost changes

**Exam Tip:**

- Basic variable change: Affects Z directly
- Non-basic variable change: Check if it should enter basis

---

## TYPE 3: Changes in Constraint Coefficients

**When to Use:** When technology coefficients change  
**Example:** What if x1's consumption of Resource 1 changes from 2 to 3?

**Steps:**

1. Select Analysis Option 3
2. Choose the constraint (e.g., Constraint 1)
3. Choose the variable (e.g., x1)
4. Enter new coefficient (e.g., 3)

**What to Look For:**

- Is variable basic or non-basic?
- Impact on feasibility
- Impact on optimality
- Need for re-optimization

**Exam Tip:** If changing coefficient of basic variable, usually need to re-optimize

---

## TYPE 4: Addition of a New Constraint

**When to Use:** When a new restriction is added  
**Example:** Add constraint: x1 + x2 + x3 <= 60

**Steps:**

1. Select Analysis Option 4
2. Enter coefficients for new constraint
   - x1: 1
   - x2: 1
   - x3: 1
3. Enter constraint type (1 for <=)
4. Enter RHS (60)

**What to Look For:**

- Does current solution satisfy new constraint?
- If YES: Constraint is REDUNDANT (no change needed)
- If NO: Constraint is ACTIVE (cuts current solution, need re-optimization)

**Exam Tip:** Calculate LHS at current solution and compare with RHS

**Example Calculation:**
If current solution is x1=10, x2=20, x3=15:

- LHS = 1(10) + 1(20) + 1(15) = 45
- RHS = 60
- Since 45 <= 60, constraint is satisfied = REDUNDANT

---

## TYPE 5: Addition of a New Decision Variable

**When to Use:** When introducing a new product/activity  
**Example:** Add variable x4 with profit coefficient 4

**Steps:**

1. Select Analysis Option 5
2. Enter objective coefficient (e.g., 4)
3. Enter constraint coefficients:
   - Constraint 1: 2
   - Constraint 2: 3
   - Constraint 3: 1

**What to Look For:**

- Calculate reduced cost: Zj - cj
- If reduced cost < 0 (MAX) or > 0 (MIN): Variable SHOULD enter
- If reduced cost >= 0 (MAX) or <= 0 (MIN): Variable stays at 0

**Exam Tip:** Use formula Zj = Σ(CB_i × a_ij)

**Example Calculation:**
If basis costs are [3, 0, 5] and new column is [2, 3, 1]:

- Zj = 3(2) + 0(3) + 5(1) = 6 + 0 + 5 = 11
- cj = 4
- Reduced cost = 11 - 4 = 7 > 0
- For MAX problem: Should NOT enter (current solution optimal)

---

## QUICK REFERENCE TABLE

| Analysis Type      | Key Question       | Satisfies? | Action                             |
| ------------------ | ------------------ | ---------- | ---------------------------------- |
| 1. RHS Change      | Feasible?          | Yes        | Calculate new Z using shadow price |
|                    |                    | No         | Re-optimize (Dual Simplex)         |
| 2. Obj Coef        | Optimal?           | Yes        | Calculate new Z if basic           |
|                    |                    | No         | Re-optimize (Primal Simplex)       |
| 3. Constraint Coef | Basic var?         | Yes        | Re-optimize                        |
|                    |                    | No         | Check impact on reduced cost       |
| 4. New Constraint  | Satisfied?         | Yes        | Redundant (no change)              |
|                    |                    | No         | Re-optimize                        |
| 5. New Variable    | Z_j - c_j optimal? | Yes        | Don't add (stays 0)                |
|                    |                    | No         | Add and re-optimize                |

---

## EXAM STRATEGY

### FORMAT YOU'LL SEE:

"Given the optimal solution x1=10, x2=20, Z=100..."

1. **RHS Problems:** Look for "resource availability increases"  
   → Use shadow prices

2. **Objective Problems:** Look for "profit/cost changes"  
   → Check if variable is basic

3. **Constraint Coef:** Look for "technology/consumption rate changes"  
   → Check basic/non-basic status

4. **New Constraint:** Look for "new requirement added"  
   → Evaluate at current solution

5. **New Variable:** Look for "new product introduced"  
   → Calculate reduced cost

### FORMULAS TO MEMORIZE:

1. **Shadow Price:** ΔZ = Δb × y_i
2. **Objective Change (Basic):** ΔZ = Δc × x_current
3. **Reduced Cost:** Z_j - c_j = Σ(CB_i × a_ij) - c_j
4. **New Constraint:** Σ(a_i × x_i\*) compared with b

### OPTIMALITY CONDITIONS:

**Maximization:**

- Z_j - c_j >= 0 for all variables → OPTIMAL
- Z_j - c_j < 0 for some variable → NOT OPTIMAL

**Minimization:**

- Z_j - c_j <= 0 for all variables → OPTIMAL
- Z_j - c_j > 0 for some variable → NOT OPTIMAL

---

## TESTING COMMANDS

```bash
# Run comprehensive test
python test_sensitivity_comprehensive.py

# Run integrated solver with sensitivity
python integrated_solver.py
# Choose option 3 or 4 for sensitivity analysis
```

---

## PRACTICE PROBLEMS

Use the test problem above and try:

1. **RHS:** Change b1 from 100 to 120
2. **Objective:** Change c2 from 2 to 6
3. **Constraint:** Change a[1,2] from 3 to 5
4. **New Constraint:** Add 2x1 + x2 <= 50
5. **New Variable:** Add x4 with c4=6, column [1, 2, 3]

Work through each one manually first, then verify with the solver!

---

Good luck on your exam! 🎓
