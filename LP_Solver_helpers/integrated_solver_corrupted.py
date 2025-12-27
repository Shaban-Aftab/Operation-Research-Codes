"""
Integrated Linear Programming Solver
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Unified application combining simplex optimization and sensitivity analysis.

Features:
► Simplex Method (handles all constraint types with Big-M)
► Post-Optimal Sensitivity Analysis
► Seamless workflow integration
► Zero external dependencies

This integrates:
- LinearOptimizationEngine (simplex_refactored.py)
- PostOptimalAnalyzer (sensitivity_module.py)
"""

from simplex_refactored import LinearOptimizationEngine
from sensitivity_module import PostOptimalAnalyzer


def display_main_menu():
    """Display the main application menu"""
    print(\"\\n\" + \"═\"*70)
    print(\"┃\" + \" \"*15 + \"INTEGRATED LP SOLVER & ANALYZER\" + \" \"*22 + \"┃\")
    print(\"┃\" + \" \"*12 + \"Simplex + Sensitivity Analysis\" + \" \"*25 + \"┃\")
    print(\"┃\" + \" \"*12 + \"(Zero Dependencies - Pure Python!)\" + \" \"*21 + \"┃\")
    print(\"═\"*70)
    
    print(\"\\n┌─ Main Menu ─┐\")
    print(\"│ 1. Solve LP Problem\")\r\n    print(\"│ 2. Solve + Sensitivity Analysis\")\r\n    print(\"│ 3. Sensitivity Analysis (existing solution)\")\r\n    print(\"│ 4. Exit\")\r\n    print(\"└──────────────┘\")\r\n\r\n\r\ndef solve_lp_problem():\r\n    \"\"\"\r\n    Solve a linear programming problem using the simplex method.\r\n    Returns the solved engine instance.\r\n    \"\"\"\r\n    print(\"\\n\" + \"─\"*70)\r\n    print(\"           STEP 1: PROBLEM FORMULATION & SOLUTION\")\r\n    print(\"─\"*70)\r\n    \r\n    engine = LinearOptimizationEngine()\r\n    engine.gather_problem_configuration()\r\n    \r\n    input(\"\\n→ Press ENTER to begin optimization...\")\r\n    engine.commence_solution_process()\r\n    \r\n    return engine\r\n\r\n\r\ndef perform_sensitivity_analysis(engine):\r\n    \"\"\"\r\n    Perform sensitivity analysis on a solved LP problem.\r\n    \r\n    Args:\r\n        engine: A solved LinearOptimizationEngine instance\r\n    \"\"\"\r\n    print(\"\\n\" + \"─\"*70)\r\n    print(\"        STEP 2: POST-OPTIMAL SENSITIVITY ANALYSIS\")\r\n    print(\"─\"*70)\r\n    \r\n    try:\r\n        analyzer = PostOptimalAnalyzer(engine)\r\n        analyzer.post_optimal_menu()\r\n    except Exception as e:\r\n        print(f\"\\n✗ Error creating analyzer: {e}\")\r\n        print(\"  Ensure the problem was solved to optimality first.\")\r\n\r\n\r\ndef integrated_workflow():\r\n    \"\"\"\r\n    Execute the complete integrated workflow:\r\n    1. Solve LP problem\r\n    2. Perform sensitivity analysis\r\n    \"\"\"\r\n    engine = solve_lp_problem()\r\n    \r\n    # Check if solution was found\r\n    if engine.operational_matrix is None:\r\n        print(\"\\n⚠ Problem was not solved successfully.\")\r\n        print(\"  Sensitivity analysis requires an optimal solution.\")\r\n        return\r\n    \r\n    # Ask if user wants sensitivity analysis\r\n    print(\"\\n\" + \"─\"*70)\r\n    response = input(\"\\nProceed to sensitivity analysis? (y/n): \")\r\n    \r\n    if response.lower() == 'y':\r\n        perform_sensitivity_analysis(engine)\r\n\r\n\r\ndef main_application():\r\n    \"\"\"\r\n    Main application loop with menu system.\r\n    \"\"\"\r\n    # Storage for last solved engine (for option 3)\r\n    last_solved_engine = None\r\n    \r\n    while True:\r\n        display_main_menu()\r\n        \r\n        try:\r\n            choice = int(input(\"\\n→ Select option: \"))\r\n            \r\n            if choice == 1:\r\n                # Solve only\r\n                last_solved_engine = solve_lp_problem()\r\n                \r\n            elif choice == 2:\r\n                # Solve + Sensitivity\r\n                last_solved_engine = solve_lp_problem()\r\n                if last_solved_engine.operational_matrix is not None:\r\n                    perform_sensitivity_analysis(last_solved_engine)\r\n                \r\n            elif choice == 3:\r\n                # Sensitivity on existing solution\r\n                if last_solved_engine is None:\r\n                    print(\"\\n⚠ No solution available.\")\r\n                    print(\"  Please solve a problem first (option 1 or 2).\")\r\n                else:\r\n                    perform_sensitivity_analysis(last_solved_engine)\r\n                \r\n            elif choice == 4:\r\n                # Exit\r\n                print(\"\\n\" + \"═\"*70)\r\n                print(\"Thank you for using the Integrated LP Solver!\")\r\n                print(\"═\"*70 + \"\\n\")\r\n                break\r\n                \r\n            else:\r\n                print(\"\\n⚠ Invalid choice. Please select 1-4.\")\r\n                \r\n        except ValueError:\r\n            print(\"\\n⚠ Invalid input. Please enter a number.\")\r\n        except KeyboardInterrupt:\r\n            print(\"\\n\\nOperation cancelled by user.\")\r\n            break\r\n        except Exception as e:\r\n            print(f\"\\n✗ An error occurred: {e}\")\r\n            print(\"  Please try again or report this issue.\")\r\n\r\n\r\nif __name__ == \"__main__\":\r\n    main_application()\r\n
