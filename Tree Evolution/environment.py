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

        # Observer list. Holds references to observers for notifying of updates.
        self.observers = list()

        # Store args
        self.width = width
        self.height = height
        self.name = name

        # Resource features are functions, where the input is position.
        # To account for resource competition, the update function will need to track
        # how the trees are trying to acquire resources.
        self.sunlight = self._init_sun()
        self.water = None
        self.nutrients = None

        # List to hold trees
        self.trees = list()
        self.tiles = np.zeros_like(self.sunlight)

    def attach(self, view):
        """
        Params
            view: The view instance which is observing this model.
        """
        self.observers.append(view)

    def notify(self, event):
        """
        Notify all observers of an update in the data
        """
        for observer in self.observers:
            observer.notify(event)

    def get_state(self):
        """
        Return relevant data to the caller (View).
        """
        nodes = []
        edges = []
        for tree in self.trees:
            nodes.append(np.asarray(tree.F)[:,:2])
            edges.append(tree.Adj)

        return self.sunlight, nodes, edges

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

    def add_tree(self, origin):
        """
        Instantiate and then add a tree to this environment. Root positioned at 'origin'
        """
        new_tree = Tree(self, origin)
        self.trees.append(new_tree)
        return new_tree

    def init_population(self, pop_size):
        """
        Initialize a new population of random trees.
        """
        assert pop_size > -1
        for i in range(pop_size):
            rand_x = np.random.randint(0, self.width-1)
            self.add_tree([rand_x, 0])

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
