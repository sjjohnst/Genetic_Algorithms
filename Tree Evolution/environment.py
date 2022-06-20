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

    def __init__(self, width, height, name):
        """
        Params
            height: The number of cells in the vertical dimension
            width: The number of cells in the horizontal dimension
            name: A unique id to differentiate environments
        """

        # Store args
        self.width = width
        self.height = height
        self.name = name

        # List to hold trees
        self.trees = list()

        # Resource features are functions, where the input is position.
        # To account for resource competition, the update function will need to track
        # how the trees are trying to acquire resources.
        self.sunlight = self._init_sun()
        self.water = None
        self.nutrients = None

        # Plotting variables
        self.surf = pygame.Surface((width*cell_size, height*cell_size))

        # Where to blit the surface within the simulation window
        self.pos = (0, simulation_size[1]-self.height*cell_size)

        # Determines the zoom level of the environment
        self.zoom = 0

    def update(self):
        """
        Function to update the environment display. Reblits everything.
        """

        # Base colour is white
        self.surf.fill(WHITE)

        # For each cell, pad out to be the size of a cell
        sunlight_pixels = np.repeat(np.repeat(self.sunlight, cell_size, axis=0), cell_size, axis=1)
        pygame.surfarray.blit_array(self.surf, sunlight_pixels)

        # Plot all the trees, do a step
        for tree in self.trees:
            tree.plot(self.surf)

        # Plot grid lines over all
        # Vertical bars
        for i in range(0, self.width):
            pygame.draw.rect(self.surf, BLACK_A, (i*cell_size, 0, 1, self.height*cell_size))

        # Horizontal bars
        for i in range(0, self.height):
            pygame.draw.rect(self.surf, BLACK_A, (0, i*cell_size, self.width*cell_size, 1))

    def step(self):
        """ Perform a simulation step """
        for tree in self.trees:
            tree.step()

    def scroll(self, shift_x, shift_y):
        """
        Updates the blit position of this environment, in accordance with current scrolling.
        User will attempt to scroll in main.py, and this function handles how this affects
        the displaying of the environment.
        """

        pos_x, pos_y = self.pos

        pos_x = min(0, pos_x+shift_x)
        pos_y = min(0, pos_y+shift_y)

        if pos_x < 0:
            pos_x = max(simulation_size[0]-self.width*cell_size, pos_x+shift_x)
        if pos_y < 0:
            pos_y = max(simulation_size[1]-self.height*cell_size, pos_y+shift_y)

        self.pos = (pos_x, pos_y)

    def init_population(self, pop_size):
        """
        Initialize a new population of random trees.
        """
        assert pop_size > -1
        for i in range(pop_size):
            rand_x = np.random.randint(0, self.width-1)
            self.add_tree([rand_x, 0])

    def add_tree(self, origin):
        """
        Instantiate and then add a tree to this environment. Root positioned at 'origin'
        """
        new_tree = Tree(self, origin)
        self.trees.append(new_tree)
        return new_tree

    def _init_sun(self):
        """
        Creates a numpy matrix representing the sunlight value at each cell in the environment.
        """
        base_sun = np.ones((self.width, self.height, 3)) * 255
        grad_sun = np.ones_like(base_sun)

        # Modify the sunlight of each row according to height
        for i in range(self.height):
            grad_sun[:, self.height-i-1, :] = base_sun[:, i, :] * (i/self.height)

        f = 0.6
        grad_sun[:, int(f*self.height):, :] = grad_sun[:, int(f*self.height):int(f*self.height) + 1, :]
        # print(grad_sun[:, :, 0])
        return grad_sun
