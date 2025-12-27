"""
Maximization in Transportation Problem
======================================
Solve maximization transportation problems by converting to minimization.

Method:
1. Find maximum cost in the entire cost matrix
2. Transform: new_cost[i][j] = max_cost - cost[i][j]
3. Solve transformed problem (minimization)
4. Report solution with ORIGINAL costs (maximization)


"""

from vam_method import VAMSolver
from modi_optimizer import MODIOptimizer


class MaximizationSolver(VAMSolver):
    """Maximization transportation problem solver"""
    
    def __init__(self):
        super().__init__()
        self.original_costs = None
        self.max_cost = 0
        self.is_maximization = True
    
    def solve_maximization(self):
        """Solve maximization problem"""
        print("\n" + "="*70)
        print("      MAXIMIZATION TRANSPORTATION PROBLEM")
        print("="*70)
        
        print("\n→ Converting MAXIMIZATION to MINIMIZATION")
        print("  Method: Subtract all costs from maximum cost")
        
        # Save original costs
        self.original_costs = [row[:] for row in self.cost_matrix]
        
        # Find maximum cost
        self.max_cost = max(max(row) for row in self.cost_matrix)
        print(f"\n  Maximum cost in table: {self.max_cost}")
        
        # Transform costs
        print("\n  Transforming cost matrix...")
        print("  New cost = Max cost - Original cost")
        
        for i in range(self.num_sources):
            for j in range(self.num_destinations):
                old_cost = self.cost_matrix[i][j]
                new_cost = self.max_cost - old_cost
                self.cost_matrix[i][j] = new_cost
                print(f"    ({self.source_names[i]},{self.dest_names[j]}): "
                      f"{self.max_cost} - {old_cost} = {new_cost}")
        
        print("\n→ Transformed Cost Matrix (for minimization):")
        self._display_cost_table()
        
        input("\n→ Press ENTER to find initial solution (VAM)...")
        
        # Find initial solution using VAM on transformed problem
        self.find_initial_solution()
        
        # Optimize with MODI
        print("\n→ Optimizing with MODI...")
        input("  Press ENTER to continue...")
        
        optimizer = MODIOptimizer()
        optimizer.__dict__.update(self.__dict__)
        result = optimizer.optimize()
        
        if result:
            # Solution found - display with ORIGINAL costs
            self.allocation = optimizer.allocation
            self.display_maximization_solution()
            return True
        else:
            print("\n⚠ Could not find optimal solution")
            return False
    
    def display_maximization_solution(self):
        """Display solution with original (maximization) costs"""
        print("\n" + "="*70)
        print("           MAXIMUM PROFIT TRANSPORTATION PLAN")
        print("="*70)
        
        # Show allocation table with ORIGINAL costs
        col_w = self.COL_WIDTH
        
        print(f"\n{'-'*70}")
        print("  Final Allocation (Original Profit Values)")
        print(f"{'-'*70}")
        
        # Header
        print("\n" + " "*10, end="")
        for name in self.dest_names:
            print(f"{name:^{col_w}}", end="")
        print(f"{'Supply':^{col_w}}")
        
        print(" "*10 + "-" * (col_w * (self.num_destinations + 1)))
        
        # Rows with allocations and ORIGINAL costs
        for i in range(self.num_sources):
            print(f"{self.source_names[i]:>8} |", end="")
            
            for j in range(self.num_destinations):
                orig_cost = self.original_costs[i][j]
                alloc = self.allocation[i][j]
                
                if alloc is not None and alloc > self.EPSILON:
                    cell = f"{orig_cost:.0f}[{alloc:.0f}]"
                elif alloc is not None:
                    cell = f"{orig_cost:.0f}[0]"
                else:
                    cell = f"{orig_cost:.0f}"
                
                print(f"{cell:^{col_w}}", end="")
            
            print(f"{self.supply[i]:^{col_w}.0f}")
        
        # Demand row
        print(" "*10 + "-" * (col_w * (self.num_destinations + 1)))
        print(f"{'Demand':>8} |", end="")
        for j in range(self.num_destinations):
            print(f"{self.demand[j]:^{col_w}.0f}", end="")
        print(f"{sum(self.demand):^{col_w}.0f}")
        
        # Calculate MAXIMUM profit using ORIGINAL costs
        print("\n→ Maximum Profit Calculation (using original values):")
        total_profit = 0
        terms = []
        
        for i in range(self.num_sources):
            for j in range(self.num_destinations):
                if self.allocation[i][j] is not None and self.allocation[i][j] > self.EPSILON:
                    profit = self.allocation[i][j] * self.original_costs[i][j]
                    total_profit += profit
                    terms.append(f"({self.allocation[i][j]:.0f}×{self.original_costs[i][j]:.0f})")
        
        print(f"  = " + " + ".join(terms))
        print(f"  = {total_profit:.2f}")
        
        print("\n" + "="*70)
        print(f">>> MAXIMUM TOTAL PROFIT: ${total_profit:.2f}")
        print("="*70)
        
        # Detailed shipments
        print("\n→ Optimal Shipment Plan:")
        print("-"*50)
        
        for i in range(self.num_sources):
            for j in range(self.num_destinations):
                if self.allocation[i][j] is not None and self.allocation[i][j] > self.EPSILON:
                    is_dummy = (self.source_names[i] == "Dummy" or self.dest_names[j] == "Dummy")
                    
                    if is_dummy:
                        print(f"  {self.source_names[i]:>6} → {self.dest_names[j]:<6}: "
                              f"{self.allocation[i][j]:>6.0f} units (DUMMY)")
                    else:
                        profit = self.allocation[i][j] * self.original_costs[i][j]
                        print(f"  {self.source_names[i]:>6} → {self.dest_names[j]:<6}: "
                              f"{self.allocation[i][j]:>6.0f} units × ${self.original_costs[i][j]:.0f} = ${profit:.0f}")
        
        print("-"*50)


def solve_maximization_problem():
    """Solve a maximization transportation problem"""
    print("\n" + "-"*70)
    print("         MAXIMIZATION TRANSPORTATION PROBLEM")
    print("-"*70)
    
    print("\n→ For PROFIT maximization instead of COST minimization")
    print("  Enter profit values in the cost matrix")
    
    solver = MaximizationSolver()
    solver.configure_problem()
    solver.balance_problem()
    
    input("\n→ Press ENTER to solve maximization problem...")
    solver.solve_maximization()
    solver.verify_solution()
    
    return solver
