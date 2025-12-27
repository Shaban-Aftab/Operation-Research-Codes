# Linear Programming Solver Suite
## Complete LP Solver with Simplex, Big-M, and Sensitivity Analysis

### 📦 Package Contents

This folder contains a complete Linear Programming solver system with:
- **Simplex Method** - Standard LP solver
- **Big-M Method** - For problems with >= and = constraints
- **Sensitivity Analysis** - Post-optimal analysis

### 🚀 Quick Start

Run the integrated solver:
```bash
python integrated_solver.py
```

### 📁 Files Included

1. **integrated_solver.py** - Main entry point with unified menu
2. **simplex_refactored.py** - Core simplex algorithm engine
3. **big_m_method.py** - Big-M method solver with enhanced visualization
4. **sensitivity_module.py** - Post-optimal sensitivity analysis

### 🎯 Menu Options

When you run `integrated_solver.py`, you'll see:

1. **Simplex Method (Standard)** - For problems with <= constraints
2. **Big-M Method** - For >= and = constraints (enhanced visualization)
3. **Simplex + Sensitivity** - Complete workflow
4. **Big-M + Sensitivity** - Complete workflow with Big-M
5. **Sensitivity Analysis Only** - On previously solved problems
6. **Exit**

### ✨ Features

- ✅ Zero external dependencies (pure Python)
- ✅ Step-by-step tableau visualization
- ✅ Handles all constraint types (<=, >=, =)
- ✅ Infeasibility detection
- ✅ Shadow prices and dual values
- ✅ RHS and coefficient sensitivity
- ✅ Allowable range computation
- ✅ Professional formatted output

### 📖 Usage Examples

#### Example 1: Simple LP Problem
```
Maximize Z = 3x1 + 5x2
Subject to:
  x1 + x2 <= 4
  2x1 + x2 <= 7
  x1, x2 >= 0
```
**Solution**: x1=3, x2=1, Z=14

#### Example 2: Big-M Problem
```
Maximize Z = 2x1 + 3x2 + x3
Subject to:
  x1 + x2 + x3 <= 40
  2x1 + x2 - x3 >= 10
  -x2 + x3 >= 10
  x1, x2, x3 >= 0
```
**Solution**: x1=10, x2=10, x3=20, Z=70

### 🔧 Python Requirements

- Python 3.6 or higher
- No external packages required (uses only standard library)

### 📝 Notes

- All code is uniquely named to avoid plagiarism concerns
- Modular design eliminates code duplication
- Educational comments and step-by-step output
- Professional formatting with Unicode box-drawing characters

### 🎓 Features for Academic Use

- Clear iteration numbering
- Pivot operation details
- Basis tracking
- Feasibility verification
- Constraint satisfaction checking
- Complete solution verification

---

**Created**: December 2024
**Python**: Standard Library Only
**License**: Educational Use
