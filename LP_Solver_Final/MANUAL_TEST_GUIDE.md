# MANUAL TESTING GUIDE FOR ALL 5 SENSITIVITY ANALYSIS TYPES

## TEST SETUP

**Test Problem:**

```
Maximize Z = 2x1 + 3x2

Subject to:
  -x1 + x2 <= 4
  x1 + x2 <= 6
  3x1 + x2 <= 9
  x1, x2 >= 0
```

**Expected Optimal Solution:**

- x1 = 1.5
- x2 = 4.5
- Z = 16.5

---

## HOW TO RUN TESTS

```bash
cd "d:\Fast NUCES CFD\Semester VII\Operation Research\Code\LP_Solver_Final"
python integrated_solver.py
```

### Step 1: Solve the Problem

1. Select option **1** (Simplex Method)
2. Enter the problem:

   - Maximize: **1**
   - Variables: **2**
   - Constraints: **3**

   **Objective:** 2, 3

   **Constraint 1:** -1, 1, type 1, RHS 4
   **Constraint 2:** 1, 1, type 1, RHS 6
   **Constraint 3:** 3, 1, type 1, RHS 9

3. Verify optimal solution matches expected values above

---

## TEST 1: RHS Perturbation Analysis

**What to Test:** Change Resource 2 from 6 to 8

### Steps:

1. After solving, choose **Sensitivity Analysis**
2. Select **1. Changes in RHS / Resource Availability**
3. Select constraint **2** (x1 + x2 <= 6)
4. Enter new RHS: **8**

### Expected Results:

- **Shadow price** for constraint 2 should be displayed
- New objective = Old Z + (Δb × shadow price)
- Should show: ΔZ = 2 × (shadow_price_2)
- New Z = 16.5 + ΔZ
- Solution remains FEASIBLE

### Manual Verification:

- Shadow price y2 ≈ 1.5 (verify from solver)
- ΔZ = (8-6) × 1.5 = 3.0
- New Z = 16.5 + 3.0 = 19.5 ✓

---

## TEST 2: Objective Coefficient Variation

**What to Test:** Change c1 from 2 to 5

### Steps:

1. Select **2. Changes in Objective Function Coefficients**
2. Select variable **1** (x1)
3. Enter new coefficient: **5**

### Expected Results:

- Should identify x1 as BASIC
- Calculate new objective
- ΔZ = Δc × x1_value = (5-2) × 1.5 = 4.5
- New Z = 16.5 + 4.5 = 21.0

### Manual Verification:

Since x1 is basic at value 1.5:

- New Z = 5(1.5) + 3(4.5) = 7.5 + 13.5 = 21.0 ✓

---

## TEST 3: Constraint Coefficient Change

**What to Test:** Change a[2,1] from 1 to 2

### Steps:

1. Select **3. Changes in Constraint Coefficients**
2. Select constraint **2**
3. Select variable **1** (x1)
4. Enter new coefficient: **2**

### Expected Results:

- Should identify x1 as BASIC
- Warn that this affects a basic variable
- Recommend re-optimization
- Solution values unchanged (but may become infeasible)

### Manual Verification:

Check if 2(1.5) + 1(4.5) = 7.5 ≤ 6?

- NO! 7.5 > 6, so solution becomes infeasible
- Must re-optimize ✓

---

## TEST 4: New Constraint Addition

**What to Test:** Add constraint x1 + x2 <= 10

### Steps:

1. Select **4. Addition of a New Constraint**
2. Enter coefficients: **1, 1**
3. Select type: **1** (<=)
4. Enter RHS: **10**

### Expected Results:

- Evaluate at current solution: 1.5 + 4.5 = 6
- Check: 6 ≤ 10? YES
- Constraint is REDUNDANT
- Current solution remains optimal
- Z unchanged = 16.5

### Manual Verification:

LHS = 1.5 + 4.5 = 6.0 ≤ 10 ✓ SATISFIED

---

### Test 4B: Active Constraint

**What to Test:** Add constraint x1 + x2 <= 5

### Steps:

1. Select **4. Addition of a New Constraint**
2. Enter coefficients: **1, 1**
3. Select type: **1** (<=)
4. Enter RHS: **5**

### Expected Results:

- Evaluate: 1.5 + 4.5 = 6
- Check: 6 ≤ 5? NO
- Constraint VIOLATED
- Must re-optimize
- New Z will be LOWER

### Manual Verification:

LHS = 6.0 > 5.0 ✗ VIOLATED - needs re-optimization ✓

---

## TEST 5: New Variable Addition

**What to Test:** Add variable x3 with c3=4, column [1, 2, 1]

### Steps:

1. Select **5. Addition of a New Decision Variable**
2. Enter objective coefficient: **4**
3. Enter constraint coefficients:
   - Constraint 1: **1**
   - Constraint 2: **2**
   - Constraint 3: **1**

### Expected Results:

**Calculate manually first:**

1. Get basis costs (from optimal tableau):

   - If basis = [x2, s2, x1], costs CB = [3, 0, 2]

2. Calculate Zj:

   - Zj = 3(1) + 0(2) + 2(1) = 3 + 0 + 2 = 5

3. Reduced cost:

   - Zj - cj = 5 - 4 = 1 > 0

4. For MAX: Since reduced cost > 0, variable should NOT enter

### Expected Solver Output:

- Zj = 5.00
- cj = 4.00
- Reduced cost = 1.00
- **Current solution remains OPTIMAL**
- x3 would be 0 (non-basic)

---

### Test 5B: Attractive Variable

**What to Test:** Add variable x3 with c3=10, column [1, 1, 1]

### Expected Results:

1. Zj = 3(1) + 0(1) + 2(1) = 5
2. Reduced cost = 5 - 10 = -5 < 0
3. For MAX: Since reduced cost < 0, **variable SHOULD enter**
4. Need to re-optimize

---

## VERIFICATION CHECKLIST

Run through each test and mark:

- [ ] TEST 1: RHS change - Shadow price calculated correctly
- [ ] TEST 1: New objective value computed correctly
- [ ] TEST 2: Basic variable identified
- [ ] TEST 2: New Z = Old Z + Δc × x_value
- [ ] TEST 3: Basic variable warning shown
- [ ] TEST 3: Re-optimization recommended
- [ ] TEST 4A: Redundant constraint identified
- [ ] TEST 4B: Violated constraint detected
- [ ] TEST 5A: Reduced cost positive → don't add
- [ ] TEST 5B: Reduced cost negative → should add

---

## QUICK TEST COMMAND

```bash
python test_sensitivity_simple.py
```

This verifies all methods are implemented.

---

## EXAM TIPS

### What each test shows you:

1. **RHS Test** → How to use shadow prices
2. **Objective Test** → Basic vs non-basic impact
3. **Constraint Coef** → When re-optimization needed
4. **New Constraint** → Redundant vs active distinction
5. **New Variable** → Reduced cost interpretation

### Remember:

- Shadow price = marginal value of resource
- Basic variable change → affects Z directly
- Non-basic variable change → check reduced cost
- New constraint → check satisfaction at current solution
- New variable → calculate Zj - cj

All formulas and calculations are shown step-by-step by the solver!

Good luck! 🎓
