"""
Date: May 1st 2022
Author: Sam Johnston

Tree class definition.
Tree's are the base 'organism' of the evolution simulation.

A tree is a graph containing no cycles.
It is stored as a list of vertices and edges.
Each vertex will be given a unique id, in order to differentiate them.
Apart from the id, tree vertices will have other associated features,
which affect how the tree fares in the simulated environment.
Trees also have a set of general traits, which are not associated with any specific vertices.

"""
import numpy as np


class Tree:

    def __init__(self):

        # Vertices (V), Edges (E), Features (F)
        self.V = list()
        self.E = list()
        self.F = np.array()

        # Status variables
        self.sun = 0
        self.energy = 0

        # General Traits: Genes (G)
        self.G = np.array()
        self.mutation_rate = None

    def step(self):
        # Do a tree state update
        """
        The genes G as well as status variables are used to determine
        how the tree behaves in this step.

        The tree can do a number of actions:
            - Grow a new leaf
            - Extend a branch
            - Strengthen a leaf
            - ETC
        """
        pass

    def reproduce(self):
        # Create new genetics and return
        pass

