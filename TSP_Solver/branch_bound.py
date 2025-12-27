"""
Branch and Bound Algorithm for TSP
===================================

Algorithm:
1. Start from initial city
2. Calculate lower bounds
3. Branch to next cities
4. Prune if bound >= best cost
"""

from tsp_core import TSPEngine
from collections import deque


class TSPNode:
    """Node in the Branch and Bound tree"""
    
    def __init__(self, node_id, path, cost, bound, level, parent_id=-1):
        self.node_id = node_id
        self.path = path[:]  # Cities visited so far
        self.cost = cost      # Cost so far
        self.bound = bound    # Lower bound estimate
        self.level = level    # Depth in tree
        self.parent_id = parent_id
        self.children = []    # Child node IDs
        self.status = "ACTIVE"  # ROOT, ACTIVE, BRANCHED, PRUNED, SOLUTION, NO_RETURN
        self.is_optimal = False
    
    def __lt__(self, other):
        """For priority queue comparison"""
        return self.bound < other.bound


class BranchAndBoundTSP(TSPEngine):
    """TSP solver using Branch and Bound"""
    
    def __init__(self):
        super().__init__()
        self.nodes = {}  # All nodes in tree
        self.node_counter = 0
        self.root_id = 0
        self.optimal_path_ids = []
    
    def calculate_lower_bound(self, path, current_cost):
        """
        Calculate lower bound for current partial tour
       
        Bound = current_cost +
                min outgoing edge from last city +
                sum of min outgoing edges for unvisited cities
        """
        n = self.num_cities
        visited = set(path)
        bound = current_cost
        
        # Minimum outgoing edge from last city in path
        if path:
            last_city = path[-1]
            if len(visited) < n:
                min_edge = self.INF
                for j in range(n):
                    # Can visit unvisited cities or return to start at end
                    can_visit = (j not in visited) or (len(visited) == n - 1 and j == self.start_city)
                    if can_visit and self.distance_matrix[last_city][j] < min_edge:
                        min_edge = self.distance_matrix[last_city][j]
                
                if min_edge < self.INF - 1:
                    bound += min_edge
        
        # Minimum outgoing edges for unvisited cities
        for i in range(n):
            if i not in visited:
                min_out = self.INF
                for j in range(n):
                    # Can go to unvisited or back to start
                    can_go = (i != j) and (j not in visited or j == self.start_city)
                    if can_go and self.distance_matrix[i][j] < min_out:
                        min_out = self.distance_matrix[i][j]
                
                if min_out < self.INF - 1:
                    bound += min_out
        
        return bound
    
    def solve(self):
        """Solve TSP using Branch and Bound"""
        print("\n" + "=" * 70)
        print("      SOLVING TSP - BRANCH AND BOUND")
        print("=" * 70)
        
        n = self.num_cities
        
        if n <= 1:
            print("\nNeed at least 2 cities!")
            return False
        
        # Verify connectivity
        self.verify_connectivity()
        
        # Initialize root node
        root_path = [self.start_city]
        root_cost = 0
        root_bound = self.calculate_lower_bound(root_path, root_cost)
        
        self.root_id = self.node_counter
        root = TSPNode(self.node_counter, root_path, root_cost, root_bound, 0, -1)
        root.status = "ROOT"
        self.nodes[self.node_counter] = root
        self.node_counter += 1
        
        print("\n>>> ROOT NODE:")
        print(f"    Path: [{self.city_names[self.start_city]}]")
        print(f"    Cost: {root_cost}")
        print(f"    Lower Bound: {root_bound:.1f}")
        
        # Priority queue (min-heap by bound)
        import heapq
        pq = [(root_bound, self.root_id)]
        
        iteration = 0
        
        print("\n>>> BRANCHING:")
        
        while pq:
            iteration += 1
            
            current_bound, current_id = heapq.heappop(pq)
            current = self.nodes[current_id]
            
            # Skip if bound is worse than best
            if current_bound >= self.best_cost:
                current.status = "PRUNED"
                continue
            
            print("\n" + "-" * 50)
            print(f"Iteration {iteration}: Expanding Node {current_id}")
            print(f"  Path: [{' -> '.join([self.city_names[c] for c in current.path])}]")
            print(f"  Cost: {current.cost:.0f}, Bound: {current.bound:.1f}")
            
            # Check if complete tour
            if len(current.path) == n:
                # Add return to start
                return_cost = self.distance_matrix[current.path[-1]][self.start_city]
                
                if return_cost < self.INF - 1:
                    total_cost = current.cost + return_cost
                    
                    print(f"  Complete tour found!")
                    print(f"  Return to start: {return_cost:.0f}")
                    print(f"  Total cost: {total_cost:.0f}")
                    
                    if total_cost < self.best_cost:
                        self.best_cost = total_cost
                        self.best_tour = current.path + [self.start_city]
                        current.status = "SOLUTION"
                        print(f"  >>> NEW BEST SOLUTION!")
                        
                        # Update optimal path
                        self.optimal_path_ids = []
                        trace_id = current_id
                        while trace_id != -1:
                            self.optimal_path_ids.insert(0, trace_id)
                            trace_id = self.nodes[trace_id].parent_id
                    else:
                        current.status = "PRUNED"
                else:
                    current.status = "NO_RETURN"
                    print(f"  No return path to start!")
                continue
            
            # Branch to unvisited cities
            visited = set(current.path)
            last_city = current.path[-1]
            
            current.status = "BRANCHED"
            
            for next_city in range(n):
                if next_city in visited:
                    continue
                if self.distance_matrix[last_city][next_city] >= self.INF - 1:
                    continue
                
                new_path = current.path + [next_city]
                new_cost = current.cost + self.distance_matrix[last_city][next_city]
                new_bound = self.calculate_lower_bound(new_path, new_cost)
                
                print(f"  -> Branch to {self.city_names[next_city]}: "
                      f"cost={new_cost:.0f}, bound={new_bound:.1f}", end="")
                
                # Create child node
                child_id = self.node_counter
                child = TSPNode(child_id, new_path, new_cost, new_bound, 
                               current.level + 1, current_id)
                self.nodes[child_id] = child
                current.children.append(child_id)
                self.node_counter += 1
                
                if new_bound >= self.best_cost:
                    print(" [PRUNED]")
                    child.status = "PRUNED"
                else:
                    print(" [EXPLORE]")
                    child.status = "ACTIVE"
                    heapq.heappush(pq, (new_bound, child_id))
        
        # Mark optimal path nodes
        for node_id in self.optimal_path_ids:
            self.nodes[node_id].is_optimal = True
        
        print("\n" + "=" * 70)
        print(f"✓ Branch and Bound Complete")
        print(f"  Nodes explored: {len(self.nodes)}")
        print("=" * 70)
        
        return len(self.best_tour) > 0
