"""
0/1 Knapsack Problem - Core Engine
===================================
Base class for knapsack solving with input and constraints.
"""

class KnapsackEngine:
    """Base engine for 0/1 Knapsack problem"""
    
    def __init__(self):
        self.num_items = 0
        self.capacity = 0
        self.weights = []
        self.values = []
        self.item_names = []
        self.excluded_items = []  # Items to NOT pick
        self.required_items = []  # Items to MUST pick
        
    def configure_problem(self):
        """Get problem input from user"""
        print("\n" + "=" * 70)
        print("         0/1 KNAPSACK PROBLEM SOLVER")
        print("           (Dynamic Programming)")
        print("=" * 70)
        
        # Number of items
        while True:
            try:
                self.num_items = int(input("\nEnter the number of items: "))
                if self.num_items > 0:
                    break
                print("Number of items must be positive")
            except ValueError:
                print("Invalid input!")
        
        # Capacity
        while True:
            try:
                self.capacity = int(input("Enter the knapsack capacity: "))
                if self.capacity > 0:
                    break
                print("Capacity must be positive")
            except ValueError:
                print("Invalid input!")
        
        # Get item details
        print("\n--- ITEM DETAILS ---")
        for i in range(self.num_items):
            print(f"\nItem {i+1}:")
            
            # Name
            name = input(f"  Item name (or press Enter for 'Item {i+1}'): ").strip()
            if not name:
                name = f"Item {i+1}"
            self.item_names.append(name)
            
            # Weight
            while True:
                try:
                    weight = int(input(f"  Weight of {name}: "))
                    if weight > 0:
                        self.weights.append(weight)
                        break
                    print("  Weight must be positive")
                except ValueError:
                    print("  Invalid input!")
            
            # Value
            while True:
                try:
                    value = float(input(f"  Value of {name}: "))
                    if value >= 0:
                        self.values.append(value)
                        break
                    print("  Value must be non-negative")
                except ValueError:
                    print("  Invalid input!")
        
        # Constraints
        self._get_constraints()
        self.display_problem()
    
    def _get_constraints(self):
        """Get item selection constraints"""
        print("\n" + "-" * 60)
        print("         ITEM SELECTION CONSTRAINTS")
        print("-" * 60)
        
        # Excluded items
        exclude = input("\nExclude any items? (y/n): ").lower() == 'y'
        if exclude:
            print("\nAvailable items:")
            for i in range(self.num_items):
                print(f"  {i+1}. {self.item_names[i]} (w={self.weights[i]}, v={self.values[i]})")
            
            exclude_input = input("Enter item numbers to EXCLUDE (comma-separated): ").strip()
            if exclude_input:
                for num_str in exclude_input.split(','):
                    try:
                        num = int(num_str.strip())
                        if 1 <= num <= self.num_items:
                            self.excluded_items.append(num - 1)
                            print(f"  X {self.item_names[num-1]} will be EXCLUDED")
                    except:
                        pass
        
        # Required items
        require = input("\nRequire any items to be picked? (y/n): ").lower() == 'y'
        if require:
            print("\nAvailable items (not excluded):")
            for i in range(self.num_items):
                if i not in self.excluded_items:
                    print(f"  {i+1}. {self.item_names[i]} (w={self.weights[i]}, v={self.values[i]})")
            
            require_input = input("Enter item numbers to REQUIRE (comma-separated): ").strip()
            if require_input:
                for num_str in require_input.split(','):
                    try:
                        num = int(num_str.strip())
                        if 1 <= num <= self.num_items and (num-1) not in self.excluded_items:
                            self.required_items.append(num - 1)
                            print(f"  + {self.item_names[num-1]} will be REQUIRED")
                    except:
                        pass
    
    def display_problem(self):
        """Display problem summary"""
        print("\n" + "=" * 70)
        print("                 KNAPSACK PROBLEM")
        print("=" * 70)
        
        print(f"\nKnapsack Capacity: {self.capacity}")
        print(f"Number of Items: {self.num_items}")
        
        # Show constraints
        if self.excluded_items or self.required_items:
            print("\n" + "-" * 50)
            print("USER-DEFINED CONSTRAINTS:")
            if self.excluded_items:
                print(f"  X EXCLUDED: {', '.join([self.item_names[i] for i in self.excluded_items])}")
            if self.required_items:
                print(f"  + REQUIRED: {', '.join([self.item_names[i] for i in self.required_items])}")
        
        # Item table
        print("\n" + "-" * 60)
        print(f"{'Item':<15}{'Weight':<10}{'Value':<10}{'Ratio':<10}{'Constraint':<15}")
        print("-" * 60)
        
        for i in range(self.num_items):
            ratio = self.values[i] / self.weights[i]
            
            if i in self.excluded_items:
                constraint = "EXCLUDED X"
            elif i in self.required_items:
                constraint = "REQUIRED +"
            else:
                constraint = "Optional"
            
            print(f"{self.item_names[i]:<15}{self.weights[i]:<10}{self.values[i]:<10.2f}"
                  f"{ratio:<10.2f}{constraint:<15}")
       
        print("-" * 60)
