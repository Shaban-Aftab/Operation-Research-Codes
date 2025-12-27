def get_input(prompt, default=0.0):
    val = input(prompt).strip()
    if not val:
        return default
    try:
        return float(val)
    except ValueError:
        return val

class SimplexSolver:
    def __init__(self, obj_coeffs, constraints, is_max=True):
        self.is_max = is_max
        self.num_vars = len(obj_coeffs)
        self.num_constraints = len(constraints)
        self.M = 100000.0
        
        self.basic_vars = [None] * self.num_constraints
        
        self.matrix = [] 
        
        self.artif_indices = [] 
        
        total_slacks = 0
        total_artifs = 0
        
        slack_names = []
        artif_names = []
        
        constraint_definitions = [] 
        
        for i, c in enumerate(constraints):
            op = c[-2]
            
            definition = {'type': op, 'slack_idx': -1, 'artif_idx': -1}
            
            if op == '<=':
                definition['slack_idx'] = total_slacks
                total_slacks += 1
                s_name = f"s{total_slacks}"
                slack_names.append(s_name)
                self.basic_vars[i] = s_name
                
            elif op == '>=':
                definition['slack_idx'] = total_slacks
                total_slacks += 1
                e_name = f"e{total_slacks}"
                slack_names.append(e_name)
                
                definition['artif_idx'] = total_artifs
                total_artifs += 1
                a_name = f"a{total_artifs}"
                artif_names.append(a_name)
                self.basic_vars[i] = a_name
                
            elif op == '=':
                definition['artif_idx'] = total_artifs
                total_artifs += 1
                a_name = f"a{total_artifs}"
                artif_names.append(a_name)
                self.basic_vars[i] = a_name
            
            constraint_definitions.append(definition)

        self.col_headers = [f"x{i+1}" for i in range(self.num_vars)] + slack_names + artif_names
        self.num_total_vars = self.num_vars + total_slacks + total_artifs
        
        for i, c in enumerate(constraints):
            row = []
            
            row.extend(c[:-2]) 
            
            temp_slacks = [0.0] * total_slacks
            def_ = constraint_definitions[i]
            
            if def_['type'] == '<=':
                temp_slacks[def_['slack_idx']] = 1.0
            elif def_['type'] == '>=':
                temp_slacks[def_['slack_idx']] = -1.0
            
            row.extend(temp_slacks)
            
            temp_artifs = [0.0] * total_artifs
            if def_['artif_idx'] != -1:
                temp_artifs[def_['artif_idx']] = 1.0
                current_col_idx = self.num_vars + total_slacks + def_['artif_idx']
                self.artif_indices.append(current_col_idx)

            row.extend(temp_artifs)
            
            row.append(c[-1])
            
            self.matrix.append(row)
            
        z_row = [0.0] * (self.num_total_vars + 1)
        
        mult = 1.0 if self.is_max else -1.0 
        
        for i in range(self.num_vars):
            z_row[i] = -1.0 * obj_coeffs[i] * mult
            
        if total_artifs > 0:
            for artif_col_idx in self.artif_indices:
                z_row[artif_col_idx] = self.M
                
            for i in range(self.num_constraints):
                basic_var = self.basic_vars[i]
                if basic_var.startswith('a'):
                    col_idx = self.col_headers.index(basic_var)
                    factor = z_row[col_idx] 
                    for j in range(len(z_row)):
                        z_row[j] -= factor * self.matrix[i][j]
                        
        self.matrix.append(z_row)
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def print_tableau(self):
        header = ["Basic"] + self.col_headers + ["Solution"]
        
        widths = [10] * len(header)
        
        print("-" * (sum(widths) + len(widths)))
        print("".join([f"{h:>{w}}" for h, w in zip(header, widths)]))
        print("-" * (sum(widths) + len(widths)))
        
        for i in range(self.rows - 1):
            row_label = self.basic_vars[i]
            row_vals = [f"{x:.2f}" for x in self.matrix[i]]
            print(f"{row_label:>10}" + "".join([f"{v:>10}" for v in row_vals]))
            
        z_vals = [f"{x:.2f}" for x in self.matrix[-1]]
        print(f"{'Z':>10}" + "".join([f"{v:>10}" for v in z_vals]))
        print("-" * (sum(widths) + len(widths)))

    def solve(self):
        iteration = 0
        max_iterations = 1000

        while iteration < max_iterations:
            print(f"\n--- Iteration {iteration} ---")
            self.print_tableau()
            
            z_row = self.matrix[-1][:-1]
            min_val = min(z_row)
            
            if min_val >= -1e-9:
                
                for i in range(self.rows - 1):
                    basic_var = self.basic_vars[i]
                    val = self.matrix[i][-1]
                    if basic_var.startswith('a') and val > 1e-6:
                        print(f"\n[Infeasible Solution] Artificial variable '{basic_var}' > 0.")
                        return

                alt_optima = []
                for i, c_val in enumerate(z_row):
                    var_name = self.col_headers[i]
                    if var_name not in self.basic_vars and abs(c_val) < 1e-6:
                        alt_optima.append(var_name)
                
                if alt_optima:
                    print(f"\n[Alternative Optima Detected] Variable(s) {', '.join(alt_optima)} could enter basis with no Z change.")
                
                print("\n[Optimal Solution Found]")
                self.print_tableau()
                return

            pivot_col = z_row.index(min_val)
            entering_var = self.col_headers[pivot_col]
            
            ratios = []
            possible_rows = []
            for i in range(self.rows - 1):
                lhs = self.matrix[i][pivot_col]
                rhs = self.matrix[i][-1]
                if lhs > 1e-9:
                    ratio = rhs / lhs
                    ratios.append(ratio)
                    possible_rows.append(i)
                else:
                    ratios.append(float('inf'))
                    possible_rows.append(i)
            
            min_ratio = min(ratios)
            if min_ratio == float('inf'):
                print("\n[Unbounded Solution]")
                return
            
            candidates = [i for i, r in enumerate(ratios) if abs(r - min_ratio) < 1e-9]
            
            if len(candidates) > 1:
                print(f"   [Degeneracy] Tie in ratio test between rows {candidates}. Choosing {candidates[0]}.")
            
            pivot_row = candidates[0]
            leaving_var = self.basic_vars[pivot_row]
            pivot_element = self.matrix[pivot_row][pivot_col]
            
            print(f"\n>> Pivot Element: {pivot_element:.4f}")
            print(f"   Row: {pivot_row} (Leaving: {leaving_var})")
            print(f"   Col: {pivot_col} (Entering: {entering_var})")
            
            self.matrix[pivot_row] = [x / pivot_element for x in self.matrix[pivot_row]]
            
            self.basic_vars[pivot_row] = entering_var
            
            for i in range(self.rows):
                if i != pivot_row:
                    factor = self.matrix[i][pivot_col]
                    self.matrix[i] = [self.matrix[i][j] - factor * self.matrix[pivot_row][j] for j in range(self.cols)]
            
            iteration += 1
        
        print("\n[Terminated] Max iterations reached. Probable cycling.")

if __name__ == "__main__":
    print("--- General Big-M Simplex Solver ---")
    try:
        n_vars = int(get_input("Enter number of variables: "))
        n_cons = int(get_input("Enter number of constraints: "))
        
        type_lp = get_input("Type 'max' or 'min': ")
        is_max = (str(type_lp).lower().startswith('max'))
    
        print("\n--- Objective Function ---")
        obj = [get_input(f"Coeff for x{i+1}: ") for i in range(n_vars)]
        
        print("\n--- Constraints ---")
        print("Format: Coeffs... -> Operator (<=, >=, =) -> RHS")
        cons = []
        for i in range(n_cons):
            print(f"Constraint {i+1}:")
            row = [get_input(f"  Coeff for x{j+1}: ") for j in range(n_vars)]
            op = str(get_input("  Operator (<=, >=, =): ")).strip()
            rhs = get_input("  RHS: ")
            row.append(op)
            row.append(rhs)
            cons.append(row)
    
        solver = SimplexSolver(obj, cons, is_max=is_max)
        solver.solve()
        
    except Exception as e:
        print(f"\n[Error] {e}")
        import traceback
        traceback.print_exc()
