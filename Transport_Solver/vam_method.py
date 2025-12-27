"""
Vogel's Approximation Method (VAM) for Transportation Problem
=============================================================

Algorithm:
For each row and column:
1. Calculate penalty = difference between two smallest costs
2. Select row/column with maximum penalty  
3. Allocate to minimum cost cell in that row/column

"""

from transport_core import TransportationEngine


class VAMSolver(TransportationEngine):
    """Vogel's Approximation Method solver"""
    
    def find_initial_solution(self):
        """Generate initial BFS using VAM"""
        print("\n" + "="*70)
        print("      VOGEL'S APPROXIMATION METHOD - Initial Solution")
        print("="*70)
        
        print("\n→ Algorithm: Use penalty-based intelligent allocation")
        print("  Penalty = (2nd minimum cost) - (1st minimum cost)")
        
        self.initialize_allocation()
        
        # Working copies
        supply_left = self.supply[:]
        demand_left = self.demand[:]
        
        # Track active rows/columns
        active_rows = set(range(self.num_sources))
        active_cols = set(range(self.num_destinations))
        
        iteration = 1
        
        while active_rows and active_cols:
            print(f"\n{'='*60}")
            print(f"  VAM ITERATION {iteration}")
            print(f"{'='*60}")
            
            # Calculate row penalties
            row_penalties = {}
            for i in active_rows:
                costs = sorted([self.cost_matrix[i][j] for j in active_cols
                               if self.allocation[i][j] is None])
                if len(costs) >= 2:
                    penalty = costs[1] - costs[0]
                elif len(costs) == 1:
                    penalty = costs[0]
                else:
                    continue
                row_penalties[i] = penalty
            
            # Calculate column penalties  
            col_penalties = {}
            for j in active_cols:
                costs = sorted([self.cost_matrix[i][j] for i in active_rows
                               if self.allocation[i][j] is None])
                if len(costs) >= 2:
                    penalty = costs[1] - costs[0]
                elif len(costs) == 1:
                    penalty = costs[0]
                else:
                    continue
                col_penalties[j] = penalty
            
            if not row_penalties and not col_penalties:
                break
            
            # Find maximum penalty
            max_row_penalty = max(row_penalties.values()) if row_penalties else -1
            max_col_penalty = max(col_penalties.values()) if col_penalties else -1
            
            print(f"\n  Row Penalties: {[(self.source_names[i], f'{p:.0f}') for i, p in row_penalties.items()]}")
            print(f"  Col Penalties: {[(self.dest_names[j], f'{p:.0f}') for j, p in col_penalties.items()]}")
            
            # Select based on maximum penalty
            if max_row_penalty >= max_col_penalty:
                # Row has max penalty
                selected_row = max(row_penalties, key=row_penalties.get)
                
                # Find min cost in this row
                min_cost = float('inf')
                selected_col = -1
                for j in active_cols:
                    if self.allocation[selected_row][j] is None:
                        if self.cost_matrix[selected_row][j] < min_cost:
                            min_cost = self.cost_matrix[selected_row][j]
                            selected_col = j
                
                print(f"\n  → Row {self.source_names[selected_row]} selected (penalty={row_penalties[selected_row]:.0f})")
            else:
                # Column has max penalty
                selected_col = max(col_penalties, key=col_penalties.get)
                
                # Find min cost in this column
                min_cost = float('inf')
                selected_row = -1
                for i in active_rows:
                    if self.allocation[i][selected_col] is None:
                        if self.cost_matrix[i][selected_col] < min_cost:
                            min_cost = self.cost_matrix[i][selected_col]
                            selected_row = i
                
                print(f"\n  → Column {self.dest_names[selected_col]} selected (penalty={col_penalties[selected_col]:.0f})")
            
            if selected_row == -1 or selected_col == -1:
                break
            
            # Allocate
            allocation = min(supply_left[selected_row], demand_left[selected_col])
            self.allocation[selected_row][selected_col] = allocation
            
            print(f"  → Cell ({self.source_names[selected_row]}, {self.dest_names[selected_col]})")
            print(f"     Cost: {min_cost:.0f}, Allocate: {allocation:.0f}")
            
            supply_left[selected_row] -= allocation
            demand_left[selected_col] -= allocation
            
            # Remove exhausted
            if supply_left[selected_row] < self.EPSILON:
                active_rows.remove(selected_row)
                print(f"  → Source {self.source_names[selected_row]} EXHAUSTED")
            if demand_left[selected_col] < self.EPSILON:
                active_cols.remove(selected_col)
                print(f"  → Destination {self.dest_names[selected_col]} SATISFIED")
            
            iteration += 1
        
        # Handle degeneracy
        self.handle_degeneracy()
        
        print("\n✓ VAM Complete!")
        self.display_allocation("Initial BFS (VAM)")
        self.calculate_cost()
        
        return self.allocation
