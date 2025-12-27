"""
Branch & Bound Solver for 0/1 Knapsack
=======================================
Alternative method using Branch and Bound (finds top-N solutions)
"""

from knapsack_core import KnapsackEngine


class BranchBoundKnapsack(KnapsackEngine):
    """0/1 Knapsack solver using Branch & Bound"""
    
    def __init__(self):
        super().__init__()
        self.best_value = 0
        self.best_selection = []
        self.top_n = 1
        self.top_solutions = []
        self.nodes_explored = 0
    
    def configure_problem(self):
        """Override to add top-N selection"""
        super().configure_problem()
        
        # Ask for top-N solutions
        print("\n--- TOP SOLUTIONS ---")
        while True:
            try:
                self.top_n = int(input("How many top solutions to display? (default=1): ") or "1")
                if self.top_n > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Invalid input!")
    
    def calculate_upper_bound(self, level, current_value, current_weight, selection):
        """Calculate upper bound using fractional relaxation"""
        remaining_capacity = self.capacity - current_weight
        bound = current_value
        
        # Get remaining items sorted by value/weight ratio
        remaining = []
        for i in range(level, self.num_items):
            if i not in self.excluded_items and selection[i] == -1:
                ratio = self.values[i] / self.weights[i] if self.weights[i] > 0 else 0
                remaining.append((i, ratio, self.values[i], self.weights[i]))
        
        # Sort by ratio (greedy)
        remaining.sort(key=lambda x: x[1], reverse=True)
        
        # Add items greedily (fractional allowed for bound)
        for i, ratio, value, weight in remaining:
            if weight <= remaining_capacity:
                bound += value
                remaining_capacity -= weight
            else:
                # Add fractional part
                bound += ratio * remaining_capacity
                break
        
        return bound
    
    def is_feasible(self, selection):
        """Check if selection is feasible"""
        total_weight = sum(self.weights[i] for i in range(self.num_items) if selection[i] == 1)
        
        if total_weight > self.capacity:
            return False
        
        # Check required items
        for i in self.required_items:
            if selection[i] != 1:
                return False
        
        # Check excluded items
        for i in self.excluded_items:
            if selection[i] == 1:
                return False
        
        return True
    
    def branch_and_bound(self, selection, level, current_value, current_weight):
        """Recursive Branch & Bound"""
        self.nodes_explored += 1
        
        # Prune if over capacity
        if current_weight > self.capacity:
            return
        
        # Base case: all items considered
        if level == self.num_items:
            if self.is_feasible(selection):
                solution_copy = selection[:]
                total_val = sum(self.values[i] for i in range(self.num_items) if selection[i] == 1)
                
                # Add to top solutions
                self.top_solutions.append((total_val, solution_copy))
                self.top_solutions.sort(key=lambda x: x[0], reverse=True)
                
                if len(self.top_solutions) > self.top_n:
                    self.top_solutions = self.top_solutions[:self.top_n]
                
                if self.top_solutions:
                    self.best_value = self.top_solutions[0][0]
                    self.best_selection = self.top_solutions[0][1]
            return
        
        # Calculate upper bound
        bound = self.calculate_upper_bound(level, current_value, current_weight, selection)
        
        # Prune if bound <= worst in top-N
        worst_in_top = self.top_solutions[-1][0] if len(self.top_solutions) == self.top_n else float('-inf')
        if bound <= worst_in_top:
            return
        
        # Check if this item is required/excluded
        if level in self.required_items:
            # Must include
            selection[level] = 1
            self.branch_and_bound(selection, level + 1,
                                current_value + self.values[level],
                                current_weight + self.weights[level])
            selection[level] = -1
            return
        
        if level in self.excluded_items:
            # Must exclude
            selection[level] = 0
            self.branch_and_bound(selection, level + 1, current_value, current_weight)
            selection[level] = -1
            return
        
        # Try including item
        if current_weight + self.weights[level] <= self.capacity:
            selection[level] = 1
            self.branch_and_bound(selection, level + 1,
                                current_value + self.values[level],
                                current_weight + self.weights[level])
        
        # Try excluding item
        selection[level] = 0
        self.branch_and_bound(selection, level + 1, current_value, current_weight)
        
        # Reset
        selection[level] = -1
    
    def solve(self):
        """Solve using Branch & Bound"""
        print("\n" + "=" * 70)
        print("      SOLVING 0/1 KNAPSACK USING BRANCH & BOUND")
        print("=" * 70)
        
        print("\n→ Starting Branch & Bound search...")
        print(f"  Finding top {self.top_n} solution(s)")
        
        initial_selection = [-1] * self.num_items
        self.branch_and_bound(initial_selection, 0, 0, 0)
        
        print(f"\n✓ Search complete!")
        print(f"  Nodes explored: {self.nodes_explored}")
        print(f"  Solutions found: {len(self.top_solutions)}")
        
        self.display_solution()
        
        return True
    
    def display_solution(self):
        """Display all top solutions"""
        print("\n" + "=" * 70)
        if self.top_n > 1:
            print(f"              TOP {len(self.top_solutions)} SOLUTIONS")
        else:
            print("              OPTIMAL SOLUTION")
        print("=" * 70)
        
        if not self.top_solutions:
            print("\nNo feasible solution found!")
            return
        
        for rank, (value, selection) in enumerate(self.top_solutions, 1):
            print("\n" + "-" * 60)
            if self.top_n > 1:
                print(f"  SOLUTION #{rank}")
            else:
                print("  OPTIMAL SOLUTION")
            print("-" * 60)
            
            # Selection vector
            selection_str = "[" + ", ".join(str(max(0, s)) for s in selection) + "]"
            print(f"\n  Selection Vector: {selection_str}")
            print("  (1 = Selected, 0 = Not Selected)")
            
            # Detailed table
            print(f"\n  {'#':<5}{'Item':<15}{'Selected':<12}{'Weight':<10}{'Value':<10}")
            print("  " + "-" * 50)
            
            total_weight = 0
            total_value = 0
            selected_items = []
            
            for i in range(self.num_items):
                selected = selection[i]
                sel_str = "YES (1)" if selected == 1 else "NO (0)"
                print(f"  {i+1:<5}{self.item_names[i]:<15}{sel_str:<12}"
                      f"{self.weights[i]:<10}{self.values[i]:<10.2f}")
                
                if selected == 1:
                    total_weight += self.weights[i]
                    total_value += self.values[i]
                    selected_items.append(self.item_names[i])
            
            print("  " + "-" * 50)
            print(f"  {'TOTAL':<5}{'':<15}{'':<12}{total_weight:<10}{total_value:<10.2f}")
            
            print(f"\n  Selected Items: {', '.join(selected_items) if selected_items else 'None'}")
            print(f"  Total Value: {total_value:.2f}")
            print(f"  Weight Used: {total_weight}/{self.capacity}")
            print(f"  Remaining Capacity: {self.capacity - total_weight}")
        
        # Summary table if multiple solutions
        if self.top_n > 1 and len(self.top_solutions) > 1:
            print("\n" + "=" * 60)
            print("                SOLUTIONS SUMMARY")
            print("=" * 60)
            print(f"\n  {'Rank':<6}{'Value':<12}{'Weight':<12}{'Selection':<30}")
            print("  " + "-" * 60)
            
            for rank, (value, selection) in enumerate(self.top_solutions, 1):
                sel_str = "[" + ", ".join(str(max(0, s)) for s in selection) + "]"
                weight = sum(self.weights[i] for i in range(self.num_items) if selection[i] == 1)
                print(f"  {rank:<6}{value:<12.2f}{weight:<12}{sel_str:<30}")
        
        # Final answer box
        print("\n" + "=" * 60)
        print("                  BEST SOLUTION")
        print("=" * 60)
        
        best_sel_str = "[" + ", ".join(str(max(0, s)) for s in self.best_selection) + "]"
        print(f"\n  Selection:  {best_sel_str}")
        print(f"  Max Value:  {self.best_value:.2f}")
        print(f"  Nodes Explored: {self.nodes_explored}")
        print("=" * 60)
