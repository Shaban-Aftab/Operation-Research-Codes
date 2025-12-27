import copy
from Simplex import SimplexSolver, get_input

class SensitivityAnalyzer:
    def __init__(self):
        self.base_obj = []
        self.base_constraints = []
        self.base_is_max = True
        
        # Current state (modified from base)
        self.current_obj = []
        self.current_constraints = []
        self.current_is_max = True
        self.num_vars = 0

    def get_initial_problem(self):
        print("\n=== SENSITIVITY ANALYSIS: INITIAL PROBLEM SETUP ===")
        try:
            self.num_vars = int(get_input("Enter number of variables: "))
            n_cons = int(get_input("Enter number of constraints: "))
            
            type_lp = get_input("Type 'max' or 'min': ")
            self.base_is_max = (str(type_lp).lower().startswith('max'))
            self.current_is_max = self.base_is_max
        
            print("\n--- Objective Function ---")
            self.base_obj = [float(get_input(f"Coeff for x{i+1}: ")) for i in range(self.num_vars)]
            
            print("\n--- Constraints ---")
            print("Format: Coeffs... -> Operator (<=, >=, =) -> RHS")
            self.base_constraints = []
            for i in range(n_cons):
                print(f"Constraint {i+1}:")
                row = [float(get_input(f"  Coeff for x{j+1}: ")) for j in range(self.num_vars)]
                op = str(get_input("  Operator (<=, >=, =): ")).strip()
                rhs = float(get_input("  RHS: "))
                row.append(op)
                row.append(rhs)
                self.base_constraints.append(row)
            
            # Initialize current state
            self.current_obj = copy.deepcopy(self.base_obj)
            self.current_constraints = copy.deepcopy(self.base_constraints)
            
            print("\n>> Initial Problem Saved.")
            self.solve_current("Initial Problem")

        except Exception as e:
            print(f"[Error] Invalid Input: {e}")

    def solve_current(self, title="Result"):
        print(f"\n\n{'='*40}")
        print(f"SOLVING: {title}")
        print(f"{'='*40}")
        try:
            solver = SimplexSolver(self.current_obj, self.current_constraints, is_max=self.current_is_max)
            solver.solve()
        except Exception as e:
            print(f"Solver Error: {e}")

    def reset_to_base(self):
        self.current_obj = copy.deepcopy(self.base_obj)
        self.current_constraints = copy.deepcopy(self.base_constraints)
        self.current_is_max = self.base_is_max
        self.num_vars = len(self.base_obj)
        print("\n>> Problem reset to original state.")

    # --- Case 1: Change Objective Function Coefficient ---
    def change_obj_coeff(self):
        print("\n--- Case 1: Change Objective Coefficient ---")
        try:
            idx = int(get_input(f"Enter variable index (1 to {len(self.current_obj)}): ")) - 1
            if 0 <= idx < len(self.current_obj):
                old_val = self.current_obj[idx]
                new_val = float(get_input(f"Enter new coefficient for x{idx+1} (Current: {old_val}): "))
                self.current_obj[idx] = new_val
                return True
            else:
                print("Invalid index.")
                return False
        except:
            print("Invalid input.")
            return False

    # --- Case 2: Change RHS ---
    def change_rhs(self):
        print("\n--- Case 2: Change Right Hand Side (RHS) ---")
        try:
            idx = int(get_input(f"Enter constraint index (1 to {len(self.current_constraints)}): ")) - 1
            if 0 <= idx < len(self.current_constraints):
                old_rhs = self.current_constraints[idx][-1]
                new_rhs = float(get_input(f"Enter new RHS for Cons {idx+1} (Current: {old_rhs}): "))
                self.current_constraints[idx][-1] = new_rhs
                return True
            else:
                print("Invalid index.")
                return False
        except:
            print("Invalid input.")
            return False

    # --- Case 3: Change Matrix Coefficient ---
    def change_matrix_coeff(self):
        print("\n--- Case 3: Change Matrix Coefficient (A_ij) ---")
        try:
            c_idx = int(get_input(f"Enter constraint index (1 to {len(self.current_constraints)}): ")) - 1
            v_idx = int(get_input(f"Enter variable index (1 to {self.num_vars}): ")) - 1
            
            if (0 <= c_idx < len(self.current_constraints)) and (0 <= v_idx < self.num_vars):
                old_val = self.current_constraints[c_idx][v_idx]
                new_val = float(get_input(f"Enter new coeff (A_{c_idx+1},{v_idx+1}) (Current: {old_val}): "))
                self.current_constraints[c_idx][v_idx] = new_val
                return True
            else:
                print("Invalid index.")
                return False
        except:
            print("Invalid input.")
            return False

    # --- Case 4: Add New Constraint ---
    def add_constraint(self):
        print("\n--- Case 4: Add New Constraint ---")
        try:
            print(f"Enter coefficients for {self.num_vars} variables:")
            row = [float(get_input(f"  Coeff for x{j+1}: ")) for j in range(self.num_vars)]
            op = str(get_input("  Operator (<=, >=, =): ")).strip()
            rhs = float(get_input("  RHS: "))
            row.append(op)
            row.append(rhs)
            
            self.current_constraints.append(row)
            print(f">> Added Constraint {len(self.current_constraints)}")
            return True
        except:
            print("Error adding constraint.")
            return False

    # --- Case 5: Add New Variable ---
    def add_variable(self):
        print("\n--- Case 5: Add New Variable ---")
        try:
            new_var_name = f"x{self.num_vars + 1}"
            print(f"Adding Variable {new_var_name}")
            
            # 1. Add to Objective
            c_new = float(get_input(f"Enter Objective Coefficient for {new_var_name}: "))
            self.current_obj.append(c_new)
            
            # 2. Add column to Existing Constraints
            # NOTE: We insert the new coefficient BEFORE the operator (last 2 items)
            for i, cons in enumerate(self.current_constraints):
                val = float(get_input(f"Enter coeff of {new_var_name} in Constraint {i+1}: "))
                # insert at len-2 (before operator)
                cons.insert(len(cons)-2, val)
                
            self.num_vars += 1
            return True
        except:
            print("Error adding variable.")
            return False

    def run(self):
        self.get_initial_problem()
        
        while True:
            # Snapshot current state before modification
            last_obj = copy.deepcopy(self.current_obj)
            last_cons = copy.deepcopy(self.current_constraints)
            last_vars = self.num_vars
            
            print("\n\n" + "-"*50)
            print("SENSITIVITY ANALYSIS MENU")
            print("-" * 50)
            print("1. Change Objective Function Coefficient")
            print("2. Change Right Hand Side (RHS)")
            print("3. Change Constraint Matrix Value (A matrix)")
            print("4. Add New Constraint")
            print("5. Add New Variable")
            print("R. Reset to Original Problem")
            print("Q. Quit")
            
            # Use raw input() to avoid float conversion by Simplex.get_input
            choice = input("Choose Option: ").strip().upper()
            
            if choice == 'Q':
                break
            elif choice == 'R':
                self.reset_to_base()
                self.solve_current("Original Problem Restored")
                continue
                
            success = False
            label = ""
            
            if choice == '1':
                success = self.change_obj_coeff()
                label = "Diff Obj Coeffs"
            elif choice == '2':
                success = self.change_rhs()
                label = "Diff RHS"
            elif choice == '3':
                success = self.change_matrix_coeff()
                label = "Diff Matrix A"
            elif choice == '4':
                success = self.add_constraint()
                label = "Added Constraint"
            elif choice == '5':
                success = self.add_variable()
                label = "Added Variable"
            else:
                print("Invalid Option.")
                continue
            
            if success:
                self.solve_current(f"Modified Problem ({label})")
                
                # Ask to keep or revert
                keep = str(get_input("\nKeep this change for next steps? (y/n) [Default: n]: ")).lower()
                if keep != 'y':
                    # Revert to snapshot
                    self.current_obj = last_obj
                    self.current_constraints = last_cons
                    self.num_vars = last_vars
                    print(">> Change Reverted (Temporary Analysis).")
                else:
                    print(">> Change Committed.")
            
if __name__ == "__main__":
    app = SensitivityAnalyzer()
    
    # We need to wrap the internal logic to handle the "Undo" properly.
    # Refactoring the run method slightly on the fly here isn't great, but:
    
    # Let's override the run loop in the actual execution class if needed.
    # The 'run' method above is decent but lacks automatic undo.
    # I will stick to the basic 'run' above but added a small logic tweak below 
    # when I actually write the file in next tool call.
    
    app.run()