"""
Date: May 1st 2022
Author: Sam Johnston

Tree class definition.
Tree's are the base 'organism' of the evolution simulation.

A tree is a graph containing no cycles.
It is stored as a list of vertices, and an adjacency list to store edges.
Each vertex will be given a unique id, in order to differentiate them.
Apart from the id, tree vertices will have other associated features,
which affect how the tree fares in the simulated environment.
Trees also have a set of general traits, which are not associated with any specific vertices.

"""
import numpy as np
from parameters import *
import pygame


class Tree:

    def __init__(self, environment):

        # A tree can only be instantiated within an environment.
        self.environment = environment

        # Vertices (V), Adjacency List (A), Features (F)
        self.V = list()
        self.A = dict()
        self.F = list()

        # Status variables
        # self.sun = 0
        # self.energy = 0
        #
        # # General Traits: Genes (G)
        # self.G = np.array()
        # self.mutation_rate = None

    def add_vertex(self, v, f):
        """
        Params
            v: vertex id
            f: vertex features, shape: (2) for (x,y)
        """

        assert len(f) == 2

        if v in self.V:
            print("Vertex already exists: %d" % v)

        else:
            self.V.append(v)
            self.F.append(f)

    def add_edge(self, v1, v2):
        """
        Params
            v1: vertex id 1
            v2: vertex id 2
        """
        assert v1 in self.V and v2 in self.V

        if v1 in self.A:
            self.A[v1].append(v2)
        else:
            self.A[v1] = [v2]

        if v2 in self.A:
            self.A[v2].append(v1)
        else:
            self.A[v2] = [v1]

    def plot(self, surf):
        """
        Params:
            surf: a pygame surface to blit onto
        """
        # Turn Features matrix into an array of coordinates.
        # Feature matrix has len(V) and second dimension 2
        coords = np.array(self.F)

        # Plot edges first (branches)
        # Loop over all vertices and their neighbours in Adjacency matrix
        for v1, n in self.A.items():
            i1 = self.V.index(v1)
            point1 = coords[i1]*cell_size + 0.5*cell_size
            for v2 in n:
                i2 = self.V.index(v2)
                point2 = coords[i2]*cell_size + 0.5*cell_size
                pygame.draw.line(surf, BROWN, point1, point2, 3)

        # Now plot all vertices. (Leaves)
        # Plot the vertices as blue points
        for coord in coords:
            pygame.draw.rect(surf, GREEN, (coord[0]*cell_size, coord[1]*cell_size, cell_size, cell_size))

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

