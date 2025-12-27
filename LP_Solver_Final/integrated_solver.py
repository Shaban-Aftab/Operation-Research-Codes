"""
Integrated Linear Programming Solver
================================================================================
Unified application combining simplex optimization and sensitivity analysis.

Features:
► Simplex Method (handles all constraint types with Big-M)
► Big-M Method (dedicated solver with enhanced visualization)
► Post-Optimal Sensitivity Analysis
► Seamless workflow integration
► Zero external dependencies

This integrates:
- LinearOptimizationEngine (simplex_refactored.py)
- BigMSolver (big_m_method.py)
- PostOptimalAnalyzer (sensitivity_module.py)
"""

from simplex_refactored import LinearOptimizationEngine
from big_m_method import BigMSolver
from sensitivity_module import PostOptimalAnalyzer


def display_main_menu():
    """Display the main application menu"""
    print("\n" + "="*70)
    print("┃" + " "*12 + "INTEGRATED LP SOLVER & ANALYZER" + " "*25 + "┃")
    print("┃" + " "*8 + "Simplex + Big-M + Sensitivity Analysis" + " "*21 + "┃")
    print("┃" + " "*15 + "(Zero Dependencies!)" + " "*32 + "┃")
    print("="*70)
    
    print("\n┌─ Main Menu ─┐")
    print("│ 1. Simplex Method (Standard)")
    print("│ 2. Big-M Method (>= and = constraints)")
    print("│ 3. Simplex + Sensitivity Analysis")
    print("│ 4. Big-M + Sensitivity Analysis")
    print("│ 5. Sensitivity Analysis Only")
    print("│ 6. Exit")
    print("└──────────────┘")


def solve_lp_problem():
    """
    Solve a linear programming problem using the standard simplex method.
    Returns the solved engine instance.
    """
    print("\n" + "-"*70)
    print("           STANDARD SIMPLEX METHOD")
    print("-"*70)
    
    engine = LinearOptimizationEngine()
    engine.gather_problem_configuration()
    
    input("\n→ Press ENTER to begin optimization...")
    engine.commence_solution_process()
    
    return engine


def solve_bigm_problem():
    """
    Solve a linear programming problem using the Big-M method.
    Returns the solved engine instance.
    """
    print("\n" + "-"*70)
    print("           BIG-M METHOD SOLVER")
    print("-"*70)
    
    solver = BigMSolver()
    solver.gather_problem_configuration()
    
    input("\n→ Press ENTER to solve using Big-M method...")
    solver.commence_solution_process()
    
    return solver


def perform_sensitivity_analysis(engine):
    """
    Perform sensitivity analysis on a solved LP problem.
    
    Args:
        engine: A solved LinearOptimizationEngine or BigMSolver instance
    """
    print("\n" + "-"*70)
    print("        POST-OPTIMAL SENSITIVITY ANALYSIS")
    print("-"*70)
    
    try:
        analyzer = PostOptimalAnalyzer(engine)
        analyzer.post_optimal_menu()
    except Exception as e:
        print(f"\n✗ Error creating analyzer: {e}")
        print("  Ensure the problem was solved to optimality first.")


def main_application():
    """
    Main application loop with menu system.
    """
    # Storage for last solved engine
    last_solved_engine = None
    
    while True:
        display_main_menu()
        
        try:
            choice = int(input("\n→ Select option: "))
            
            if choice == 1:
                # Simplex only
                last_solved_engine = solve_lp_problem()
                
            elif choice == 2:
                # Big-M only
                last_solved_engine = solve_bigm_problem()
                
            elif choice == 3:
                # Simplex + Sensitivity
                last_solved_engine = solve_lp_problem()
                if last_solved_engine.operational_matrix is not None:
                    response = input("\nProceed to sensitivity analysis? (y/n): ")
                    if response.lower() == 'y':
                        perform_sensitivity_analysis(last_solved_engine)
                
            elif choice == 4:
                # Big-M + Sensitivity
                last_solved_engine = solve_bigm_problem()
                if last_solved_engine.operational_matrix is not None:
                    response = input("\nProceed to sensitivity analysis? (y/n): ")
                    if response.lower() == 'y':
                        perform_sensitivity_analysis(last_solved_engine)
                
            elif choice == 5:
                # Sensitivity on existing solution
                if last_solved_engine is None:
                    print("\n⚠ No solution available.")
                    print("  Please solve a problem first (option 1, 2, 3, or 4).")
                else:
                    perform_sensitivity_analysis(last_solved_engine)
                
            elif choice == 6:
                # Exit
                print("\n" + "="*70)
                print("Thank you for using the Integrated LP Solver!")
                print("="*70 + "\n")
                break
                
            else:
                print("\n⚠ Invalid choice. Please select 1-6.")
                
        except ValueError:
            print("\n⚠ Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"\n✗ An error occurred: {e}")
            print("  Please try again or report this issue.")


if __name__ == "__main__":
    main_application()
