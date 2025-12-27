"""
Integrated Transportation Problem Solver


Methods:
- Northwest Corner (simplest)
- Least Cost (greedy)
- VAM (best initial solution)
- MODI Optimization (finds optimal)

"""

from northwest_corner import NorthwestCornerSolver
from least_cost import LeastCostSolver
from vam_method import VAMSolver
from modi_optimizer import MODIOptimizer
from maximization import solve_maximization_problem


def display_menu():
    """Display main menu"""
    print("\n" + "="*70)
    print("┃" + " "*10 + "TRANSPORTATION PROBLEM SOLVER" + " "*29 + "┃")
    print("┃" + " "*8 + "Modular | Step-by-Step | Zero Dependencies" + " "*17 + "┃")
    print("="*70)
    
    print("\n┌─ SELECT METHOD ─┐")
    print("│ 1. Northwest Corner Method")
    print("│ 2. Least Cost Method")
    print("│ 3. Vogel's Approximation Method (VAM)")
    print("│ 4. Complete Optimization (VAM + MODI)")
    print("│ 5. Maximization Problem (Profit)")
    print("│ 6. Custom (choose initial + optimizer)")
    print("│ 7. Exit")
    print("└──────────────────┘")


def solve_northwest_corner():
    """Solve using Northwest Corner only"""
    print("\n" + "-"*70)
    print("         NORTHWEST CORNER METHOD")
    print("-"*70)
    
    solver = NorthwestCornerSolver()
    solver.configure_problem()
    solver.balance_problem()
    
    input("\n→ Press ENTER to find initial solution...")
    solver.find_initial_solution()
    solver.verify_solution()
    
    return solver


def solve_least_cost():
    """Solve using Least Cost only"""
    print("\n" + "-"*70)
    print("         LEAST COST METHOD")
    print("-"*70)
    
    solver = LeastCostSolver()
    solver.configure_problem()
    solver.balance_problem()
    
    input("\n→ Press ENTER to find initial solution...")
    solver.find_initial_solution()
    solver.verify_solution()
    
    return solver


def solve_vam():
    """Solve using VAM only"""
    print("\n" + "-"*70)
    print("         VOGEL'S APPROXIMATION METHOD")
    print("-"*70)
    
    solver = VAMSolver()
    solver.configure_problem()
    solver.balance_problem()
    
    input("\n→ Press ENTER to find initial solution...")
    solver.find_initial_solution()
    solver.verify_solution()
    
    return solver


def solve_complete():
    """Complete solution: VAM + MODI optimization"""
    print("\n" + "-"*70)
    print("         COMPLETE OPTIMIZATION (VAM + MODI)")
    print("-"*70)
    
    # Phase 1: VAM for initial solution
    print("\n>>> PHASE 1: Initial Solution (VAM)")
    vam_solver = VAMSolver()
    vam_solver.configure_problem()
    vam_solver.balance_problem()
    
    input("\n→ Press ENTER for VAM initial solution...")
    vam_solver.find_initial_solution()
    
    # Phase 2: MODI optimization
    print("\n>>> PHASE 2: Optimization (MODI)")
    input("\n→ Press ENTER to optimize with MODI...")
    
    # Transfer to MODI optimizer
    optimizer = MODIOptimizer()
    optimizer.__dict__.update(vam_solver.__dict__)
    optimizer.optimize()
    optimizer.verify_solution()
    
    display_final_solution(optimizer)
    
    return optimizer


def solve_custom():
    """Custom workflow - user chooses initial method + optimization"""
    print("\n" + "-"*70)  
    print("         CUSTOM WORKFLOW")
    print("-"*70)
    
    # Choose initial method
    print("\nSelect Initial BFS Method:")
    print("  1. Northwest Corner")
    print("  2. Least Cost")
    print("  3. VAM")
    
    choice = get_choice(1, 3)
    
    # Get initial solution
    if choice == 1:
        solver = NorthwestCornerSolver()
    elif choice == 2:
        solver = LeastCostSolver()
    else:
        solver = VAMSolver()
    
    solver.configure_problem()
    solver.balance_problem()
    
    input("\n→ Press ENTER for initial solution...")
    solver.find_initial_solution()
    
    # Ask about optimization
    print("\n" + "-"*70)
    optimize = input("Optimize with MODI method? (y/n): ").lower() == 'y'
    
    if optimize:
        optimizer = MODIOptimizer()
        optimizer.__dict__.update(solver.__dict__)
        optimizer.optimize()
        optimizer.verify_solution()
        display_final_solution(optimizer)
        return optimizer
    else:
        solver.verify_solution()
        return solver


def display_final_solution(solver):
    """Display final solution summary"""
    print("\n" + "="*70)
    print("                 FINAL TRANSPORTATION PLAN")
    print("="*70)
    
    print("\n→ Optimal Shipments:")
    print("-"*50)
    
    real_cost = 0
    for i in range(solver.num_sources):
        for j in range(solver.num_destinations):
            if solver.allocation[i][j] is not None and solver.allocation[i][j] > solver.EPSILON:
                is_dummy = (solver.source_names[i] == "Dummy" or solver.dest_names[j] == "Dummy")
                
                if is_dummy:
                    print(f"  {solver.source_names[i]:>6} → {solver.dest_names[j]:<6}: "
                          f"{solver.allocation[i][j]:>6.0f} units (DUMMY - no cost)")
                else:
                    unit_cost = solver.cost_matrix[i][j]
                    total = solver.allocation[i][j] * unit_cost
                    real_cost += total
                    print(f"  {solver.source_names[i]:>6} → {solver.dest_names[j]:<6}: "
                          f"{solver.allocation[i][j]:>6.0f} units × ${unit_cost:.0f} = ${total:.0f}")
    
    print("-"*50)
    print(f"\n>>> MINIMUM TOTAL COST: ${real_cost:.2f}")
    
    if solver.dummy_added:
        print(f"\n⚠ Note: Dummy {solver.dummy_added} was added for balancing")


def get_choice(min_val, max_val):
    """Get valid choice from user"""
    while True:
        try:
            choice = int(input(f"\nEnter choice ({min_val}-{max_val}): "))
            if min_val <= choice <= max_val:
                return choice
            print(f"Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print("Invalid input!")


def main():
    """Main application loop"""
    print("\n" + "="*70)
    print("|" + " "*15 + "TRANSPORTATION SOLVER SUITE" + " "*26 + "|")
    print("|" + " "*10 + "Modular • Professional • Zero Dependencies" + " "*15 + "|")
    print("="*70)
    
    while True:
        display_menu()
        
        choice = get_choice(1, 7)
        
        if choice == 1:
            solve_northwest_corner()
        elif choice == 2:
            solve_least_cost()
        elif choice == 3:
            solve_vam()
        elif choice == 4:
            solve_complete()
        elif choice == 5:
            solve_maximization_problem()
        elif choice == 6:
            solve_custom()
        elif choice == 7:
            print("\n" + "="*70)
            print("Thank you for using Transportation Solver!")
            print("="*70 + "\n")
            break
        
        print("\n" + "-"*70)
        cont = input("\nSolve another problem? (y/n): ").lower()
        if cont != 'y':
            print("\n" + "="*70)
            print("Thank you for using Transportation Solver!")
            print("="*70 + "\n")
            break


if __name__ == "__main__":
    main()
