"""
Integrated 0/1 Knapsack Solver
===============================
Main interface for knapsack solving with DP and Branch & Bound.
"""

from dp_solver import DPKnapsackSolver
from branch_bound_knapsack import BranchBoundKnapsack

def solve_knapsack_problem():
    """Solve a knapsack problem"""
    print("\n" + "-" * 70)
    print("         0/1 KNAPSACK PROBLEM")
    print("-" * 70)
    
    # Ask for method
    print("\nSelect Solution Method:")
    print("  1. Dynamic Programming (DP) - Fast, finds optimal")
    print("  2. Branch & Bound (B&B) - Can find top-N solutions")
    
    while True:
        try:
            method = int(input("\nEnter choice (1 or 2): "))
            if method in [1, 2]:
                break
            print("Please enter 1 or 2")
        except ValueError:
            print("Invalid input!")
    
    if method == 1:
        solver = DPKnapsackSolver()
        solver.configure_problem()
        input("\n→ Press ENTER to start solving...")
        solver.solve(show_steps=True)
    else:
        solver = BranchBoundKnapsack()
        solver.configure_problem()
        input("\n→ Press ENTER to start solving...")
        solver.solve()
    
    return solver

def main():
    """Main application loop"""
    print("\n" + "=" * 70)
    print("|" + " " * 15 + "KNAPSACK SOLVER SUITE" + " " * 31 + "|")
    print("|" + " " * 8 + "DP & Branch & Bound • Zero Dependencies" + " " * 19 + "|")
    print("=" * 70)
    
    while True:
        print("\n┌─ 0/1 KNAPSACK PROBLEM ─┐")
        print("│ 1. Solve Knapsack Problem")
        print("│ 2. Exit")
        print("└────────────────────────┘")
        
        while True:
            try:
                choice = int(input("\nEnter choice (1-2): "))
                if choice in [1, 2]:
                    break
                print("Please enter 1 or 2")
            except ValueError:
                print("Invalid input!")
        
        if choice == 1:
            solve_knapsack_problem()
        elif choice == 2:
            print("\n" + "=" * 70)
            print("Thank you for using Knapsack Solver!")
            print("=" * 70 + "\n")
            break
        
        print("\n" + "-" * 70)
        cont = input("\nSolve another problem? (y/n): ").lower()
        if cont != 'y':
            print("\n" + "=" * 70)
            print("Thank you for using Knapsack Solver!")
            print("=" * 70 + "\n")
            break

if __name__ == "__main__":
    main()
