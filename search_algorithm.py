"""

"""

from node import Node
from tree import Tree
from math import sqrt


class SearchAlgorithm:

    def __init__(self):
        self.frontier = {}              # frontier, list of leaf nodes that can be expanded
        self.explored_set = {}          # explored set, set of the nodes that have been expanded

        self.num_nodes_expanded = 0     # the number of nodes expanded
        self.max_queue_size = 0         # the maximum size of the queue
        self.depth = 0                  # the depth of the goal node

        self.node = None                # the current node the algorithm is looking at
        self.goal_state = []            # goal state of the initial state

        self.tree = None                # the search tree that stores all the nodes
        self.tree_dict = {}             # dictionary to store the tree nodes

    # idea of comments below from lecture slides, 02. Blind Search
    # function GRAPH-SEARCH(problem) returns a solution, or failure
    def graph_search(self, initial_state, goal_state, operators, algorithm_choice):

        print("\nBEGIN GRAPH SEARCH\n-----------------------------------------")

        # set up the root node with initial_state, goal_state, operators, algorithm_choice
        self.create_root_node(initial_state, goal_state, operators, algorithm_choice)

        # initialize the frontier using the initial state of problem
        #   - frontier is a priority queue, but implemented as a dictionary of key : value pairs
        #   - the key is the cost, the value is the node object
        self.frontier[self.node.get_estimated_cost()] = [self.node]

        # set up the root of the tree, add to the dictionary
        self.tree = Tree()
        self.tree.set_node(self.node)
        self.tree_dict[self.node.get_estimated_cost()] = [self.tree]

        # initialize the explored set to be empty
        self.explored_set = {}

        # loop do
        while 1:
            # if the frontier is empty then return failure (None)
            if len(self.frontier) == 0:
                return None, None

            # choose a leaf node and remove it from the frontier
            # sort priority queue (dictionary) in ascending order by the key (estimated_cost)
            self.frontier = dict(sorted(self.frontier.items()))

            # look at the key : value in the front of the dictionary
            cost, object_list = next(iter(self.frontier.items()))
            # object_list.sort()

            # set the node to the object at the front of the list
            self.node = object_list[0]

            # the lowest cost is at the front, remove it from the frontier, update the dictionary
            object_list.pop(0)
            self.frontier[cost] = object_list

            # remove the estimated_cost key if no objects in the list
            if len(object_list) == 0:
                self.frontier.pop(cost)

            # find the corresponding node in the tree dictionary
            if cost in self.tree_dict:
                object_list = list(self.tree_dict.get(cost))
                for obj in object_list:
                    node = obj.get_node()
                    if node == self.node:
                        self.tree = obj

            # if the node contains a goal state then return the corresponding solution
            if self.node.get_state() == self.goal_state:
                return self.node, self.tree

            # add the node to the explored set
            # check if the estimated_cost is a key in the explored set
            if self.node.get_estimated_cost() in self.explored_set:
                # get the list of objects, add the new node object, update the dictionary
                object_list = list(self.explored_set.get(self.node.get_estimated_cost()))
                object_list.append(self.node)
                self.explored_set[self.node.get_estimated_cost()] = object_list
            else:
                # update the dictionary with the node object
                self.explored_set[self.node.get_estimated_cost()] = [self.node]

            # check if the maximum number of nodes in the explored set has increased
            if len(self.explored_set) > self.max_queue_size:
                self.max_queue_size = len(self.explored_set)

            # expand the chosen node, adding the resulting nodes to the frontier
            # only if not in the frontier or explored set
            #   - increase the number of nodes expanded by 1
            operators = self.node.get_actions()
            parent = self.node

            # output the node that was just expanded, increase the number of nodes expanded by 1
            self.output_expanded_node()
            self.num_nodes_expanded += 1

            # loop through the viable actions of the node, do that action to create a child node
            # add to frontier if not in frontier and not in explored set
            for operator in operators:
                child = self.create_child(parent, operator, algorithm_choice)

                # get the child data, a tuple of the state and estimated cost
                child_data = child.get_data()

                # bool for if the child node is in the frontier, explored set
                in_frontier = False
                in_explored_set = False

                # check if the estimated_cost is a key in the frontier, check if child in list of nodes
                if child.get_estimated_cost() in self.frontier:
                    object_list = list(self.frontier.get(child.get_estimated_cost()))
                    for obj in object_list:
                        node_data = obj.get_data()
                        if node_data == child_data:
                            in_frontier = True

                # check if the estimated_cost is a key in the explored set, check if child in list of nodes
                if child.get_estimated_cost() in self.explored_set:
                    object_list = list(self.explored_set.get(child.get_estimated_cost()))
                    for obj in object_list:
                        node_data = obj.get_data()
                        if node_data == child_data:
                            in_explored_set = True

                # child object not in frontier or explored set
                if not in_frontier and not in_explored_set:

                    # check if the estimated_cost is a key in the frontier
                    if child.get_estimated_cost() in self.frontier:
                        # get the list of objects, add the new node object, update the dictionary
                        object_list = list(self.frontier.get(child.get_estimated_cost()))
                        object_list.append(child)
                        self.frontier[child.get_estimated_cost()] = object_list
                    else:
                        # update the dictionary with the node object
                        self.frontier[child.get_estimated_cost()] = [child]

                # create another tree object, set the node as the child node, the parent as the current tree node
                subtree = Tree()
                subtree.set_node(child)
                subtree.set_parent(self.tree)

                # add the tree object to the dictionary
                if child.get_estimated_cost() in self.tree_dict:
                    object_list = list(self.tree_dict.get(child.get_estimated_cost()))
                    object_list.append(subtree)
                    self.tree_dict[child.get_estimated_cost()] = object_list
                else:
                    self.tree_dict[child.get_estimated_cost()] = [subtree]

    # set up the root node with initial_state, goal_state, operators, algorithm_choice
    def create_root_node(self, initial_state, goal_state, operators, algorithm_choice):
        self.goal_state = goal_state

        self.node = Node()
        self.node.set_data(initial_state, operators)
        self.node.calculate_estimated_cost(algorithm_choice, 0)
        self.node.find_operators()

    # create children nodes based on node state and viable operators
    def create_child(self, parent, operator, algorithm_choice):
        # create new child node for each operator, set data, set parent node
        # lists are mutable data structures, use .copy() to create a copy of parent.state
        self.node = Node()
        self.node.set_data(parent.state.copy(), ["up", "down", "left", "right"])

        # number of rows and columns, index of the blank (0) square
        num_row_col = int(sqrt(self.node.get_state_length()))
        blank_square_index = self.node.get_blank_square_index()

        # use indices and swap positions based on the operation, list[a], list[b] = list[b], list[a]
        match operator:
            case 'up':
                self.node.swap_elements(blank_square_index, blank_square_index - num_row_col)
            case 'down':
                self.node.swap_elements(blank_square_index, blank_square_index + num_row_col)
            case 'left':
                self.node.swap_elements(blank_square_index, blank_square_index - 1)
            case 'right':
                self.node.swap_elements(blank_square_index, blank_square_index + 1)

        # get the path cost of the parent node
        path_cost, heuristic = parent.get_path_heuristic_costs()

        # calculate estimated cost, find viable operators for the child node
        self.node.calculate_estimated_cost(algorithm_choice, path_cost + 1)
        self.node.find_operators()

        return self.node

    # output the expanded node with g(n) and h(n)
    def output_expanded_node(self):
        state = self.node.get_state()
        num_row_col = int(sqrt(self.node.get_state_length()))
        path_cost, heuristic_cost = self.node.get_path_heuristic_costs()

        # output a message depending on if the node is the start state (path_cost == 0), or not
        if path_cost == 0:
            print("Expanding state", end='')
        else:
            print("\n\nThe node to expand has g(n) = {}, h(n) = {}".format(path_cost, heuristic_cost), end='')

        # loop through the state list, print it out in a NxN matrix format
        for index, element in enumerate(state):
            if index % num_row_col == 0:
                print("\n", end='')
            print(element, end=' ')

        # output message if not in the start state (path_cost == 0)
        if path_cost != 0:
            print("\t\tExpanding this node ...")

    # output the results after finding the goal state
    def output_results(self):

        # loop through the lists of node objects in the explored set dictionary, sum them to find max queue size
        self.max_queue_size = 0

        for object_list in self.explored_set.values():
            self.max_queue_size += len(object_list)

        print("\n\nRESULTS\n-------------------------------------")
        print("The number of nodes expanded  : {}".format(self.num_nodes_expanded))
        print("The maximum size of the queue : {}".format(self.max_queue_size))
        print("The depth of the goal node    : {}".format(self.depth))

    # output the sequence of actions to get from the initial state to the goal state
    def output_sequence_of_actions(self, tree):
        print("\n\nSEQUENCE OF ACTIONS\n-------------------------------------")

        node = tree.get_node()
        num_row_col = int(sqrt(len(node.get_state())))

        # initial value of the sequence is the state of the goal node
        sequence = [node.get_state()]
        parent = tree.get_parent()

        # go to the parent node and save the state, stop when at the start state who has a parent 'None'
        while parent is not None:
            node = parent.get_node()
            sequence.append(node.get_state())
            parent = parent.get_parent()

        # we added node states in the order of goal -> ... -> start, reverse this list to now have start -> ... -> goal
        sequence.reverse()

        # the depth of our graph search is how many actions it took to get from the start node to end node
        # need to subtract 1 as the start node is depth = 0
        self.depth = len(sequence) - 1

        # loop through the sequence, a list of lists, each list is the state of a node (e.g. [1,2,3,4,5,6,7,0,8])
        # compare each state to the subsequent state to see if the blank square moved up, down, left, or right
        # the sequence[:-1] means we don't look at the last element of the list
        for index, action in enumerate(sequence[:-1]):
            # store the index of the blank square (0) for the current state
            blank_square_index = action.index(0)

            # look at the next state in the sequence, find the index of the blank square (0)
            action_next = sequence[index + 1]
            blank_square_index_next = action_next.index(0)

            # hold the difference between the indexes of the blank squares
            difference = blank_square_index_next - blank_square_index

            # we have an NxN matrix with the following indices
            #
            #    3x3         4x4                5x5
            #   0 1 2     0 1  2  3        0  1  2  3  4
            #   3 4 5     4 5  6  7        5  6  7  8  9
            #   6 7 8     8 9 10 11       10 11 12 13 14
            #
            # how to determine which direction (up, down, left, or right) the blank square (0) moved
            #   - up:    blank_square_index_next - blank_square_index = -num_row_col
            #   - down:  blank_square_index_next - blank_square_index = num_row_col
            #   - left:  blank_square_index_next - blank_square_index = -1
            #   - right: blank_square_index_next - blank_square_index = 1

            if difference == -num_row_col:
                print("move up")
            elif difference == num_row_col:
                print("move down")
            elif difference == -1:
                print("move left")
            elif difference == 1:
                print("move right")

    # # idea of comments below from reading material 2, general-search-and-uniform-cost-search
    # # function CHILD-NODE(problem, parent, action) returns a node
    # def child_node(self):
    #     # return a node with
    #         # STATE = problem.Result(parent.STATE, action),
    #         # PARENT = parent, ACTION = action,
    #         # PATH-COST = parent.PATH-COST + problem.STEP-COST(parent.STATE, action)

    # # idea of comments below from lecture slides, 02. Blind Search
    # # function TREE-SEARCH(problem) returns a solution, or failure
    # def tree_search(self):
    #     # initialize the frontier using the initial state of problem
    #     # loop do
    #         # if the frontier is empty then return failure
    #         # choose a leaf node and remove it from the frontier
    #         # if the node contains a goal state then return the corresponding solution
    #         # expand the chosen node, adding the resulting nodes to the frontier
