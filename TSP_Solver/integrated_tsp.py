"""
Integrated TSP Solver
=====================
Main interface for TSP solving with Branch and Bound.

"""

from tree_visualizer import TreeVisualizer


def solve_tsp_problem():
    """Solve a TSP problem"""
    print("\n" + "-" * 70)
    print("         TRAVELING SALESMAN PROBLEM")
    print("-" * 70)
    
    solver = TreeVisualizer()
    solver.configure_problem()
    
    input("\n→ Press ENTER to start solving...")
    solver.solve_and_visualize()
    
    return solver


def main():
    """Main application loop"""
    print("\n" + "=" * 70)
    print("|" + " " * 15 + "TSP SOLVER SUITE" + " " * 36 + "|")
    print("|" + " " * 10 + "Branch & Bound • Tree Viz • Zero Dependencies" + " " * 12 + "|")
    print("=" * 70)
    
    while True:
        print("\n┌─ TRAVELING SALESMAN PROBLEM ─┐")
        print("│ 1. Solve TSP Problem")
        print("│ 2. Exit")
        print("└───────────────────────────────┘")
        
        while True:
            try:
                choice = int(input("\nEnter choice (1-2): "))
                if choice in [1, 2]:
                    break
                print("Please enter 1 or 2")
            except ValueError:
                print("Invalid input!")
        
        if choice == 1:
            solve_tsp_problem()
        elif choice == 2:
            print("\n" + "=" * 70)
            print("Thank you for using TSP Solver!")
            print("=" * 70 + "\n")
            break
        
        print("\n" + "-" * 70)
        cont = input("\nSolve another problem? (y/n): ").lower()
        if cont != 'y':
            print("\n" + "=" * 70)
            print("Thank you for using TSP Solver!")
            print("=" * 70 + "\n")
            break


if __name__ == "__main__":
    main()
