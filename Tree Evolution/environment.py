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
import matplotlib.pyplot as plt

from tree import Tree


class Environment:

    def __init__(self, name):
        # List to hold trees
        self.trees = list()

        # Resource features are functions, where the input is position.
        # To account for resource competition, the update function will need to track
        # how the trees are trying to acquire resources.
        self.sunlight = None
        self.water = None
        self.nutrients = None

        # Plotting variables
        self.fig = plt.figure(figsize=(5, 5))
        self.fig.suptitle(name)
        self.ax = self.fig.gca()

    def add_tree(self):
        # Create a new tree object
        new_tree = Tree(self)
        self.trees.append(new_tree)
        return new_tree

    def pop_tree(self):
        # Removes the tree from the back of self.trees list
        self.trees.pop(-1)

    def update_plot(self):

        # Clear the ax
        self.ax.clear()

        # Plot the environment stuff here
        #
        #
        #

        # Now add all the trees on top of the environment
        for tree in self.trees:
            tree.plot(self.ax)

        return self.fig

    def update(self):
        # Update all the associated trees, taking into account competition
        # The environment can also be updated.
        pass
