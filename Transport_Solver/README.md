# Transportation Problem Solver Suite

Complete modular transportation problem solver with multiple methods.

## Features

✅ **Three Initial BFS Methods**:

- Northwest Corner (simplest, educational)
- Least Cost (greedy approach)
- VAM (best initial solution)

✅ **MODI Optimization**: Finds optimal solution using dual variables

✅ **Modular Design**: Separate files for each method

✅ **Zero Dependencies**: Pure Python using only standard library

✅ **Step-by-Step Output**: Educational, like pen-and-paper solving

## Files

- `transport_core.py` - Base transportation engine
- `northwest_corner.py` - Northwest Corner method
- `least_cost.py` - Least Cost (greedy) method
- `vam_method.py` - Vogel's Approximation Method
- `modi_optimizer.py` - MODI optimization
- `integrated_transport.py` - Main interface

## Quick Start

```bash
cd Transport_Solver
python integrated_transport.py
```

## Menu Options

1. **Northwest Corner** - Quick initial solution
2. **Least Cost** - Greedy approach
3. **VAM** - Best initial solution (recommended)
4. **Complete Optimization** - VAM + MODI (finds optimal)
5. **Maximization** - **NEW!** For profit maximization problems
6. **Custom** - Choose your own workflow
7. **Exit**

## Example Problem

```
Sources: 3 (S1, S2, S3)
Destinations: 4 (D1, D2, D3, D4)

Supply: [60, 70, 50]
Demand: [60, 40, 30, 50]

Cost Matrix:
     D1   D2   D3   D4
S1   20   22   17   14
S2   24   37    9    7
S3   32   37   20   15
```

**Solution** (using VAM + MODI):

- S1 → D4: 60 units × $14 = $840
- S2 → D3: 30 units × $9 = $270
- S2 → D4: 40 units × $7 = $280
- S3 → D1: 50 units × $32 = $1600
- **Total Cost**: $2990

## Features

### Handles Unbalanced Problems

- Automatically adds dummy source or destination
- Zero cost for dummy allocations

### Degeneracy Detection

- Ensures m+n-1 basic variables
- Adds zero allocations as needed

### Solution Verification

- Checks supply constraints
- Checks demand constraints
- Validates m+n-1 requirement

## Academic Use

Perfect for:

- Operations Research assignments
- Transportation problem demonstrations
- Understanding optimization algorithms
- Learning MODI method step-by-step

## Code Structure

```python
class TransportationEngine:
    # Base class with common functionality
    - Input handling
    - Balancing
    - Display utilities
    - Cost calculation

class NorthwestCornerSolver(TransportationEngine):
    def find_initial_solution()

class LeastCostSolver(TransportationEngine):
    def find_initial_solution()

class VAMSolver(TransportationEngine):
    def find_initial_solution()

class MODIOptimizer(TransportationEngine):
    def optimize()
```

## No External Dependencies

Uses only Python standard library:

- No NumPy
- No SciPy
- No pandas

Just pure Python!

---

**Created**: December 2024  
**Python**: 3.6+  
**License**: Educational Use
