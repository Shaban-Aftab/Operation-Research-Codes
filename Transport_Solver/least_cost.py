"""
Least Cost Method for Transportation Problem
============================================
Greedy approach - always allocate to lowest cost cell first.

Algorithm:
1. Find cell with minimum cost among available cells
2. Allocate maximum possible (min of supply and demand)
3. Cross out exhausted row or column
4. Repeat until all allocated
"""

from transport_core import TransportationEngine


class LeastCostSolver(TransportationEngine):
    """Least Cost Method (Greedy) solver"""
    
    def find_initial_solution(self):
        """Generate initial BFS using Least Cost Method"""
        print("\n" + "="*70)
        print("         LEAST COST METHOD - Initial Solution")
        print("="*70)
        
        print("\n→ Algorithm: Always choose minimum cost cell")
        
        self.initialize_allocation()
        
        # Working copies
        supply_left = self.supply[:]
        demand_left = self.demand[:]
        
        step = 1
        
        while True:
            # Find minimum cost cell with available supply/demand
            min_cost = float('inf')
            min_i, min_j = -1, -1
            
            for i in range(self.num_sources):
                if supply_left[i] < self.EPSILON:
                    continue
                for j in range(self.num_destinations):
                    if demand_left[j] < self.EPSILON:
                        continue
                    if self.allocation[i][j] is None and self.cost_matrix[i][j] < min_cost:
                        min_cost = self.cost_matrix[i][j]
                        min_i, min_j = i, j
            
            if min_i == -1:
                break  # All allocated
            
            print(f"\n--- Step {step}: Minimum Cost Cell ---")
            print(f"  Cell: ({self.source_names[min_i]}, {self.dest_names[min_j]})")
            print(f"  Cost: {min_cost:.0f}")
            print(f"  Supply: {supply_left[min_i]:.0f}, Demand: {demand_left[min_j]:.0f}")
            
            # Allocate
            allocation = min(supply_left[min_i], demand_left[min_j])
            self.allocation[min_i][min_j] = allocation
            
            print(f"  Allocate: {allocation:.0f} units")
            
            supply_left[min_i] -= allocation
            demand_left[min_j] -= allocation
            
            if supply_left[min_i] < self.EPSILON:
                print(f"  → Source {self.source_names[min_i]} exhausted")
            if demand_left[min_j] < self.EPSILON:
                print(f"  → Destination {self.dest_names[min_j]} satisfied")
            
            step += 1
        
        # Handle degeneracy
        self.handle_degeneracy()
        
        print("\n✓ Least Cost Method Complete!")
        self.display_allocation("Initial BFS (Least Cost)")
        self.calculate_cost()
        
        return self.allocation
