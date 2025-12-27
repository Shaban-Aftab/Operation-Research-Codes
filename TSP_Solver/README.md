# TSP (Traveling Salesman Problem) Solver

Complete Python implementation of TSP using Branch and Bound algorithm.

## Features

✅ **Branch and Bound Algorithm**: Optimal solution guaranteed
✅ **Lower Bound Pruning**: Efficient search space reduction
✅ **Tree Visualization**: See complete decision tree
✅ **Two Input Methods**: Matrix or edge-by-edge
✅ **Modular Design**: Clean, separated modules
✅ **Zero Dependencies**: Pure Python (standard library only)
✅ **Step-by-Step Output**: Educational display

## Files

- `tsp_core.py` (350 lines) - Base engine with input/output
- `branch_bound.py` (230 lines) - Branch & Bound algorithm
- `tree_visualizer.py` (95 lines) - Tree display
- `integrated_tsp.py` (70 lines) - Main interface
- `test_tsp.py` - Test case

## Quick Start

```bash
cd TSP_Solver
python integrated_tsp.py
```

## Algorithm

**Branch and Bound** finds the optimal tour by:

1. **Initialize**: Start from chosen city
2. **Branch**: Explore unvisited cities
3. **Bound**: Calculate lower bound estimate
4. **Prune**: Discard paths worse than current best
5. **Solution**: Complete tour back to start

**Lower Bound** = Current cost + Minimum edges needed

## Example Problem

**4 Cities** (A, B, C, D):

```
     A    B    C    D
A   --   10   15   20
B   10   --   35   25
C   15   35   --   30
D   20   25   30   --
```

**Optimal Tour**: A → B → D → C → A  
**Cost**: 80  
**Nodes Explored**: 14

## Tree Visualization

```
[*] Node 0: [A] cost=0 bound=55.0
|-- [*] Node 1: [A->B] cost=10 bound=70.0
|   |-- [P] Node 4: [A->B->C] cost=45 bound=80.0
|   `-- [*] Node 5: [A->B->D] cost=35 bound=70.0
|       `-- [*] Node 8: [A->B->D->C] cost=65 bound=65.0
|-- [B] Node 2: [A->C] cost=15 bound=75.0
...
```

**Legend**:

- `[*]` = Optimal path
- `[S]` = Solution found
- `[P]` = Pruned
- `[B]` = Branched

## Input Methods

### Method 1: Distance Matrix

Enter all distances in matrix form:

```
A -> B: 10
A -> C: 15
...
```

### Method 2: Edge List

Enter edges one by one:

```
From: A, To: B, Distance: 10
From: A, To: C, Distance: 15
...
```

## Code Structure

```python
class TSPEngine:
    # Base class
    - Input handling
    - Data management
    - Display utilities

class BranchAndBoundTSP(TSPEngine):
    # Core algorithm
    - Lower bound calculation
    - Branching logic
    - Pruning strategy

class TreeVisualizer(BranchAndBoundTSP):
    # Visualization
    - Tree drawing
    - Solution display
```

## No External Dependencies

Uses only Python standard library:

- No NumPy
- No SciPy
- No networkx

Just pure Python!

## Test Results

**Test**: 4-city symmetric TSP

- ✅ Optimal tour found
- ✅ Cost = 80
- ✅ Tree visualization working
- ✅ All constraints satisfied

## Academic Use

Perfect for:

- Operations Research assignments
- Algorithm demonstrations
- Understanding Branch & Bound
- TSP visualization

---

**Created**: December 2024  
**Python**: 3.6+  
**Algorithm**: Branch and Bound  
**License**: Educational Use
