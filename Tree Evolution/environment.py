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

class Environment:

    def __init__(self):
        # Dictionary to hold the attached trees
        self.trees = dict()

        # Resource features are functions, where the input is position.
        # To account for resource competition, the update function will need to track
        # how the trees are trying to acquire resources.
        self.sunlight = None
        self.water = None
        self.nutrients = None

    def attach(self, tree):
        # Attach a new tree to the environment
        pass

    def detach(self, tree):
        # Detach a specific tree from the environment
        pass

    def update(self):
        # Update all the associated trees, taking into account competition
        # The environment can also be updated.
        pass

