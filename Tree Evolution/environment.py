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


class Environment:

    def __init__(self, width, height):
        """
        Params
            height: The number of cells in the vertical dimension
            width: The number of cells in the horizontal dimension
        """

        # Observer list. Holds references to observers for notifying of updates.
        self.observers = list()

        # Store args
        self.width = width
        self.height = height

        self.time, self.env, self.sun, self.orgs = None, None, None, None
        self.initialize()

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
        self.orgs = dict()

    # Attach a new observer
    def attach(self, view):
        """
        Params
            view: The view instance which is observing this model.
        """
        self.observers.append(view)

    # Notify all observers of event
    def notify(self, event):
        """
        Notify all observers of an update in the data
        """
        for observer in self.observers:
            observer.notify(event)

    # Check if position falls within environment grid
    def in_bound(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    # Return the number of organisms within the environment
    def get_population(self):
        return len(self.orgs)

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

    # Instantiate a new organism, positioned at argument 'pos', and finally add to organism list
    def add_organism(self, x, y):
        # Check position is available
        if not (self.in_bound(x, y) and self.get_cell(x, y) is None):
            return

        # Create a new organism (a Tree in this case)
        org = Tree(self, x, y)

        # Get a hash value for the organism instance
        key = hash(org)

        # If key is present, rehash until available key is found
        while key in self.orgs.keys():
            key += 1

        # Finally, insert (key,value) into the hashmap, and update the environment to contain leaf at position
        self.orgs[key] = org
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
            self.add_organism(x, 0)

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
