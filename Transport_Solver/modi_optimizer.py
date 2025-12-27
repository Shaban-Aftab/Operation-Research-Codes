"""
MODI Method (Modified Distribution) for Transportation Problem
==============================================================
Optimality test and solution improvement using dual variables.

Also known as: U-V Method, Stepping Stone Method

Algorithm:
1. Calculate u[i] and v[j] dual variables from basic cells
2. For non-basic cells, calculate opportunity cost: Δ = c[i][j] - u[i] - v[j]  
3. If all Δ ≥ 0, solution is optimal
4. Otherwise, find most negative Δ (entering variable)
5. Construct closed loop
6. Redistribute along loop
7. Repeat until optimal
"""

from transport_core import TransportationEngine


class MODIOptimizer(TransportationEngine):
    """MODI Method optimizer for transportation problem"""
    
    def optimize(self, max_iterations=50):
        """Optimize using MODI method"""
        print("\n" + "="*70)
        print("         MODI METHOD - Optimization")
        print("="*70)
        
        for iteration in range(1, max_iterations + 1):
            print(f"\n{'='*60}")
            print(f"  ITERATION {iteration}")
            print(f"{'='*60}")
            
            # Step 1: Calculate dual variables
            u, v = self._calculate_dual_variables()
            
            if u is None or v is None:
                print("\n✗ Could not calculate dual variables!")
                return False
            
            print(f"\n→ Dual variables:")
            print(f"  u = {[f'{self.source_names[i]}:{u[i]:.1f}' for i in range(self.num_sources)]}")
            print(f"  v = {[f'{self.dest_names[j]}:{v[j]:.1f}' for j in range(self.num_destinations)]}")
            
            # Step 2: Calculate opportunity costs
            entering_cell, min_delta = self._find_entering_variable(u, v)
            
            # Step 3: Check optimality
            if entering_cell is None or min_delta >= -self.EPSILON:
                print("\n" + "="*60)
                print("  ✓ OPTIMAL SOLUTION FOUND!")
                print("="*60)
                self.display_allocation("OPTIMAL SOLUTION")
                self.calculate_cost()
                return True
            
            print(f"\n→ Most negative opportunity cost: Δ = {min_delta:.2f}")
            print(f"   Entering cell: ({self.source_names[entering_cell[0]]}, {self.dest_names[entering_cell[1]]})")
            print(  "  ✗ NOT OPTIMAL - Improving...")
            
            # Step 4: Find loop and improve
            loop = self._find_closed_loop(entering_cell)
           
            if loop is None or len(loop) < 4:
                print("\n✗ Could not find valid loop!")
                return False
            
            print(f"\n→ Closed loop with {len(loop)} cells:")
            loop_str = " → ".join([f"({self.source_names[i]},{self.dest_names[j]})" for i, j in loop])
            print(f"  {loop_str}")
            
            # Step 5: Redistribute
            theta = self._get_redistribution_amount(loop)
            print(f"\n→ Redistribution amount (θ) = {theta:.2f}")
            
            self._redistribute_along_loop(loop, theta)
            
            self.display_allocation(f"After Iteration {iteration}")
            self.calculate_cost()
        
        print("\n⚠ Maximum iterations reached!")
        return False
    
    def _calculate_dual_variables(self):
        """Calculate u and v dual variables"""
        u = [None] * self.num_sources
        v = [None] * self.num_destinations
        
        # Set u[0] = 0
        u[0] = 0
        
        # Iteratively find all u and v
        # For basic cell (i,j): u[i] + v[j] = c[i][j]
        max_iter = 1000  # Increased for complex problems
        for iteration in range(max_iter):
            updated = False
            
            for i in range(self.num_sources):
                for j in range(self.num_destinations):
                    if self.allocation[i][j] is not None:
                        # Basic cell
                        if u[i] is not None and v[j] is None:
                            v[j] = self.cost_matrix[i][j] - u[i]
                            updated = True
                        elif v[j] is not None and u[i] is None:
                            u[i] = self.cost_matrix[i][j] - v[j]
                            updated = True
            
            # Check if all found
            if None not in u and None not in v:
                return u, v
            
            if not updated:
                # If no updates possible but not all found, try setting another u to 0
                for i in range(self.num_sources):
                    if u[i] is None:
                        u[i] = 0
                        updated = True
                        break
                
                if not updated:
                    break
        
        # Check if all found
        if None in u or None in v:
            return None, None
        
        return u, v
    
    def _find_entering_variable(self, u, v):
        """Find entering variable (most negative opportunity cost)"""
        min_delta = 0
        entering_cell = None
        
        print("\n→ Opportunity costs (non-basic cells):")
        
        for i in range(self.num_sources):
            for j in range(self.num_destinations):
                if self.allocation[i][j] is None:
                    # Non-basic cell
                    delta = self.cost_matrix[i][j] - u[i] - v[j]
                    print(f"   ({self.source_names[i]},{self.dest_names[j]}): "
                          f"Δ = {self.cost_matrix[i][j]:.0f} - {u[i]:.1f} - {v[j]:.1f} = {delta:.2f}")
                    
                    if delta < min_delta:
                        min_delta = delta
                        entering_cell = (i, j)
        
        return entering_cell, min_delta
    
    def _find_closed_loop(self, start_cell):
        """Find closed loop starting from entering cell"""
        # Get basic cells
        basic_cells = {(i, j) for i in range(self.num_sources) 
                      for j in range(self.num_destinations) 
                      if self.allocation[i][j] is not None}
        
        # BFS to find loop
        def find_loop_bfs(current, direction, path, visited):
            """
            direction: 'H' = horizontal, 'V' = vertical
            """
            ci, cj = current
            
            if direction == 'H':
                # Move horizontally
                for j in range(self.num_destinations):
                    if j == cj:
                        continue
                    cell = (ci, j)
                    
                    # Check if back to start
                    if cell == start_cell and len(path) >= 3:
                        return path + [current]
                    
                    # Check if valid (basic cell)
                    if cell in basic_cells and cell not in visited:
                        result = find_loop_bfs(cell, 'V', path + [current], visited | {cell})
                        if result:
                            return result
            else:
                # Move vertically
                for i in range(self.num_sources):
                    if i == ci:
                        continue
                    cell = (i, cj)
                    
                    # Check if back to start
                    if cell == start_cell and len(path) >= 3:
                        return path + [current]
                    
                    # Check if valid (basic cell)
                    if cell in basic_cells and cell not in visited:
                        result = find_loop_bfs(cell, 'H', path + [current], visited | {cell})
                        if result:
                            return result
            
            return None
        
        # Try starting horizontally
        loop = find_loop_bfs(start_cell, 'H', [], {start_cell})
        if loop:
            return loop
        
        # Try starting vertically
        loop = find_loop_bfs(start_cell, 'V', [], {start_cell})
        return loop
    
    def _get_redistribution_amount(self, loop):
        """Get theta - minimum allocation at negative positions"""
        theta = float('inf')
        
        # Negative positions are at odd indices (1, 3, 5, ...)
        for idx in range(1, len(loop), 2):
            i, j = loop[idx]
            if self.allocation[i][j] is not None:
                theta = min(theta, self.allocation[i][j])
        
        return theta
    
    def _redistribute_along_loop(self, loop, theta):
        """Redistribute theta along the loop"""
        print("\n→ Redistribution:")
        
        for idx, (i, j) in enumerate(loop):
            if idx % 2 == 0:
                # Add
                if self.allocation[i][j] is None:
                    self.allocation[i][j] = theta
                else:
                    self.allocation[i][j] += theta
                print(f"  (+) ({self.source_names[i]},{self.dest_names[j]}): "
                      f"+{theta:.2f} = {self.allocation[i][j]:.2f}")
            else:
                # Subtract
                self.allocation[i][j] -= theta
                print(f"  (-) ({self.source_names[i]},{self.dest_names[j]}): "
                      f"-{theta:.2f} = {self.allocation[i][j]:.2f}")
                
                # Remove if becomes zero
                if self.allocation[i][j] < self.EPSILON:
                    self.allocation[i][j] = None
