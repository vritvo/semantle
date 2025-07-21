#!/usr/bin/env python3
"""
Main entry point for the Semantle solver application.
"""

from semantle.semantle import Semantle
from semantle.solver import Solver


def main():
    """
    Run the Semantle solver to find today's word.
    """
    print("Initializing Semantle...")
    semantle = Semantle()

    print("Creating solver...")
    solver = Solver(semantle)

    print("Analyzing potential answers...")
    solver.create_answer_table()

    print("Identifying solution...")
    solution = solver.identify_solution()

    if solution:
        print(f"{solution} is the solution to today's Semantle")
    else:
        print("No solution found with the current guesses")


if __name__ == "__main__":
    main()
