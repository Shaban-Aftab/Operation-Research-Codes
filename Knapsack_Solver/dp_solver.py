"""
Dynamic Programming Solver for 0/1 Knapsack
===========================================
Implements DP with step-by-step visualization and backtracking.
"""

from knapsack_core import KnapsackEngine


class DPKnapsackSolver(KnapsackEngine):
    """0/1 Knapsack solver using Dynamic Programming"""
    
    def __init__(self):
        super().__init__()
        self.dp_table = []
        self.selected_items = []
    
    def solve(self, show_steps=True):
        """Solve knapsack using DP"""
        print("\n" + "=" * 70)
        print("      SOLVING 0/1 KNAPSACK USING DYNAMIC PROGRAMMING")
        print("="*70)
        
        n = self.num_items
        W = self.capacity
        
        # Check required items feasibility
        req_weight = sum([self.weights[i] for i in self.required_items])
        req_value = sum([self.values[i] for i in self.required_items])
        
        if req_weight > W:
            print(f"\n✗ ERROR: Required items (weight={req_weight}) exceed capacity ({W})!")
            return False
        
        # Initialize DP table
        self.dp_table = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
        
        print("\n" + "-" * 70)
        print(f"Table dimensions: ({n+1}) rows × ({W+1}) columns")
        print(f"dp[i][w] = Maximum value using items 0..i-1 with capacity w")
        print("-" * 70)
        
        if show_steps:
            input("\nPress ENTER to see step-by-step DP table filling...")
        
        # Fill DP table
        for i in range(1, n + 1):
            item_idx = i - 1
            
            if show_steps:
                print(f"\n{'='*70}")
                print(f"  PROCESSING ITEM {i}: {self.item_names[item_idx]}")
                print(f"  Weight = {self.weights[item_idx]}, Value = {self.values[item_idx]}")
            
            is_excluded = item_idx in self.excluded_items
            is_required = item_idx in self.required_items
            
            if is_excluded:
                if show_steps:
                    print("  *** EXCLUDED - Skipping ***")
                for w in range(W + 1):
                    self.dp_table[i][w] = self.dp_table[i-1][w]
                continue
            
            if is_required and show_steps:
                print("  *** REQUIRED - Must include ***")
            
            # Fill for each capacity
            for w in range(W + 1):
                if self.weights[item_idx] > w:
                    # Can't include
                    self.dp_table[i][w] = self.dp_table[i-1][w]
                else:
                    # Can include
                    exclude_value = self.dp_table[i-1][w]
                    include_value = self.values[item_idx] + self.dp_table[i-1][w - self.weights[item_idx]]
                    
                    if is_required:
                        self.dp_table[i][w] = include_value
                    else:
                        self.dp_table[i][w] = max(exclude_value, include_value)
            
            if show_steps and self.weights[item_idx] <= W:
                exclude_val = self.dp_table[i-1][W]
                include_val = self.values[item_idx] + self.dp_table[i-1][W - self.weights[item_idx]]
                print(f"\n  At capacity w={W}:")
                if is_required:
                    print(f"    MUST INCLUDE: {include_val}")
                else:
                    print(f"    Exclude: {exclude_val} vs Include: {include_val}")
                    print(f"    Decision: {'INCLUDE' if self.dp_table[i][W] == include_val else 'EXCLUDE'}")
                
                if i < n:
                    input(f"  Press ENTER to process next item...")
        
        print(f"\n{'='*70}")
        print(f"  >>> MAXIMUM VALUE = dp[{n}][{W}] = {self.dp_table[n][W]}")
        print("="*70)
        
        # Backtrack
        self._backtrack(show_steps)
        
        # Display solution
        self.display_solution()
        
        return True
    
    def _backtrack(self, show_steps=True):
        """Backtrack to find selected items"""
        print("\n" + "=" * 70)
        print("      BACKTRACKING TO FIND SELECTED ITEMS")
        print("=" * 70)
        
        n = self.num_items
        w = self.capacity
        self.selected_items = []
        
        if show_steps:
            print(f"\nStarting from dp[{n}][{w}] = {self.dp_table[n][w]}")
            print("\nBacktracking path:")
        
        for i in range(n, 0, -1):
            if self.dp_table[i][w] != self.dp_table[i-1][w]:
                self.selected_items.insert(0, i-1)
                if show_steps:
                    print(f"  dp[{i}][{w}] ≠ dp[{i-1}][{w}] => {self.item_names[i-1]} INCLUDED")
                    print(f"     Remaining capacity: {w} - {self.weights[i-1]} = {w - self.weights[i-1]}")
                w -= self.weights[i-1]
            else:
                if show_steps:
                    print(f"  dp[{i}][{w}] == dp[{i-1}][{w}] => {self.item_names[i-1]} NOT included")
    
    def display_solution(self):
        """Display optimal solution"""
        print("\n" + "=" * 60)
        print("                OPTIMAL SOLUTION")
        print("=" * 60)
        
        total_weight = 0
        total_value = 0
        
        print("\nSelected Items:")
        print("-" * 50)
        print(f"{'Item':<20}{'Weight':<10}{'Value':<10}")
        print("-" * 50)
        
        for idx in self.selected_items:
            print(f"{self.item_names[idx]:<20}{self.weights[idx]:<10}{self.values[idx]:<10.2f}")
            total_weight += self.weights[idx]
            total_value += self.values[idx]
        
        print("-" * 50)
        print(f"{'TOTAL':<20}{total_weight:<10}{total_value:<10.2f}")
        print("-" * 50)
        
        print(f"\nKnapsack Capacity Used: {total_weight} / {self.capacity}")
        print(f"Remaining Capacity: {self.capacity - total_weight}")
        print(f"\nMaximum Value Achieved: {total_value:.2f}")
        
        # Visual representation
        print("\n" + "-" * 50)
        print("KNAPSACK VISUALIZATION")
        print("-" * 50)
        
        filled = int((total_weight / self.capacity) * 30)
        empty = 30 - filled
        
        print(f"\n  [{'#' * filled}{'.' * empty}]")
        print(f"  Capacity: {total_weight}/{self.capacity} ({(total_weight/self.capacity*100):.1f}% full)")
        
        # Items not selected
        not_selected = [i for i in range(self.num_items) if i not in self.selected_items]
        if not_selected:
            print("\n  Items NOT selected:")
            for idx in not_selected:
                print(f"  x {self.item_names[idx]} (w={self.weights[idx]}, v={self.values[idx]})")
