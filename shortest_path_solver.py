"""
SHORTEST/LONGEST PATH SOLVER

===============================================================

Features:
- Shortest OR Longest Path
- Backward Dynamic Programming for DAGs
- Bellman-Ford for graphs with cycles
- Cycle detection using DFS

===============================================================
"""


class ShortestPathSolver:
    """Complete solver for shortest/longest path problems"""
    
    def __init__(self):
        self.num_nodes = 0
        self.num_edges = 0
        self.edges = {}  # forward edges: {from: [(to, cost), ...]}
        self.reverse_edges = {}  # backward edges
        self.node_names = {}
        self.cost = {}  # f(i) values
        self.next_node = {}  # optimal next node
        self.source = 1
        self.destination = 0
        self.is_minimization = True
        self.has_cycle = False
        self.cycle_path = []
        self.processed_nodes = set()
        
        self.INF = float('inf')
        self.NEG_INF = float('-inf')
    
    def get_user_input(self):
        """Get problem input from user"""
        print("\n" + "=" * 60)
        print("       SHORTEST/LONGEST PATH SOLVER")
        print("         (Stage Graph / Network)")
        print("=" * 60)
        
        # Problem type
        print("\nProblem Type:")
        print("  1. Shortest Path (Minimization)")
        print("  2. Longest Path (Maximization)")
        
        while True:
            try:
                choice = int(input("\nEnter choice (1 or 2): "))
                if choice in [1, 2]:
                    self.is_minimization = (choice == 1)
                    break
                print("Please enter 1 or 2")
            except ValueError:
                print("Invalid input!")
        
        problem_type = "SHORTEST PATH" if self.is_minimization else "LONGEST PATH"
        print(f"\n>>> Selected: {problem_type}")
        
        # Number of nodes
        while True:
            try:
                self.num_nodes = int(input("\nHow many nodes/stages? "))
                if self.num_nodes > 1:
                    break
                print("Must have at least 2 nodes")
            except ValueError:
                print("Invalid input!")
        
        self.destination = self.num_nodes
        
        # Node names
        print(f"\n>>> Nodes: 1 (Source) to {self.num_nodes} (Destination)")
        custom = input("\nCustom node names? (y/n, default=n): ").lower() == 'y'
        
        if custom:
            for i in range(1, self.num_nodes + 1):
                name = input(f"  Node {i}: ").strip()
                self.node_names[i] = name if name else str(i)
        else:
            for i in range(1, self.num_nodes + 1):
                self.node_names[i] = str(i)
        
        # Initialize edges
        for i in range(1, self.num_nodes + 1):
            self.edges[i] = []
            self.reverse_edges[i] = []
        
        # Get edges
        print("\n" + "-" * 60)
        print("ENTER COST MATRIX")
        print("-" * 60)
        print("Enter cost from each node to connected nodes.")
        print("Use 'x', '-', or 0 for NO connection.")
        
        for i in range(1, self.num_nodes + 1):
            print(f"\nNode {i} connections:")
            
            for j in range(1, self.num_nodes + 1):
                if i == j or j < i:
                    continue  # Skip self-loops and backward edges
                
                while True:
                    inp = input(f"  {i} -> {j}: ").strip().lower()
                    
                    if inp in ['x', '-', '0', 'n', 'no', '']:
                        break  # No connection
                    
                    try:
                        cost = float(inp)
                        if cost < 0:
                            print("    Cost cannot be negative")
                            continue
                        
                        self.edges[i].append((j, cost))
                        self.reverse_edges[j].append((i, cost))
                        self.num_edges += 1
                        break
                    except:
                        print("    Enter a number or 'x' for no connection")
        
        self.display_cost_matrix()
        self.display_graph()
    
    def display_cost_matrix(self):
        """Display the cost matrix"""
        print("\n" + "=" * 60)
        print("              COST MATRIX")
        print("=" * 60)
        
        # Build matrix
        matrix = [['-' for _ in range(self.num_nodes)] for _ in range(self.num_nodes)]
        
        for i in self.edges:
            for j, cost in self.edges[i]:
                matrix[i-1][j-1] = f"{cost:.0f}" if cost == int(cost) else f"{cost:.1f}"
        
        # Print matrix
        col_width = 8
        print(f"\n{'':>6} |", end="")
        for j in range(1, self.num_nodes + 1):
            print(f"{self.node_names[j]:^{col_width}}", end="")
        print()
        print("-" * (6 + col_width * self.num_nodes + 1))
        
        for i in range(1, self.num_nodes + 1):
            print(f"{self.node_names[i]:>5} |", end="")
            for j in range(1, self.num_nodes + 1):
                print(f"{matrix[i-1][j-1]:^{col_width}}", end="")
            print()
        
        print("-" * (6 + col_width * self.num_nodes + 1))
        print(f"\nTotal edges: {self.num_edges}")
        print("('-' = no connection)")
        print("=" * 60)
    
    def detect_cycle_dfs(self, node, path, color):
        """DFS for cycle detection"""
        WHITE, GRAY, BLACK = 0, 1, 2
        color[node] = GRAY
        path.append(node)
        
        for next_node, _ in self.edges[node]:
            if color[next_node] == GRAY:
                # Found cycle
                idx = path.index(next_node)
                self.cycle_path = path[idx:] + [next_node]
                return True
            elif color[next_node] == WHITE:
                if self.detect_cycle_dfs(next_node, path, color):
                    return True
        
        path.pop()
        color[node] = BLACK
        return False
    
    def detect_cycle(self):
        """Detect if graph has cycles"""
        color = [0] * (self.num_nodes + 1)  # WHITE
        
        for node in range(1, self.num_nodes + 1):
            if color[node] == 0:
                if self.detect_cycle_dfs(node, [], color):
                    self.has_cycle = True
                    return True
        
        self.has_cycle = False
        return False
    
    def display_graph(self):
        """Display graph structure"""
        problem_type = "SHORTEST PATH" if self.is_minimization else "LONGEST PATH"
        
        print("\n" + "=" * 60)
        print(f"            GRAPH STRUCTURE ({problem_type})")
        print("=" * 60)
        
        print(f"\nSource: Node {self.node_names[1]}")
        print(f"Destination: Node {self.node_names[self.destination]}")
        
        # Cycle detection
        print("\n" + "-" * 50)
        print("CYCLE DETECTION:")
        print("-" * 50)
        
        if self.detect_cycle():
            print("\n  [!] CYCLE DETECTED IN GRAPH!")
            print("  Cycle: " + " -> ".join([self.node_names[n] for n in self.cycle_path]))
            print("\n  Using Bellman-Ford algorithm (handles cycles).")
        else:
            print("\n  [OK] No cycle detected. Graph is a DAG.")
            print("  Using Backward Dynamic Programming.")
    
    def solve_bellman_ford(self):
        """Solve using Bellman-Ford (for cyclic graphs)"""
        problem_type = "SHORTEST" if self.is_minimization else "LONGEST"
        
        print("\n" + "=" * 60)
        print(f"      SOLVING: {problem_type} PATH (Bellman-Ford)")
        print("=" * 60)
        
        # Initialize
        for i in range(1, self.num_nodes + 1):
            self.cost[i] = self.INF if self.is_minimization else self.NEG_INF
            self.next_node[i] = 0
        
        self.cost[self.destination] = 0
        
        print(f"\n>>> Initialization: f({self.node_names[self.destination]}) = 0")
        
        # Iterate
        print("\n>>> Iterations:")
        
        for iter in range(1, self.num_nodes + 1):
            print(f"\n--- Iteration {iter} ---")
            updated = False
            
            for i in range(1, self.num_nodes + 1):
                for j, edge_cost in self.edges[i]:
                    if abs(self.cost[j]) == self.INF:
                        continue
                    
                    new_cost = self.cost[j] + edge_cost
                    
                    should_update = False
                    if self.is_minimization and new_cost < self.cost[i] - 1e-9:
                        should_update = True
                    elif not self.is_minimization and new_cost > self.cost[i] + 1e-9:
                        should_update = True
                    
                    if should_update:
                        print(f"    f({self.node_names[i]}): {self.cost[i]} -> {new_cost} via {self.node_names[j]}")
                        self.cost[i] = new_cost
                        self.next_node[i] = j
                        updated = True
            
            if not updated:
                print("    No updates - converged!")
                break
    
    def solve_backward_dp(self):
        """Solve using Backward DP (for DAGs)"""
        problem_type = "SHORTEST" if self.is_minimization else "LONGEST"
        
        print("\n" + "=" * 60)
        print(f"      SOLVING: {problem_type} PATH (Backward DP)")
        print("=" * 60)
        
        # Initialize
        for i in range(1, self.num_nodes + 1):
            self.cost[i] = self.INF if self.is_minimization else self.NEG_INF
            self.next_node[i] = 0
        
        self.cost[self.destination] = 0
        self.processed_nodes.add(self.destination)
        
        print(f"\n>>> Initialization: f({self.node_names[self.destination]}) = 0")
        print("\n>>> Backward Pass:")
        
        # Process from destination-1 to source
        for node in range(self.num_nodes - 1, 0, -1):
            print(f"\n{'-'*50}")
            print(f"Processing Node {node} ({self.node_names[node]})")
            print("-" * 50)
            
            if not self.edges[node]:
                print("    No outgoing edges")
                continue
            
            func_type = "min" if self.is_minimization else "max"
            print(f"    f({self.node_names[node]}) = {func_type}{{ c(i,j) + f(j) }}")
            print("\n    Evaluating options:")
            
            best_cost = self.INF if self.is_minimization else self.NEG_INF
            best_next = 0
            
            for j, edge_cost in self.edges[node]:
                if abs(self.cost[j]) == self.INF:
                    print(f"      -> {self.node_names[j]}: {edge_cost} + INF = INF (skip)")
                    continue
                
                total_cost = edge_cost + self.cost[j]
                print(f"      -> {self.node_names[j]}: {edge_cost} + {self.cost[j]} = {total_cost}", end="")
                
                is_better = False
                if self.is_minimization and total_cost < best_cost:
                    is_better = True
                elif not self.is_minimization and total_cost > best_cost:
                    is_better = True
                
                if is_better:
                    best_cost = total_cost
                    best_next = j
                    print(f" <-- {'MIN' if self.is_minimization else 'MAX'}")
                else:
                    print()
            
            if best_next > 0:
                self.cost[node] = best_cost
                self.next_node[node] = best_next
                print(f"\n    => f({self.node_names[node]}) = {best_cost}, next = {self.node_names[best_next]}")
            
            self.processed_nodes.add(node)
    
    def solve(self):
        """Main solve method"""
        if self.has_cycle:
            self.solve_bellman_ford()
        else:
            self.solve_backward_dp()
    
    def display_solution(self):
        """Display final solution"""
        problem_type = "SHORTEST" if self.is_minimization else "LONGEST"
        cost_type = "Minimum" if self.is_minimization else "Maximum"
        
        print("\n" + "=" * 60)
        print(f"                FINAL {problem_type} PATH")
        print("=" * 60)
        
        # Check if path exists
        if abs(self.cost[self.source]) == self.INF:
            print("\n>>> No path exists from source to destination!")
            return
        
        # Reconstruct path
        print("\n>>> OPTIMAL PATH:")
        print("-" * 50)
        
        path = []
        current = self.source
        total_cost = 0
        
        while current != 0 and current != self.destination:
            path.append(current)
            next = self.next_node.get(current, 0)
            
            if next == 0:
                break
            
            # Find edge cost
            edge_cost = 0
            for j, cost in self.edges[current]:
                if j == next:
                    edge_cost = cost
                    break
            
            total_cost += edge_cost
            current = next
        
        path.append(self.destination)
        
        # Display
        print("\n    PATH: " + " -> ".join([self.node_names[i] for i in path]))
        print("\n    DETAILED PATH:")
        
        for i in range(len(path) - 1):
            from_node = path[i]
            to_node = path[i + 1]
            
            edge_cost = 0
            for j, cost in self.edges[from_node]:
                if j == to_node:
                    edge_cost = cost
                    break
            
            print(f"      {self.node_names[from_node]} --({edge_cost})-> {self.node_names[to_node]}")
        
        print("\n" + "=" * 50)
        print(f"{cost_type} Path Cost = {self.cost[self.source]:.1f}")
        print("=" * 50)
        
        # Show all paths
        self.display_all_paths()
    
    def find_all_paths(self, current, dest, path, path_cost, all_paths, visited):
        """Recursively find all paths"""
        path.append(current)
        visited.add(current)
        
        if current == dest:
            all_paths.append((path[:], path_cost))
        else:
            for next_node, edge_cost in self.edges[current]:
                if next_node not in visited:
                    self.find_all_paths(next_node, dest, path, path_cost + edge_cost, all_paths, visited)
        
        path.pop()
        visited.remove(current)
    
    def display_all_paths(self):
        """Display all possible paths"""
        print("\n" + "=" * 60)
        print("              ALL POSSIBLE PATHS")
        print("=" * 60)
        
        all_paths = []
        self.find_all_paths(self.source, self.destination, [], 0, all_paths, set())
        
        if not all_paths:
            print("\n>>> No paths found!")
            return
        
        # Sort by cost
        all_paths.sort(key=lambda x: x[1], reverse=not self.is_minimization)
        
        optimal_cost = all_paths[0][1]
        
        print(f"\nTotal paths found: {len(all_paths)}")
        print("-" * 60)
        
        for i, (path, cost) in enumerate(all_paths):
            is_optimal = abs(cost - optimal_cost) < 1e-9
            marker = "*** " if is_optimal else "    "
            
            print(f"\n{marker}Path {i+1}: " + " -> ".join([self.node_names[n] for n in path]))
            print(f"    Cost: {cost:.1f}", end="")
            if is_optimal:
                print(" <-- OPTIMAL", end="")
            print()
        
        print("\n" + "-" * 60)
        print("*** = Optimal path(s)")


def main():
    """Main application"""
    print("\n" + "=" * 60)
    print("|         SHORTEST/LONGEST PATH SOLVER                    |")
    print("|      Dynamic Programming & Bellman-Ford                 |")
    print("|            With Cycle Detection                         |")
    print("=" * 60)
    
    while True:
        solver = ShortestPathSolver()
        solver.get_user_input()
        
        input("\nPress ENTER to start solving...")
        solver.solve()
        solver.display_solution()
        
        print("\n" + "-" * 60)
        choice = input("\nSolve another problem? (y/n): ").lower()
        if choice != 'y':
            print("\n" + "=" * 60)
            print("Thank you for using Shortest Path Solver!")
            print("=" * 60 + "\n")
            break


if __name__ == "__main__":
    main()
