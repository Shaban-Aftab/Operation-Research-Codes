"""
Tree Visualization for Branch and Bound
========================================
Draws the decision tree showing branching and pruning.
"""

from branch_bound import BranchAndBoundTSP


class TreeVisualizer(BranchAndBoundTSP):
    """TSP solver with tree visualization"""
    
    def draw_tree(self):
        """Draw the complete Branch and Bound tree"""
        print("\n" + "=" * 70)
        print("                BRANCH AND BOUND TREE")
        print("=" * 70)
        
        print("\nLEGEND:")
        print("  [*] = Optimal Path")
        print("  [S] = Solution Found")
        print("  [P] = Pruned")
        print("  [B] = Branched")
        print()
        
        self._draw_node(self.root_id, "", True)
    
    def _draw_node(self, node_id, prefix, is_last):
        """Recursively draw tree node"""
        if node_id not in self.nodes:
            return
        
        node = self.nodes[node_id]
        
        # Determine marker
        if node.is_optimal:
            marker = "[*]"
        elif node.status == "SOLUTION":
            marker = "[S]"
        elif node.status == "PRUNED":
            marker = "[P]"
        elif node.status == "BRANCHED":
            marker = "[B]"
        else:
            marker = "[ ]"
        
        # Determine connector
        if node.level == 0:
            connector = ""
            new_prefix = ""
        else:
            connector = "`-- " if is_last else "|-- "
            new_prefix = prefix + ("    " if is_last else "|   ")
        
        # Build path string
        path_str = "->".join([self.city_names[c][:3] for c in node.path])
        
        # Print node
        print(f"{prefix}{connector}{marker} Node {node_id}: "
              f"[{path_str}] cost={node.cost:.0f} bound={node.bound:.1f}")
        
        # Draw children
        for i, child_id in enumerate(node.children):
            self._draw_node(child_id, new_prefix, i == len(node.children) - 1)
    
    def display_solution(self):
        """Display optimal solution"""
        print("\n" + "=" * 70)
        print("              OPTIMAL TSP SOLUTION")
        print("=" * 70)
        
        if not self.best_tour:
            print("\nNo valid tour found!")
            print("Check if all cities are connected.")
            return
        
        print("\nOPTIMAL TOUR:")
        print("-" * 50)
        
        # Tour path
        print("\n  ", end="")
        for i, city_idx in enumerate(self.best_tour):
            print(self.city_names[city_idx], end="")
            if i < len(self.best_tour) - 1:
                print(" -> ", end="")
        print()
        
        # Detailed path
        print("\nDETAILED PATH:")
        for i in range(len(self.best_tour) - 1):
            from_city = self.best_tour[i]
            to_city = self.best_tour[i + 1]
            dist = self.distance_matrix[from_city][to_city]
            print(f"  {self.city_names[from_city]} --({dist:.0f})--> {self.city_names[to_city]}")
        
        print("\n" + "=" * 50)
        print(f"MINIMUM TOUR COST = {self.best_cost:.0f}")
        print("=" * 50)
        
        print(f"\nNodes explored: {len(self.nodes)}")
    
    def solve_and_visualize(self):
        """Complete solve with tree visualization"""
        success = self.solve()
        
        if success:
            self.draw_tree()
            self.display_solution()
        else:
            print("\n✗ Could not find valid tour")
        
        return success
