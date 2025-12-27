# TOYCO ALLOWABLE RANGE - MANUAL VERIFICATION

===============================================

Based on terminal output from your test:

## Optimal Solution (CORRECT ✓)

- x1 = 0
- x2 = 100
- x3 = 230
- Z = 1350

## Basis Inverse Matrix B^(-1)

To verify ranges, we need the final tableau's basis inverse.

From the final tableau in your test:

```
Basis: x2, x3, s3
Basic values: 100,  230, 20
```

The ranges are calculated as follows:

### Operation 1 (current RHS = 430):

Column 1 of B^(-1) tells us how each basic variable changes when b1 changes.

For feasibility: basic_value + Δb₁ × B^(-1)[i,1] ≥ 0

### Operation 2 (current RHS = 460):

Column 2 of B^(-1).

### Operation 3 (current RHS = 420):

Column 3 of B^(-1).

## Expected Ranges (from textbook):

1. Operation 1: [230, 440] (current 430)
2. Operation 2: [440, 860] (current 460)
3. Operation 3: [-∞, ∞] (current 420)

## Shadow Prices (Dual Values):

Expected: y₁=1, y₂=2, y₃=0

These are the negatives of the slack variable coefficients in the objective row:

- y₁ = coefficient of s₁ in Z-row
- y₂ = coefficient of s₂ in Z-row
- y₃ = coefficient of s₃ in Z-row

## TO TEST:

Run: `python integrated_solver.py`

1. Choose option 3 (Simplex + Sensitivity)
2. Enter the TOYCO problem
3. After solving, choose sensitivity analysis
4. Select option 6 (Allowable Ranges)

## Verification Checklist:

- [ ] Shadow prices match: 1, 2, 0
- [ ] Operation 1 range: [230, 440]
- [ ] Operation 2 range: [440, 860]
- [ ] Operation 3 range: [-∞, ∞]

If ALL match → ✅ FIXED!
If Any differ → Need more debugging

---

**Note:** The fix in `sensitivity_module.py` changed the algorithm to:

1. Extract columns of B^(-1) instead of rows
2. Correctly calculate max increase/decrease
3. Display absolute values for shadow prices

This should match the TOYCO methodology from your textbook images.
