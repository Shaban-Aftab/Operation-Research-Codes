"""
ASSIGNMENT PROBLEM SOLVER - HUNGARIAN METHOD
============================================


Features:
- Hungarian Method algorithm
- Handles unbalanced problems (adds dummy rows/columns)
- Minimization AND Maximization
============================================
"""


class HungarianMethod:
    """Complete Hungarian Method solver for assignment problems"""
    
    def __init__(self):
        self.num_workers = 0
        self.num_jobs = 0
        self.original_matrix = []
        self.cost_matrix = []
        self.worker_names = []
        self.job_names = []
        self.is_minimization = True
        self.is_balanced = True
        self.dummy_workers = 0
        self.dummy_jobs = 0
        self.assignments = {}  # worker -> job
        
        self.INF = float('inf')
    
    def get_user_input(self):
        """Get problem input from user"""
        print("\n" + "=" * 70)
        print("       ASSIGNMENT PROBLEM SOLVER")
        print("           (Hungarian Method)")
        print("=" * 70)
        
        # Problem type
        print("\nProblem Type:")
        print("  1. Minimization (minimize cost)")
        print("  2. Maximization (maximize profit)")
        
        while True:
            try:
                choice = int(input("\nEnter choice (1 or 2): "))
                if choice in [1, 2]:
                    self.is_minimization = (choice == 1)
                    break
                print("Please enter 1 or 2")
            except ValueError:
                print("Invalid input!")
        
        problem_type = "MINIMIZATION" if self.is_minimization else "MAXIMIZATION"
        print(f"\n>>> Selected: {problem_type}")
        
        # Number of workers
        while True:
            try:
                self.num_workers = int(input("\nNumber of workers/agents: "))
                if self.num_workers > 0:
                    break
                print("Must be positive")
            except ValueError:
                print("Invalid input!")
        
        # Number of jobs
        while True:
            try:
                self.num_jobs = int(input("Number of jobs/tasks: "))
                if self.num_jobs > 0:
                    break
                print("Must be positive")
            except ValueError:
                print("Invalid input!")
        
        # Check if balanced
        self.is_balanced = (self.num_workers == self.num_jobs)
        
        if not self.is_balanced:
            print(f"\n⚠ UNBALANCED PROBLEM: {self.num_workers} workers × {self.num_jobs} jobs")
            print("  → Will add dummy rows/columns to balance")
        
        # Worker names
        print("\n--- WORKER NAMES ---")
        use_default = input("Use default names (W1, W2, ...)? (y/n): ").lower() == 'y'
        
        if use_default:
            self.worker_names = [f"W{i+1}" for i in range(self.num_workers)]
        else:
            for i in range(self.num_workers):
                name = input(f"  Worker {i+1} name: ").strip()
                self.worker_names.append(name if name else f"W{i+1}")
        
        # Job names
        print("\n--- JOB NAMES ---")
        use_default = input("Use default names (J1, J2, ...)? (y/n): ").lower() == 'y'
        
        if use_default:
            self.job_names = [f"J{i+1}" for i in range(self.num_jobs)]
        else:
            for i in range(self.num_jobs):
                name = input(f"  Job {i+1} name: ").strip()
                self.job_names.append(name if name else f"J{i+1}")
        
        # Cost matrix
        print("\n--- COST MATRIX ---")
        cost_type = "cost" if self.is_minimization else "profit"
        print(f"Enter the {cost_type} for each worker-job pair:")
        
        self.original_matrix = []
        for i in range(self.num_workers):
            print(f"\nWorker {self.worker_names[i]}:")
            row = []
            for j in range(self.num_jobs):
                while True:
                    try:
                        value = float(input(f"  {cost_type} for {self.job_names[j]}: "))
                        row.append(value)
                        break
                    except ValueError:
                        print("  Invalid input!")
            self.original_matrix.append(row)
        
        self.display_original_problem()
    
    def display_original_problem(self):
        """Display original problem"""
        print("\n" + "=" * 70)
        print("              ORIGINAL PROBLEM")
        print("=" * 70)
        
        problem_type = "Minimization" if self.is_minimization else "Maximization"
        print(f"\nType: {problem_type}")
        print(f"Workers: {self.num_workers}")
        print(f"Jobs: {self.num_jobs}")
        print(f"Balanced: {'Yes' if self.is_balanced else 'No'}")
        
        self._display_matrix(self.original_matrix, self.worker_names, self.job_names, "ORIGINAL COST MATRIX")
    
    def _display_matrix(self, matrix, row_names, col_names, title):
        """Display a matrix with labels"""
        print("\n" + "-" * 60)
        print(title)
        print("-" * 60)
        
        col_width = 10
        
        # Header
        print(f"{'':>8} |", end="")
        for name in col_names:
            print(f"{name:^{col_width}}", end="")
        print()
        print("-" * (8 + col_width * len(col_names) + 1))
        
        # Rows
        for i, row_name in enumerate(row_names):
            print(f"{row_name:>7} |", end="")
            for j in range(len(col_names)):
                if i < len(matrix) and j < len(matrix[i]):
                    value = matrix[i][j]
                    if value == 0:
                        print(f"{'[0]':^{col_width}}", end="")
                    else:
                        print(f"{value:^{col_width}.1f}", end="")
                else:
                    print(f"{'0':^{col_width}}", end="")
            print()
        
        print("-" * (8 + col_width * len(col_names) + 1))
    
    def balance_matrix(self):
        """Balance the matrix by adding dummy rows/columns"""
        print("\n" + "=" * 70)
        print("      STEP 1: BALANCING THE MATRIX")
        print("=" * 70)
        
        if self.is_balanced:
            print("\n✓ Matrix is already balanced!")
            self.cost_matrix = [row[:] for row in self.original_matrix]
            return
        
        # Determine what to add
        if self.num_workers < self.num_jobs:
            self.dummy_workers = self.num_jobs - self.num_workers
            print(f"\n→ Adding {self.dummy_workers} dummy worker(s)")
            
            # Copy original matrix
            self.cost_matrix = [row[:] for row in self.original_matrix]
            
            # Add dummy rows with zeros
            for i in range(self.dummy_workers):
                self.cost_matrix.append([0] * self.num_jobs)
                self.worker_names.append(f"Dummy{i+1}")
            
        else:  # num_workers > num_jobs
            self.dummy_jobs = self.num_workers - self.num_jobs
            print(f"\n→ Adding {self.dummy_jobs} dummy job(s)")
            
            # Add dummy columns with zeros
            self.cost_matrix = []
            for row in self.original_matrix:
                new_row = row[:] + [0] * self.dummy_jobs
                self.cost_matrix.append(new_row)
            
            for i in range(self.dummy_jobs):
                self.job_names.append(f"Dummy{i+1}")
        
        print("→ Dummy assignments have zero cost")
        
        self._display_matrix(self.cost_matrix, self.worker_names, self.job_names, "BALANCED COST MATRIX")
    
    def convert_to_minimization(self):
        """Convert maximization to minimization"""
        if self.is_minimization:
            return
        
        print("\n" + "=" * 70)
        print("      CONVERTING MAXIMIZATION TO MINIMIZATION")
        print("=" * 70)
        
        # Find maximum value
        max_val = max(max(row) for row in self.cost_matrix)
        print(f"\n→ Maximum value: {max_val}")
        print("→ New matrix: Max - Original")
        
        # Subtract all values from max
        for i in range(len(self.cost_matrix)):
            for j in range(len(self.cost_matrix[i])):
                self.cost_matrix[i][j] = max_val - self.cost_matrix[i][j]
        
        self._display_matrix(self.cost_matrix, self.worker_names, self.job_names, "CONVERTED MATRIX (MINIMIZATION)")
    
    def row_reduction(self):
        """Step 2: Row reduction"""
        print("\n" + "=" * 70)
        print("      STEP 2: ROW REDUCTION")
        print("=" * 70)
        
        print("\n→ Subtract minimum from each row")
        
        for i in range(len(self.cost_matrix)):
            min_val = min(self.cost_matrix[i])
            print(f"  Row {self.worker_names[i]}: min = {min_val}")
            
            for j in range(len(self.cost_matrix[i])):
                self.cost_matrix[i][j] -= min_val
        
        self._display_matrix(self.cost_matrix, self.worker_names, self.job_names, "AFTER ROW REDUCTION")
    
    def column_reduction(self):
        """Step 3: Column reduction"""
        print("\n" + "=" * 70)
        print("      STEP 3: COLUMN REDUCTION")
        print("=" * 70)
        
        print("\n→ Subtract minimum from each column")
        
        n = len(self.cost_matrix)
        for j in range(len(self.cost_matrix[0])):
            min_val = min(self.cost_matrix[i][j] for i in range(n))
            print(f"  Column {self.job_names[j]}: min = {min_val}")
            
            for i in range(n):
                self.cost_matrix[i][j] -= min_val
        
        self._display_matrix(self.cost_matrix, self.worker_names, self.job_names, "AFTER COLUMN REDUCTION")
    
    def find_assignments(self):
        """Find optimal assignments using greedy approach on zeros"""
        n = len(self.cost_matrix)
        self.assignments = {}
        assigned_jobs = set()
        
        # Greedy assignment: assign zeros
        for i in range(n):
            for j in range(len(self.cost_matrix[0])):
                if self.cost_matrix[i][j] == 0 and j not in assigned_jobs:
                    self.assignments[i] = j
                    assigned_jobs.add(j)
                    break
    
    def solve(self):
        """Main solving method"""
        print("\n" + "=" * 70)
        print("      SOLVING ASSIGNMENT PROBLEM")
        print("=" * 70)
        
        # Balance
        self.balance_matrix()
        
        # Convert if maximization
        self.convert_to_minimization()
        
        # Row reduction
        self.row_reduction()
        
        # Column reduction
        self.column_reduction()
        
        # Find assignments
        print("\n" + "=" * 70)
        print("      STEP 4: FINDING ASSIGNMENTS")
        print("=" * 70)
        
        print("\n→ Finding zeros and making assignments...")
        self.find_assignments()
        
        print("\n✓ Assignments complete!")
    
    def display_solution(self):
        """Display final solution"""
        print("\n" + "=" * 70)
        print("              OPTIMAL ASSIGNMENT")
        print("=" * 70)
        
        total_cost = 0
        
        print("\n" + "-" * 60)
        print(f"{'Worker':<15}{'→':^5}{'Job':<15}{'Cost':>10}")
        print("-" * 60)
        
        for worker_idx in sorted(self.assignments.keys()):
            job_idx = self.assignments[worker_idx]
            worker_name = self.worker_names[worker_idx]
            job_name = self.job_names[job_idx]
            
            # Get original cost
            if worker_idx < self.num_workers and job_idx < self.num_jobs:
                cost = self.original_matrix[worker_idx][job_idx]
                total_cost += cost
            else:
                cost = 0  # Dummy assignment
            
            is_dummy = "Dummy" in worker_name or "Dummy" in job_name
            marker = " (Dummy)" if is_dummy else ""
            
            print(f"{worker_name:<15}{'→':^5}{job_name:<15}{cost:>10.1f}{marker}")
        
        print("-" * 60)
        
        if self.is_minimization:
            print(f"\n>>> MINIMUM TOTAL COST = {total_cost:.1f}")
        else:
            print(f"\n>>> MAXIMUM TOTAL PROFIT = {total_cost:.1f}")
        
        print("=" * 70)
        
        # Show unassigned
        if self.dummy_workers > 0:
            print(f"\n⚠ Note: {self.dummy_workers} dummy worker(s) → some jobs left unassigned")
        if self.dummy_jobs > 0:
            print(f"\n⚠ Note: {self.dummy_jobs} dummy job(s) → some workers left unassigned")


def main():
    """Main application"""
    print("\n" + "=" * 70)
    print("|         ASSIGNMENT PROBLEM SOLVER                       |")
    print("|            Hungarian Method                             |")
    print("|     (Handles Balanced & Unbalanced Problems)            |")
    print("=" * 70)
    
    while True:
        solver = HungarianMethod()
        solver.get_user_input()
        
        input("\nPress ENTER to solve...")
        solver.solve()
        solver.display_solution()
        
        print("\n" + "-" * 70)
        choice = input("\nSolve another problem? (y/n): ").lower()
        if choice != 'y':
            print("\n" + "=" * 70)
            print("Thank you for using Assignment Problem Solver!")
            print("=" * 70 + "\n")
            break


if __name__ == "__main__":
    main()
