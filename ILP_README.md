# Integer Linear Programming (ILP) Solver

**Complete Python Implementation of Branch & Bound Algorithm**

Zero external dependencies • Pure/Mixed/Binary ILP • Tree Visualization

---

## Features

### Supported Problem Types

1. **Pure Integer Programming** - All variables must be integers
2. **Mixed Integer Programming** - Some integer, some continuous
3. **Binary Integer Programming** - All variables are 0 or 1

### Algorithm Features

- ✅ Branch & Bound with Best-First Search
- ✅ Simplex Method for LP Relaxation
- ✅ Big M Method for >= and = constraints
- ✅ Automatic constraint type conversion
- ✅ Top-N solutions support
- ✅ ASCII Tree Visualization
- ✅ Step-by-step iteration display

### Constraint Types Supported

- `<=` (Less than or equal)
- `>=` (Greater than or equal)
- `=` (Equality)
- `<` (Strict less than - treated as <=)
- `>` (Strict greater than - treated as >=)

---

## Installation

No installation required! Just Python 3.x standard library.

```bash
# Clone or download ilp_solver.py
python ilp_solver.py
```

---

## Usage

### Interactive Mode

```bash
python ilp_solver.py
```

Follow the prompts:

1. Select optimization type (Maximization/Minimization)
2. Enter number of variables and constraints
3. Input objective function coefficients
4. Input constraint coefficients, types, and RHS values
5. Specify which variables must be integers
6. Optionally specify binary variables (0/1)
7. Choose how many top solutions to display

### Programmatic Mode

```python
from ilp_solver import ILPSolver

# Create solver
solver = ILPSolver()

# Configure problem
solver.num_variables = 2
solver.num_constraints = 2
solver.objective = [5, 4]
solver.constraints = [[1, 1], [10, 6]]
solver.rhs = [5, 45]
solver.constraint_types = [1, 1]  # Both <=
solver.is_maximization = True
solver.integer_vars = [0, 1]  # Both integer
solver.top_n = 1

# Solve
solver.solve()
```

---

## Example Problems

### Example 1: Pure Integer LP

```
Maximize z = 5x1 + 4x2
Subject to:
  x1 + x2 <= 5
  10x1 + 6x2 <= 45
  x1, x2 integers, x1, x2 >= 0
```

**Solution**: x1 = 3, x2 = 2, Z = 23

### Example 2: Mixed Integer LP

```
Maximize Z = 3x1 + 2x2
Subject to:
  2x1 + 5x2 <= 18
  4x1 + 2x2 <= 18
  x1 integer, x2 continuous
  x1, x2 >= 0
```

**Solution**: x1 = 4, x2 = 1, Z = 14

### Example 3: Binary Programming

```
Maximize z = 18x1 + 14x2 + 8x3 + 4x4
Subject to:
  15x1 + 12x2 + 7x3 + 4x4 + x5 <= 37
  0 <= xj <= 1, j = 1,2,...,5
```

**Solution**: x1 = 1, x2 = 1, x3 = 1, x4 = 0, x5 = 0, Z = 40

---

## Algorithm Details

### Branch & Bound Process

1. **LP Relaxation**: Solve linear program without integer constraints
2. **Check Integer**: If all integer variables have integer values → Done!
3. **Branch**: Select most fractional variable xi = v
   - Left branch: xi <= floor(v)
   - Right branch: xi >= ceil(v)
4. **Bound**: Prune nodes with worse bounds than current best
5. **Repeat**: Until all nodes explored or pruned

### Simplex Solver

- Handles <=, >=, and = constraints
- Big M method for >= and = constraints
- Converts >= to <= by negating coefficients
- Post-solve feasibility verification

### Tree Visualization

```
✓ = Optimal integer solution
● = Integer solution
○ = Fractional (branched)
✗ = Infeasible/Pruned
```

---

## Output

The solver provides:

1. **Problem Formulation** - Shows the LP problem
2. **LP Relaxation** - Root node solution
3. **Branch & Bound Iterations** - Step-by-step progress
4. **Tree Visualization** - ASCII tree of all nodes
5. **Final Solution** - Optimal integer solution(s)
6. **Statistics** - Nodes explored, iterations, solutions found

---

## Testing

Run the included test files:

```bash
# Test Example 9.2-1 from textbook
python verify_ilp_algorithm.py

# Test mixed integer problem
python test_ilp.py

# Test binary programming
python test_binary.py
```

---

## Technical Details

### Files

- `ilp_solver.py` - Main solver (850+ lines)
- `test_*.py` - Test cases
- `verify_*.py` - Verification scripts

### Classes

- `SimplexSolver` - LP solver with Big M
- `TreeNode` - Branch & Bound tree node
- `ILPSolver` - Main ILP solver

### Key Methods

- `get_user_input()` - Interactive input
- `solve()` - Main Branch & Bound algorithm
- `solve_subproblem()` - Solve LP relaxation
- `draw_tree()` - Visualize B&B tree
- `display_final_solution()` - Show results

---

## Limitations

- Uses exact floating-point arithmetic (may have small rounding errors)
- Best-first search (explores most promising nodes first)
- Maximum 100 Simplex iterations per subproblem
- Strictly >= constraint not supported (use >= instead)

---

## References

- Taha, H.A. (2017). _Operations Research: An Introduction_ (10th ed.)
- Land & Doig (1960). An automatic method of solving discrete programming problems
- Branch & Bound Algorithm with Simplex for LP relaxation

---

## License

MIT License - Free to use for educational and commercial purposes

---

## Author

Created for Operations Research course at FAST NUCES  
Branch & Bound • Simplex • Zero Dependencies
