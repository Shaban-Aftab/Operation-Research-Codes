"""
Transportation Problem - Core Engine
=====================================
Base class for transportation problem solving with standard terminology.

Features:
- Problem setup and validation
- Balancing (dummy sources/destinations)  
- Table display utilities
- Cost calculation
- Degeneracy handling

"""

import copy


class TransportationEngine:
    """Base engine for transportation problem solving"""
    
    def __init__(self):
        # Problem dimensions
        self.num_sources = 0
        self.num_destinations = 0
        
        # Core problem data (standard terminology!)
        self.supply = []
        self.demand = []
        self.cost_matrix = []
        self.allocation = []
        
        # Labels
        self.source_names = []
        self.dest_names = []
        
        # Problem state
        self.is_balanced = True
        self.dummy_added = None  # 'source', 'destination', or None
        self.total_cost = 0
        self.iteration = 0
        
        # For optimization reference
        self.original_supply = []
        self.original_demand = []
        
        # Display constants
        self.EPSILON = 1e-10
        self.COL_WIDTH = 12
    
    def configure_problem(self):
        """Get problem configuration from user"""
        print("\n" + "="*70)
        print("        TRANSPORTATION PROBLEM - PROBLEM SETUP")
        print("="*70)
        
        # Get dimensions
        self.num_sources = self._get_positive_int("Number of sources (supply points): ")
        self.num_destinations = self._get_positive_int("Number of destinations (demand points): ")
        
        # Names
        self._setup_names()
        
        # Supply values
        print("\n--- SUPPLY VALUES ---")
        for i in range(self.num_sources):
            val = self._get_nonnegative_float(f"  Supply at {self.source_names[i]}: ")
            self.supply.append(val)
        
        # Demand values  
        print("\n--- DEMAND VALUES ---")
        for j in range(self.num_destinations):
            val = self._get_nonnegative_float(f"  Demand at {self.dest_names[j]}: ")
            self.demand.append(val)
        
        # Cost matrix
        print("\n--- TRANSPORTATION COSTS ---")
        self.cost_matrix = []
        for i in range(self.num_sources):
            row = []
            print(f"\nFrom {self.source_names[i]}:")
            for j in range(self.num_destinations):
                cost = self._get_nonnegative_float(f"  To {self.dest_names[j]}: ")
                row.append(cost)
            self.cost_matrix.append(row)
        
        # Save originals
        self.original_supply = self.supply[:]
        self.original_demand = self.demand[:]
        
        # Display problem
        self.display_problem_summary()
    
    def _setup_names(self):
        """Setup source and destination names"""
        print("\n--- LABELS ---")
        use_custom = input("Use custom names? (y/n): ").lower() == 'y'
        
        if use_custom:
            for i in range(self.num_sources):
                name = input(f"  Source {i+1} name: ").strip() or f"S{i+1}"
                self.source_names.append(name)
            for j in range(self.num_destinations):
                name = input(f"  Destination {j+1} name: ").strip() or f"D{j+1}"
                self.dest_names.append(name)
        else:
            self.source_names = [f"S{i+1}" for i in range(self.num_sources)]
            self.dest_names = [f"D{j+1}" for j in range(self.num_destinations)]
    
    def _get_positive_int(self, prompt):
        """Get positive integer from user"""
        while True:
            try:
                val = int(input(prompt))
                if val > 0:
                    return val
                print("  Must be positive!")
            except ValueError:
                print("  Invalid input!")
    
    def _get_nonnegative_float(self, prompt):
        """Get non-negative float from user"""
        while True:
            try:
                val = float(input(prompt))
                if val >= 0:
                    return val
                print("  Cannot be negative!")
            except ValueError:
                print("  Invalid input!")
    
    def display_problem_summary(self):
        """Display transportation problem summary"""
        print("\n" + "="*70)
        print("           TRANSPORTATION PROBLEM SUMMARY")
        print("="*70)
        
        total_supply = sum(self.supply)
        total_demand = sum(self.demand)
        
        print(f"\nDimensions: {self.num_sources} sources × {self.num_destinations} destinations")
        print(f"Total Supply: {total_supply}")
        print(f"Total Demand: {total_demand}")
        
        # Check balance
        diff = abs(total_supply - total_demand)
        if diff < self.EPSILON:
            print("\n✓ Problem is BALANCED (Supply = Demand)")
            self.is_balanced = True
        else:
            print("\n⚠ Problem is UNBALANCED!")
            if total_supply > total_demand:
                print(f"  Excess supply: {total_supply - total_demand}")
                print("  → Will add dummy destination")
            else:
                print(f"  Shortage: {total_demand - total_supply}")
                print("  → Will add dummy source")
            self.is_balanced = False
        
        print("\n--- Cost Matrix ---")
        self._display_cost_table()
    
    def _display_cost_table(self):
        """Display cost matrix in table format"""
        col_w = self.COL_WIDTH
        
        # Header
        print("\n" + " "*10, end="")
        for name in self.dest_names:
            print(f"{name:^{col_w}}", end="")
        print(f"{'Supply':^{col_w}}")
        
        print(" "*10 + "-" * (col_w * (self.num_destinations + 1)))
        
        # Rows
        for i in range(self.num_sources):
            print(f"{self.source_names[i]:>8} |", end="")
            for j in range(self.num_destinations):
                print(f"{self.cost_matrix[i][j]:^{col_w}.1f}", end="")
            print(f"{self.supply[i]:^{col_w}.0f}")
        
        # Demand row
        print(" "*10 + "-" * (col_w * (self.num_destinations + 1)))
        print(f"{'Demand':>8} |", end="")
        for j in range(self.num_destinations):
            print(f"{self.demand[j]:^{col_w}.0f}", end="")
        print(f"{sum(self.demand):^{col_w}.0f}")
    
    def balance_problem(self):
        """Balance the problem by adding dummy source or destination"""
        total_supply = sum(self.supply)
        total_demand = sum(self.demand)
        
        if abs(total_supply - total_demand) < self.EPSILON:
            print("\n✓ Problem already balanced")
            return
        
        print("\n" + "="*70)
        print("         BALANCING PROBLEM")
        print("="*70)
        
        if total_supply > total_demand:
            # Add dummy destination
            diff = total_supply - total_demand
            print(f"\n→ Adding DUMMY DESTINATION with demand = {diff:.0f}")
            
            self.dest_names.append("Dummy")
            self.demand.append(diff)
            self.num_destinations += 1
            
            # Zero cost to dummy
            for i in range(self.num_sources):
                self.cost_matrix[i].append(0)
            
            self.dummy_added = 'destination'
            
        else:
            # Add dummy source
            diff = total_demand - total_supply
            print(f"\n→ Adding DUMMY SOURCE with supply = {diff:.0f}")
            
            self.source_names.append("Dummy")
            self.supply.append(diff)
            self.num_sources += 1
            
            # Zero cost from dummy
            self.cost_matrix.append([0] * self.num_destinations)
            
            self.dummy_added = 'source'
        
        print("\nBalanced problem:")
        self._display_cost_table()
    
    def initialize_allocation(self):
        """Initialize allocation matrix with None values"""
        self.allocation = [[None for _ in range(self.num_destinations)] 
                          for _ in range(self.num_sources)]
    
    def display_allocation(self, title="Current Allocation"):
        """Display allocation table with costs"""
        col_w = self.COL_WIDTH
        
        print(f"\n{'-'*70}")
        print(f"  {title}")
        print(f"{'-'*70}")
        
        # Header
        print("\n" + " "*10, end="")
        for name in self.dest_names:
            print(f"{name:^{col_w}}", end="")
        print(f"{'Supply':^{col_w}}")
        
        print(" "*10 + "-" * (col_w * (self.num_destinations + 1)))
        
        # Rows with allocations
        for i in range(self.num_sources):
            print(f"{self.source_names[i]:>8} |", end="")
            
            for j in range(self.num_destinations):
                cost = self.cost_matrix[i][j]
                alloc = self.allocation[i][j]
                
                if alloc is not None and alloc > self.EPSILON:
                    cell = f"{cost:.0f}[{alloc:.0f}]"
                elif alloc is not None:
                    cell = f"{cost:.0f}[0]"
                else:
                    cell = f"{cost:.0f}"
                
                print(f"{cell:^{col_w}}", end="")
            
            print(f"{self.supply[i]:^{col_w}.0f}")
        
        # Demand row
        print(" "*10 + "-" * (col_w * (self.num_destinations + 1)))
        print(f"{'Demand':>8} |", end="")
        for j in range(self.num_destinations):
            print(f"{self.demand[j]:^{col_w}.0f}", end="")
        print(f"{sum(self.demand):^{col_w}.0f}")
    
    def calculate_cost(self):
        """Calculate total transportation cost"""
        self.total_cost = 0
        terms = []
        
        for i in range(self.num_sources):
            for j in range(self.num_destinations):
                if self.allocation[i][j] is not None and self.allocation[i][j] > self.EPSILON:
                    cost = self.allocation[i][j] * self.cost_matrix[i][j]
                    self.total_cost += cost
                    terms.append(f"({self.allocation[i][j]:.0f}×{self.cost_matrix[i][j]:.0f})")
        
        print("\n→ Total Cost Calculation:")
        print(f"  = " + " + ".join(terms))
        print(f"  = {self.total_cost:.2f}")
        
        return self.total_cost
    
    def handle_degeneracy(self):
        """Handle degeneracy by adding zero allocations"""
        num_basic = sum(1 for i in range(self.num_sources) 
                       for j in range(self.num_destinations) 
                       if self.allocation[i][j] is not None)
        
        required = self.num_sources + self.num_destinations - 1
        
        if num_basic < required:
            shortage = required - num_basic
            print(f"\n⚠ DEGENERACY DETECTED!")
            print(f"  Current basic variables: {num_basic}")
            print(f"  Required: {required} (m+n-1)")
            print(f"  Adding {shortage} zero allocation(s)...")
            
            # Add zeros to independent cells (simple strategy)
            count = 0
            for i in range(self.num_sources):
                if count >= shortage:
                    break
                for j in range(self.num_destinations):
                    if count >= shortage:
                        break
                    if self.allocation[i][j] is None:
                        self.allocation[i][j] = 0
                        count += 1
                        print(f"    Added [0] at ({self.source_names[i]}, {self.dest_names[j]})")
    
    def export_solution(self):
        """Export solution data for optimization"""
        return {
            'cost_matrix': [row[:] for row in self.cost_matrix],
            'allocation': [row[:] for row in self.allocation],
            'supply': self.supply[:],
            'demand': self.demand[:],
            'source_names': self.source_names[:],
            'dest_names': self.dest_names[:],
            'num_sources': self.num_sources,
            'num_destinations': self.num_destinations,
            'total_cost': self.total_cost
        }
    
    def verify_solution(self):
        """Verify that solution satisfies supply/demand constraints"""
        print("\n" + "="*70)
        print("         SOLUTION VERIFICATION")
        print("="*70)
        
        all_ok = True
        
        # Check supply constraints
        print("\n→ Supply Constraints:")
        for i in range(self.num_sources):
            total = sum(self.allocation[i][j] if self.allocation[i][j] is not None else 0 
                       for j in range(self.num_destinations))
            diff = abs(total - self.supply[i])
            status = "✓" if diff < self.EPSILON else "✗"
            print(f"  {status} {self.source_names[i]}: {total:.2f} = {self.supply[i]:.2f}")
            if diff >= self.EPSILON:
                all_ok = False
        
        # Check demand constraints
        print("\n→ Demand Constraints:")
        for j in range(self.num_destinations):
            total = sum(self.allocation[i][j] if self.allocation[i][j] is not None else 0 
                       for i in range(self.num_sources))
            diff = abs(total - self.demand[j])
            status = "✓" if diff < self.EPSILON else "✗"
            print(f"  {status} {self.dest_names[j]}: {total:.2f} = {self.demand[j]:.2f}")
            if diff >= self.EPSILON:
                all_ok = False
        
        if all_ok:
            print("\n✓ All constraints satisfied!")
        else:
            print("\n✗ Some constraints violated!")
        
        return all_ok
