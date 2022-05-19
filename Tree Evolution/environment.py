"""
Date: May 1st 2022
Author: Sam Johnston

Environment Class
An environment is a class that holds tree instances.
An environment has a set of features, such as sunlight, topology, hydrology, etc..
The trees interact with their associated environment,
such as when determining how many resources they collect on a given step.

Each tree is associated with exactly one environment.
Each environment can contain any number of trees.
"""
import numpy as np
import pygame

from parameters import *
from tree import Tree


class Environment:

    def __init__(self, height, width, name):
        """
        Params
            height: The number of cells in the vertical dimension
            width: The number of cells in the horizontal dimension
            name: A unique id to differentiate environments
        """

        # List to hold trees
        self.trees = list()

        # Resource features are functions, where the input is position.
        # To account for resource competition, the update function will need to track
        # how the trees are trying to acquire resources.
        self.sunlight = np.ones(simulation_size)
        self.water = None
        self.nutrients = None

        # Plotting variables
        self.surf = pygame.Surface(simulation_size)

    def update(self):
        # Update all trees and the environment resources
        # Base colour is white
        self.surf.fill(WHITE)

        # Then we plot a gradient based on the sunlight
        pygame.surfarray.blit_array(self.surf, self.sunlight)

        # Plot grid lines over all
        # Vertical bars
        for i in range(0, simulation_size[0]+cell_size, cell_size):
            pygame.draw.rect(self.surf, GREY, (i, 0, 1, simulation_size[1]))

        # Horizontal bars
        for i in range(0, simulation_size[1]+cell_size, cell_size):
            pygame.draw.rect(self.surf, GREY, (0, i, simulation_size[0], 1))

        # Plot all the trees
        for tree in self.trees:
            tree.plot(self.surf)

    def add_tree(self):
        # Create a new tree object
        new_tree = Tree(self)
        self.trees.append(new_tree)
        return new_tree

    def pop_tree(self):
        # Removes the tree from the back of self.trees list
        self.trees.pop(-1)
