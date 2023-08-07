"""

"""

from math import sqrt


class Node:

    def __init__(self):
        self.state = []             # the current state of the puzzle, a list of integers
        self.action = None          # viable actions, derived from operators ["up", "down", "left", "right"]

        self.path_cost = 0          # g(n), the path cost
        self.heuristic_cost = 0     # h(n), the heuristic cost
        self.estimated_cost = 0     # f(n) = g(n) + h(n), the estimated cost

    # set the data for the state, the list of operators, and the algorithm choice
    def set_data(self, state, action):
        self.state = state
        self.action = action

    # use indices and swap positions based on the operation, list[a], list[b] = list[b], list[a]
    def swap_elements(self, index_one, index_two):
        self.state[index_one], self.state[index_two] = self.state[index_two], self.state[index_one]

    # calculated the estimated cost, f(n) = g(n) + h(n)
    def calculate_estimated_cost(self, algorithm_choice, path_cost):
        # g(n), path cost
        self.path_cost = path_cost

        # h(n), heuristic cost
        match algorithm_choice:
            case '1':
                self.heuristic_cost = 0
            case '2':
                self.misplaced_tile_heuristic()
            case '3':
                self.euclidean_distance_heuristic()

        # f(n) = g(n) + h(n), estimated cost
        self.estimated_cost = self.path_cost + self.heuristic_cost

    # calculate the misplaced tile heuristic of the node state
    def misplaced_tile_heuristic(self):
        self.heuristic_cost = 0

        # loop through the state, check if the (index + 1) is the same as the tile number,
        # if no then there is a misplaced tile, add 1 to the heuristic cost
        for index, tile in enumerate(self.state):
            if tile != 0 and index + 1 != tile:
                self.heuristic_cost += 1

    # calculate the euclidean distance heuristic of the node state
    def euclidean_distance_heuristic(self):
        # here is how I calculated the euclidean distance heuristic
        # consider a 3x3 tile puzzle, indices(left) and tile numbers in the goal state(right)
        #
        #   0 1 2       1 2 3
        #   3 4 5       4 5 6
        #   6 7 8       7 8 0
        #
        # of note is that the index = (tile_number - 1), this doesn't include the blank tile
        #
        # the formula is c = sqrt(a^2 + b^2)
        # where 'a' is the left right horizontal difference, and 'b' is the up down vertical difference
        #
        # 1. find left right difference
        #   - the first row of the NxN matrix will include 0, 1, 2, ..., N - 1
        #   - the same column number on the next row will be greater by + num_row_col
        #   - therefore, just use the modulus operator
        #   - this changes a number in any column to the column number in the first row (e.g.  7 % 3 = 1)
        #   - do this for (index) and (tile_number - 1), then subtract these 2 values, take absolute value
        #   - the result is how far apart they are from each other horizontally
        #
        # 2. find up down difference
        #   - the first column of the NxN matrix will include 0, 1 * num_row_col, ..., (N - 1) * num_row_col
        #   - can loop through row one, do modulus of (index) and (tile_number - 1) to find the column it is in
        #   - use this to subtract away a number of columns, changing the value to something in column one
        #   - then divide (index) and (tile_number - 1) by num_row_column
        #   - this way they're in the range of 0 to (num_row_column - 1), similar to row one
        #   - subtract the 2 values the same as before, take absolute value
        #   - the result is how far apart they are from each other vertically

        # set initial values for heuristic cost
        self.heuristic_cost = 0

        # number of rows and columns, fill array with values only for the first row
        num_row_col = int(sqrt(len(self.state)))
        row_one = []
        for number in range(num_row_col):
            row_one.append(number)

        # variables to hold left/right and up/down distance between the index and tile
        lr_tile, lr_index, ud_tile, ud_index = 0, 0, 0, 0

        for index, tile in enumerate(self.state):

            if tile != 0 and index + 1 != tile:

                # find horizontal distance
                lr_tile = (tile - 1) % num_row_col
                lr_index = index % num_row_col

                # find vertical distance
                for row in row_one:
                    if (tile - 1) % num_row_col == row:
                        ud_tile = (tile - 1) - row
                    if index % num_row_col == row:
                        ud_index = index - row

                ud_tile = int(ud_tile / num_row_col)
                ud_index = int(ud_index / num_row_col)

                # horizontal distance, vertical distance
                left_right = abs(lr_tile - lr_index)
                up_down = abs(ud_tile - ud_index)

                # euclidean distance: c = sqrt(a^2 + b^2)
                self.heuristic_cost += sqrt(left_right ** 2 + up_down ** 2)

        # round down to the nearest integer to not overestimate
        self.heuristic_cost = int(self.heuristic_cost)

    # determine viable operators of the blank square from the given state
    def find_operators(self):

        state_size = len(self.state) - 1
        num_row_col = int(sqrt(len(self.state)))
        blank_square_index = self.state.index(0)

        # we have an NxN matrix with the following indices
        #
        #    3x3         4x4                5x5
        #   0 1 2     0 1  2  3        0  1  2  3  4
        #   3 4 5     4 5  6  7        5  6  7  8  9
        #   6 7 8     8 9 10 11       10 11 12 13 14
        #
        # how to determine if an action is viable based on the index
        #   - up:    new_index = current_index - num_row_col  (cannot when new index is less than 0)
        #   - down:  new_index = current_index + num_row_col  (cannot when new index is greater than state size)
        #   - left:  new_index = current_index - 1            (cannot when current index is multiple of num_row_col)
        #   - right: new_index = current_index + 1            (cannot when new index is multiple of num_row_col)

        # remove operators that are not viable, left with viable actions
        if blank_square_index - num_row_col < 0:
            self.action.remove('up')

        if blank_square_index + num_row_col > state_size:
            self.action.remove('down')

        if blank_square_index % num_row_col == 0:
            self.action.remove('left')

        if (blank_square_index + 1) % num_row_col == 0:
            self.action.remove('right')

    # get the state of the node
    def get_state(self):
        return self.state

    # get the viable actions of the node
    def get_actions(self):
        return self.action

    # get the data for the state and estimated cost
    def get_data(self):
        return tuple((self.state, self.estimated_cost))

    # get the path cost and heuristic cost
    def get_path_heuristic_costs(self):
        return self.path_cost, self.heuristic_cost

    # get the estimated code of the node
    def get_estimated_cost(self):
        return self.estimated_cost

    # get the length of the current state list (e.g. a 3x3 would be length 9)
    def get_state_length(self):
        return len(self.state)

    # get the index of the blank square (0)
    def get_blank_square_index(self):
        return self.state.index(0)
