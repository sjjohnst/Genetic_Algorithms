"""
Date: July 5th 2022
Author: Sam Johnston

Environment Class
An environment is a class that holds organism instances.
An environment has a set of features, such as sunlight, topology, hydrology, etc..
The organisms interact with their associated environment,
such as when determining how many resources they collect on a given step.

Each tree is associated with exactly one environment.
Each environment can contain any number of organisms.
"""

import numpy as np
from tree import Tree
import event
import random


class Environment:

    def __init__(self, width, height):
        """
        Params
            height: The number of cells in the vertical dimension
            width: The number of cells in the horizontal dimension
        """

        # Store args
        self.width = width
        self.height = height

        self.time, self.env, self.sun, self.trees = None, None, None, None
        self.initialize()

        # Dictionary to hold cell updates.
        # Maps old locations to new locations, facilitating the view to update required cells
        self.cell_updates = dict()

        # Subscribe to events
        event.subscribe("NewNode", self.new_node)
        event.subscribe("MoveNode", self.move_node)

    # Run a simulation step
    def step(self):
        """
        Every step of the simulation:
            - Collect all resources, pass to trees
            - Get all trees to do a step (make decision)
            - Update accordingly
        """

        # Begin by emptying 'cell_updates'. All new updates will be added by trees.
        self.cell_updates.clear()

        # Shuffle the order of the trees, (no preferential treatment)
        tree_list = list(self.trees.values())
        random.shuffle(tree_list)
        for tree in tree_list:
            tree.step()

        # If there were cell updates, post event
        if not self.cell_updates:
            event.post_event("CellUpdates", self.cell_updates)

        self.time += 1

    # Initialize environment base
    def initialize(self):
        """
        Initialize the environment with base features
        """
        # The number of time steps run.
        self.time = 0

        # The environment is an empty space of cells.
        # These cells are filled by vertices of the trees.
        self.env = [[None for x in range(self.width)] for y in range(self.height)]

        # Resource features are functions, where the input is position.
        # To account for resource competition, the update function will need to track
        # how the trees are trying to acquire resources.
        self.sun = self._init_sun()

        # Dictionary (hash map) to store organisms
        self.trees = dict()

    # Check if position falls within environment grid
    def in_bound(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    # Return the number of organisms within the environment
    def get_population(self):
        return len(self.trees)

    # Return the sun value at input position
    def get_sun(self, x, y):
        # Assert position in bounds
        if not self.in_bound(x, y):
            return None

        return self.sun[y][x]

    # Return the value in self.env at input position
    def get_cell(self, x, y):
        if not self.in_bound(x, y):
            return False

        return self.env[y][x]

    # Instantiate a new tree, positioned at argument 'pos', and finally add to organism list
    def add_tree(self, x, y):
        # Check position is available
        if not (self.in_bound(x, y) and self.get_cell(x, y) is None):
            return

        # Create a new tree
        tree = Tree(self, x, y)

        # Get a hash value for the organism instance
        key = hash(tree)

        # If key is present, rehash until available key is found
        while key in self.trees.keys():
            key += 1

        # Finally, insert (key,value) into the hashmap, and update the environment to contain leaf at position
        self.trees[key] = tree
        self.env[y][x] = key

    # Initialize a new population of random organisms
    def init_population(self, size):
        """
        Initialize a new population of randomized organisms.
        """
        # Find all available tiles in the bottom row of the environment
        bot_row = self.env[-1]
        available = []
        for x, v in enumerate(bot_row):
            if v is None:
                available.append(x)

        # Select 'size' positions from above (if possible)
        size = min(size, len(available))
        x_positions = np.random.choice(available, size, replace=False)

        for x in x_positions:
            self.add_tree(x, 0)

    # Initialize the sun resource as a numpy array, with custom distribution
    def _init_sun(self):
        """
        Creates a numpy matrix representing the sunlight value at each cell in the environment.
        """
        base_sun = np.ones((self.height, self.width))
        grad_sun = np.ones_like(base_sun)

        # Modify the sunlight of each row according to height
        for i in range(self.height):
            grad_sun[i, :] = base_sun[i, :] * ((i+1)/self.height)

        f = 0.2
        # Create a base sunlight level for all heights below a threshold of 'f' percent
        grad_sun[:int(f*self.height), :] = grad_sun[int(f*self.height):int(f*self.height) + 1, :]
        return grad_sun

    # Called when a new node is added to the environment space
    def new_node(self, data):
        """
        data: [key, new_pos];
            - key: The unique tree hash key, for the tree adding said node.
            - new_pos: (x,y) position of the new node.
        """
        # Extract data
        key, pos = data
        x, y = pos

        # Now add cell to the environment grid
        self.env[y][x] = key

        # Finally, add a mapping to the 'cell_updates' dictionary, so View can be later notified.
        self.cell_updates[tuple(pos)] = tuple(pos)

    # Called when a node in the grid is shifted by its tree
    def move_node(self, data):
        """
        data: [old_pos, new_pos]
            - old_pos: (x,y) position of the nodes previous location
            - new_pos: (x,y) position of the nodes new location
        """
        # Extract data
        old_pos, new_pos = data
        x1, y1 = old_pos
        x2, y2 = new_pos

        # Move node
        self.env[y2][x2] = self.env[y1][x1]
        self.env[y1][x1] = None

        # Add a mapping to 'cell_updates'
        self.cell_updates[tuple(old_pos)] = tuple(new_pos)


#################################################################
## TEST
#################################################################
#
# env = Environment(10, 5)
#
# env.init_population(3)
# print(env.get_population())
# print(env.env)
#
# for i in range(5):
#     env.step()
#     print(env.cell_updates)
# print(env.env)
