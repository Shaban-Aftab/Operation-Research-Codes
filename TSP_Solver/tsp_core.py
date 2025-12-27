"""
TSP (Traveling Salesman Problem) - Core Engine
===============================================

Features:
- Problem configuration (cities, distances)
- Distance matrix input (2 methods)
- Validation
- Display utilities
"""

import copy


class TSPEngine:
    """Base engine for TSP problem solving"""
    
    def __init__(self):
        # Problem data
        self.num_cities = 0
        self.city_names = []
        self.distance_matrix = []
        self.start_city = 0
        
        # Solution data
        self.best_tour = []
        self.best_cost = float('inf')
        
        # Constants
        self.INF = float('inf')
        self.EPSILON = 1e-10
    
    def configure_problem(self):
        """Get problem configuration from user"""
        print("\n" + "=" * 70)
        print("        TRAVELING SALESMAN PROBLEM (TSP)")
        print("            Branch and Bound Solver")
        print("=" * 70)
        
        # Number of cities
        while True:
            try:
                self.num_cities = int(input("\nEnter the number of cities: "))
                if self.num_cities >= 2:
                    break
                print("Number of cities must be at least 2")
            except ValueError:
                print("Invalid input!")
        
        # City names
        print("\n--- CITY NAMES ---")
        use_default = input("Use default city names? (y/n): ").lower() == 'y'
        
        if use_default:
            self.city_names = [f"City{i+1}" for i in range(self.num_cities)]
        else:
            self.city_names = []
            for i in range(self.num_cities):
                name = input(f"  Enter name for City {i+1}: ").strip()
                if not name:
                    name = f"City{i+1}"
                self.city_names.append(name)
        
        # Display cities
        print("\nCities registered:")
        for i, name in enumerate(self.city_names):
            print(f"  {i+1}: {name}")
        
        # Starting city
        print("\n--- STARTING CITY ---")
        while True:
            try:
                start_num = int(input(f"Enter starting city (1-{self.num_cities}): "))
                if 1 <= start_num <= self.num_cities:
                    self.start_city = start_num - 1
                    print(f"  Starting from: {self.city_names[self.start_city]}")
                    break
                print(f"  Please enter a number between 1 and {self.num_cities}")
            except ValueError:
                print("Invalid input!")
        
        # Initialize distance matrix
        self.distance_matrix = [[self.INF for _ in range(self.num_cities)] 
                               for _ in range(self.num_cities)]
        
        # Choose input method
        print("\n--- INPUT METHOD ---")
        print("1. Enter distance matrix directly")
        print("2. Enter edges one by one")
        
        while True:
            try:
                method = int(input("\nChoose input method (1 or 2): "))
                if method in [1, 2]:
                    break
                print("Please enter 1 or 2")
            except ValueError:
                print("Invalid input!")
        
        if method == 1:
            self._input_matrix()
        else:
            self._input_edges()
        
        self.display_problem()
    
    def _input_matrix(self):
        """Input distances as matrix"""
        print("\n--- DISTANCE MATRIX INPUT ---")
        print("Enter distance from each city to every other city.")
        print("Use 'x', '-', or 0 for no connection/infinity.")
        print("Diagonal will be set to infinity automatically.\n")
        
        for i in range(self.num_cities):
            print(f"\nRow {i+1} ({self.city_names[i]}):")
            for j in range(self.num_cities):
                if i == j:
                    self.distance_matrix[i][j] = self.INF
                    print(f"  {self.city_names[i]} -> {self.city_names[j]}: inf (same city)")
                else:
                    while True:
                        inp = input(f"  {self.city_names[i]} -> {self.city_names[j]}: ").lower()
                        
                        if inp in ['x', '-', 'inf', 'm', '']:
                            self.distance_matrix[i][j] = self.INF
                            break
                        
                        try:
                            dist = float(inp)
                            if dist < 0:
                                print("    Distance cannot be negative.")
                                continue
                            if dist == 0:
                                self.distance_matrix[i][j] = self.INF
                            else:
                                self.distance_matrix[i][j] = dist
                            break
                        except ValueError:
                            print("    Invalid input.")
        
        print("\nDistance matrix entered successfully!")
    
    def _input_edges(self):
        """Input distances as edges"""
        print("\n--- CONNECTIONS (EDGES) ---")
        print("Enter which cities are connected and their distances.")
        print("Type 0 for 'from city' when finished.\n")
        
        edge_count = 0
        while True:
            print(f"Edge {edge_count + 1}:")
            
            try:
                from_num = int(input(f"  From city (1-{self.num_cities}, or 0 to finish): "))
                
                if from_num == 0:
                    break
                if from_num < 1 or from_num > self.num_cities:
                    print("    Invalid city number.")
                    continue
                from_idx = from_num - 1
                
                to_num = int(input(f"  To city (1-{self.num_cities}): "))
                
                if to_num < 1 or to_num > self.num_cities:
                    print("    Invalid city number.")
                    continue
                to_idx = to_num - 1
                
                if from_idx == to_idx:
                    print("    Cannot connect a city to itself.")
                    continue
                
                dist = float(input("  Distance: "))
                
                if dist <= 0:
                    print("    Distance must be positive.")
                    continue
                
                # Add edge (both directions for symmetric TSP)
                self.distance_matrix[from_idx][to_idx] = dist
                self.distance_matrix[to_idx][from_idx] = dist
                
                print(f"    Added: {self.city_names[from_idx]} <--{dist}--> {self.city_names[to_idx]}\n")
                edge_count += 1
                
            except ValueError:
                print("    Invalid input.")
        
        if edge_count == 0:
            print("\nWarning: No edges entered!")
    
    def display_problem(self):
        """Display TSP problem summary"""
        print("\n" + "=" * 70)
        print("              TSP PROBLEM")
        print("=" * 70)
        
        print(f"\nNumber of Cities: {self.num_cities}")
        print(f"Starting City: {self.city_names[self.start_city]}")
        
        # City connections
        print("\n" + "-" * 50)
        print("CITY CONNECTIONS:")
        print("-" * 50)
        
        for i in range(self.num_cities):
            connections = []
            for j in range(self.num_cities):
                if i != j and self.distance_matrix[i][j] < self.INF - 1:
                    connections.append(f"{self.city_names[j]}({self.distance_matrix[i][j]:.0f})")
            
            print(f"  {self.city_names[i]} --> ", end="")
            if connections:
                print(", ".join(connections))
            else:
                print("(no connections)")
        
        # Distance matrix
        print("\n" + "-" * 50)
        print("DISTANCE MATRIX:")
        print("-" * 50)
        
        # Header
        col_width = 10
        print(" " * 8, end="")
        for name in self.city_names:
            print(f"{name[:7]:^{col_width}}", end="")
        print()
        print(" " * 8 + "-" * (col_width * self.num_cities))
        
        # Rows
        for i in range(self.num_cities):
            print(f"{self.city_names[i][:6]:>6} |", end="")
            for j in range(self.num_cities):
                if self.distance_matrix[i][j] >= self.INF - 1:
                    print(f"{'--':^{col_width}}", end="")
                else:
                    print(f"{self.distance_matrix[i][j]:^{col_width}.0f}", end="")
            
            if i == self.start_city:
                print("  <-- START", end="")
            print()
        
        print("-" * 50)
    
    def verify_connectivity(self):
        """Check if all cities are connected"""
        print("\n→ Checking connectivity...")
        all_connected = True
        
        for i in range(self.num_cities):
            has_connection = False
            for j in range(self.num_cities):
                if i != j and self.distance_matrix[i][j] < self.INF - 1:
                    has_connection = True
                    break
            
            if not has_connection:
                print(f"  ⚠ Warning: {self.city_names[i]} has no connections!")
                all_connected = False
        
        if all_connected:
            print("  ✓ All cities are connected")
        
        return all_connected
    
    def get_distance(self, from_city, to_city):
        """Get distance between two cities"""
        return self.distance_matrix[from_city][to_city]
    
    def display_tour(self, tour, cost):
        """Display a tour solution"""
        print("\n" + "=" * 60)
        print("              TOUR SOLUTION")
        print("=" * 60)
        
        if not tour:
            print("\nNo valid tour found!")
            return
        
        print("\nTOUR PATH:")
        print("-" * 50)
        
        # Display path
        print("\n  ", end="")
        for i, city_idx in enumerate(tour):
            print(self.city_names[city_idx], end="")
            if i < len(tour) - 1:
                print(" -> ", end="")
        print()
        
        # Detailed path with distances
        print("\nDETAILED PATH:")
        total = 0
        for i in range(len(tour) - 1):
            from_city = tour[i]
            to_city = tour[i + 1]
            dist = self.distance_matrix[from_city][to_city]
            total += dist
            print(f"  {self.city_names[from_city]} --({dist:.0f})--> {self.city_names[to_city ]}")
        
        print("\n" + "=" * 50)
        print(f"TOTAL TOUR COST = {cost:.0f}")
        print("=" * 50)
