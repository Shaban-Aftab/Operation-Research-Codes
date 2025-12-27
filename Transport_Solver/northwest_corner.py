"""
Northwest Corner Method for Transportation Problem
=================================================== 
Simplest initial BFS method - starts from top-left corner.

Algorithm:
1. Start at cell (0, 0) - northwest corner
2. Allocate min(supply, demand)
3. Move right if demand met, down if supply exhausted
4. Handle degeneracy when both exhaust simultaneously
"""

from transport_core import TransportationEngine


class NorthwestCornerSolver(TransportationEngine):
    """Northwest Corner Method solver"""
    
    def find_initial_solution(self):
        """Generate initial BFS using Northwest Corner Method"""
        print("\n" + "="*70)
        print("      NORTHWEST CORNER METHOD - Initial Solution")
        print("="*70)
        
        print("\n→ Algorithm: Start from top-left, move right/down")
        
        self.initialize_allocation()
        
        # Working copies
        supply_left = self.supply[:]
        demand_left = self.demand[:]
        
        i, j = 0, 0
        step = 1
        
        while i < self.num_sources and j < self.num_destinations:
            print(f"\n--- Step {step}: Cell ({self.source_names[i]}, {self.dest_names[j]}) ---")
            print(f"  Supply available: {supply_left[i]:.0f}")
            print(f"  Demand remaining: {demand_left[j]:.0f}")
            
            # Allocate minimum
            allocation = min(supply_left[i], demand_left[j])
            self.allocation[i][j] = allocation
            
            print(f"  Allocate: min({supply_left[i]:.0f}, {demand_left[j]:.0f}) = {allocation:.0f}")
            print(f"  Cost: {self.cost_matrix[i][j]:.0f} per unit")
            
            supply_left[i] -= allocation
            demand_left[j] -= allocation
            
            # Determine next move
            if abs(supply_left[i]) < self.EPSILON and abs(demand_left[j]) < self.EPSILON:
                # Both exhausted - degeneracy case
                if i + 1 < self.num_sources and j + 1 < self.num_destinations:
                    # Add zero to next cell to maintain basic variables
                    self.allocation[i][j + 1] = 0
                    print(f"  ⚠ Both exhausted! Added [0] to avoid degeneracy")
                i += 1
                j += 1
            elif abs(supply_left[i]) < self.EPSILON:
                print(f"  → Supply exhausted, moving DOWN")
                i += 1
            else:
                print(f"  → Demand met, moving RIGHT")
                j += 1
            
            step += 1
        
        print("\n✓ Northwest Corner Method Complete!")
        self.display_allocation("Initial BFS (Northwest Corner)")
        self.calculate_cost()
        
        return self.allocation
