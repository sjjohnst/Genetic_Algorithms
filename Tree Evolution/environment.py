"""
An environment class holds a collection of organisms (trees).
It has a set of features (e.g. sunlight, water, minerals, etc.)
Trees can be added/remove from a specific environment.
Handles the interaction(s) of features (resources) with organisms, given that there are multiple organisms
    - I.E. can calculate how much sunlight every tree gets, taking into account shading of trees.
"""

import numpy as np
from tree import Tree
import heapq


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array-value)).argmin()
    return idx


class Environment:

    def __init__(self):

        self.trees = []

    @staticmethod
    def sunlight(self, y):
        # Queries what the base sunlight level is at height y
        # Defines the sunlight function
        # March 30th: using ln(y + 1.25)
        # y=0 -> sun=0.223
        # as y->inf, sun->inf, with "diminishing returns"
        return np.log(y + 1.25)

    def calculate_tree_fitness(self, node: Tree):
        sun = self.sunlight(node.y)
        for child in node.children:
            sun += self.calculate_tree_fitness(child)
        return sun

    def sort_trees(self):
        # Sort the list of trees based on fitness
        return sorted(self.trees, key=self.calculate_tree_fitness, reverse=True)
