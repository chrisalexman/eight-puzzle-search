"""

"""

class Problem:

    def __init__(self):
        self.initial_state = []     # the initial state
        self.goal_state = []        # the goal state
        self.operators = []         # the available operators
        self.algorithm_choice = 0   # which of 3 algorithms the user wants

    # determine default or custom puzzle from the user
    def get_input(self):
        print("\nHello. This is the 8 puzzle solver.\n")
        user_input = input("Type '1' for the default puzzle, or '2' to enter your own.\n")

        # NOTE: uncomment below to bypass typing in input to run code
        # print("Type '1' for the default puzzle, or '2' to enter your own.")
        # user_input = '1'
        # print(user_input)

        # match the users input
        match user_input:
            case '1':
                self.set_default_puzzle()
            case '2':
                self.set_custom_puzzle()
            case _:
                print("ERROR. Please enter 1 or 2.\n")
                self.get_input()

        self.set_operators()
        self.set_algorithm()

    # set the initial and goal states for the default puzzle
    def set_default_puzzle(self):
        # trivial
        # self.initial_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

        # very easy
        # self.initial_state = [1, 2, 3, 4, 5, 6, 7, 0, 8]

        # easy
        # self.initial_state = [1, 2, 0, 4, 5, 3, 7, 8, 6]

        # doable
        # self.initial_state = [0, 1, 2, 4, 5, 3, 7, 8, 6]

        # oh boy
        # self.initial_state = [8, 7, 1, 6, 0, 2, 5, 4, 3]

        # impossible
        # self.initial_state = [1, 2, 3, 4, 5, 6, 8, 7, 0]

        # example
        self.initial_state = [1, 0, 3,
                              4, 2, 6,
                              7, 5, 8]

        # other
        # self.initial_state = [1, 2, 3,
        #                       4, 0, 6,
        #                       7, 5, 8]

        # self.initial_state = [1, 2, 3,
        #                       4, 8, 0,
        #                       7, 6, 5]

        self.set_goal_state()

    # get the custom puzzle from the user
    def set_custom_puzzle(self):
        print("\nEnter your puzzle.\nUse spaces between the numbers.\n('0' for the blank square)\n")

        # get row 1 of user input as a list of strings
        # uses .split() to not consider the blank spaces ' ' between the numbers
        self.initial_state = input("Enter row 1: ").split()

        # numer of rows, columns is the length of row 1 input list
        num_row_col = len(self.initial_state)

        # get input for remaining rows, add to initial state list
        for row in range(num_row_col - 1):
            self.initial_state += input("Enter row {}: ".format(row + 2)).split()

        self.set_goal_state()

    # set the goal state based on the initial state
    def set_goal_state(self):
        # list comprehension, convert list of strings to list of integers
        self.initial_state = [int(item) for item in self.initial_state]

        # the goal state is the sorted initial state, modified further below
        self.goal_state = sorted(self.initial_state)

        # move the blank square '0' from the front of the sorted list to the back
        # pop(0) removes the first element in the list, append(0) adds it to the back
        zero = self.goal_state.pop(0)
        self.goal_state.append(zero)

    # set the operators the blank square can do for the puzzle, moving up/down/left/right
    def set_operators(self):
        self.operators = ["up", "down", "left", "right"]

    # determine which algorithm the user wants to use to solve the puzzle
    def set_algorithm(self):
        print("\nEnter your algorithm choice.")
        self.algorithm_choice = input("1) Uniform Cost Search\n"
                                      "2) A* with the Misplaced Tile heuristic\n"
                                      "3) A* with the Euclidean distance heuristic\n")

        # NOTE: uncomment below to bypass typing in input to run code
        # print("1) Uniform Cost Search\n"
        #       "2) A* with the Misplaced Tile heuristic\n"
        #       "3) A* with the Euclidean distance heuristic")
        # self.algorithm_choice = '3'
        # print(self.algorithm_choice)

    # return the initial state, goal state, operators, and algorithm choice of the puzzle
    def get_initial_goal_operators_algorithm(self):
        return self.initial_state, self.goal_state, self.operators, self.algorithm_choice
