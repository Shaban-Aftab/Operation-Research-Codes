# Operation Research Solver Suite 🔢

**Complete implementations of Linear Programming, Integer Programming, and Optimization algorithms**  
_Built with zero external dependencies - Pure Python 3!_

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)](requirements.txt)

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Implemented Algorithms](#implemented-algorithms)
- [Project Structure](#project-structure)
- [Usage Examples](#usage-examples)
- [Documentation](#documentation)
- [Contributing](#contributing)

## ✨ Features

### Linear Programming (LP) Solver

- **Simplex Method** - Standard LP optimization
- **Big-M Method** - Handles >=, <=, and = constraints
- **Dual Simplex Method** - Restores feasibility
- **Sensitivity Analysis** - Complete post-optimal analysis with 5 types:
  - RHS/Resource availability changes
  - Objective coefficient variations
  - Constraint coefficient changes
  - New constraint additions
  - New variable additions
- **Allowable Ranges** - Shadow prices and feasibility ranges

### Integer Linear Programming (ILP) Solver

- **Branch & Bound Algorithm** - Pure/Mixed integer optimization
- **Binary Programming** - 0/1 variable support
- **Tree Visualization** - ASCII art of branch & bound tree
- **Multiple Solutions** - Find top-N optimal solutions

### Transportation Problem Solver

- **North-West Corner Method**
- **Least Cost Method**
- **Vogel's Approximation Method (VAM)**
- **MODI Method (UV Method)** - Optimality testing
- **Stepping Stone Method** - Solution improvement
- **Balanced/Unbalanced** - Handles supply/demand mismatches

### Assignment Problem Solver

- **Hungarian Algorithm** - Optimal assignment
- **Step-by-step visualization**
- **Minimization/Maximization**

### Traveling Salesman Problem (TSP)

- **Nearest Neighbor Heuristic**
- **2-Opt Improvement**
- **Branch & Bound Exact Solution**

### Knapsack Problem

- **0/1 Knapsack** - Branch & Bound solution
- **Dynamic Programming** approach
- **Top-N solutions**

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Operation-Research-Codes.git
cd Operation-Research-Codes

# No installation needed! Just run:
python LP_Solver_Final/integrated_solver.py
```

## 🎯 Implemented Algorithms

### 1. LP Solver (`LP_Solver_Final/`)

```
├── integrated_solver.py       # Main integrated interface
├── simplex_refactored.py      # Standard Simplex implementation
├── big_m_method.py            # Big-M method for >= and = constraints
├── dual_simplex.py            # Dual Simplex algorithm
└── sensitivity_module.py      # Complete sensitivity analysis
```

**Run:**

```bash
python LP_Solver_Final/integrated_solver.py
```

**Features:**

- Interactive menu with 7 options
- Full sensitivity analysis with shadow prices
- Allowable range calculations
- Step-by-step tableau display

---

### 2. ILP Solver (`ilp_solver.py`)

```
ilp_solver.py                  # Complete Branch & Bound ILP solver
```

**Run:**

```bash
python ilp_solver.py
```

**Features:**

- Pure/Mixed/Binary integer programming
- Visual branch & bound tree
- Handles strict inequalities (<, >)
- Top-N solutions

---

### 3. Transportation Solver (`Transportation_enhanced.py`)

```
Transportation_enhanced.py     # Complete transportation problem solver
```

**Run:**

```bash
python Transportation_enhanced.py
```

**Methods Implemented:**

- North-West Corner
- Least Cost
- Vogel's Approximation Method (VAM)
- MODI optimization
- Stepping Stone method

---

### 4. Assignment Solver (`assignment_solver.py`)

```
assignment_solver.py           # Hungarian Algorithm implementation
```

**Run:**

```bash
python assignment_solver.py
```

---

### 5. TSP Solver (`tsp_solver.py`)

```
tsp_solver.py                  # Traveling Salesman Problem
```

---

### 6. Knapsack Solver

```
Knapsack_Solver/               # Multiple knapsack implementations
```

## 📁 Project Structure

```
Operation-Research-Codes/
│
├── LP_Solver_Final/              # Complete LP Solver Suite
│   ├── integrated_solver.py      # ⭐ Main entry point
│   ├── simplex_refactored.py
│   ├── big_m_method.py
│   ├── dual_simplex.py
│   └── sensitivity_module.py
│
├── ilp_solver.py                 # ⭐ Integer LP Solver
├── Transportation_enhanced.py    # ⭐ Transportation Problem
├── assignment_solver.py          # ⭐ Assignment Problem
├── tsp_solver.py                 # ⭐ TSP Solver
│
├── Knapsack_Solver/              # Knapsack variants
├── docs/                         # Documentation & guides
│   ├── SENSITIVITY_EXAM_GUIDE.md
│   ├── MANUAL_TEST_GUIDE.md
│   └── ILP_README.md
│
└── README.md                     # This file
```

## 💡 Usage Examples

### Example 1: Solving an LP Problem with Sensitivity Analysis

```bash
python LP_Solver_Final/integrated_solver.py
# Choose option 4: Simplex + Sensitivity Analysis
# Input your problem
# Get optimal solution + complete sensitivity analysis
```

### Example 2: Integer Programming

```bash
python ilp_solver.py
# Define variables, constraints
# Specify integer variables
# Get optimal integer solution with branch & bound tree
```

### Example 3: Transportation Problem

```bash
python Transportation_enhanced.py
# Input supply, demand, and costs
# Choose initial method (VAM recommended)
# Get optimal allocation using MODI method
```

## 📖 Documentation

Detailed guides available in `/docs`:

- **Sensitivity Analysis Guide** - Complete exam preparation
- **Manual Test Guide** - Step-by-step testing
- **ILP README** - Comprehensive ILP solver documentation

## 🔬 Key Algorithms Explained

### Simplex Method

The simplex algorithm iteratively moves from vertex to vertex of the feasible region, improving the objective function value at each step until optimality is reached.

### Big-M Method

Handles >= and = constraints by introducing artificial variables with large penalty coefficient M, ensuring they leave the basis.

### Sensitivity Analysis

Analyzes how changes in problem parameters affect the optimal solution:

- **Shadow Prices**: Marginal value of resources
- **Allowable Ranges**: Parameter ranges maintaining current basis
- **Reduced Costs**: Profitability of non-basic variables

### Branch & Bound for ILP

Systematically explores the solution space by:

1. Solving LP relaxation
2. Branching on fractional variables
3. Bounding subproblems
4. Finding optimal integer solution

## 🎓 Academic Use

This repository was developed for **Operation Research (CS-460)** course at FAST-NUCES.

**Verified Algorithms:**

- ✅ All implementations tested against textbook examples
- ✅ Sensitivity analysis matches TOYCO model results
- ✅ ILP solver handles binary/pure/mixed integer programs
- ✅ Transportation solvers produce optimal allocations

## 🤝 Contributing

Contributions welcome! Feel free to:

- Report bugs
- Suggest enhancements
- Add new algorithms
- Improve documentation

## 📝 License

MIT License - feel free to use for academic purposes!

## 👨‍💻 Author

**Shaban Aftab**  
FAST-NUCES  
Operation Research - CS-460

## 🌟 Acknowledgments

Built as part of coursework with zero external dependencies to demonstrate pure algorithmic implementations.

---

**⭐ If this repo helped you, please give it a star!**
