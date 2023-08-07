"""
Russell & P. Norvig "Artificial Intelligence; A Modern Approach" Prentice-Hall.
"""

from problem import Problem
from search_algorithm import SearchAlgorithm

if __name__ == "__main__":

    problem = Problem()
    problem.get_input()

    init, goal, oper, algo = problem.get_initial_goal_operators_algorithm()

    search = SearchAlgorithm()
    node, tree = search.graph_search(init, goal, oper, algo)

    if node is None:
        print("\n\nThe goal state was not found.")
    else:
        print("\n\nGoal state found!\n{}".format(node.get_state()))
        search.output_sequence_of_actions(tree)
        search.output_results()
