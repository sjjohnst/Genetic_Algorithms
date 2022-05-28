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
import copy


def flip(p):
    # Flip a coin with probability p of heads
    # Return True if heads, False if tails
    return np.random.uniform(0,1) <= p


class Tree:

    def __init__(self, environment, origin=(0, 0)):
        """
        Params:
            environment: The Environment instance that holds this tree
            origin (optional): The position of the trees 'root' vertex. Default is (0,0).
        """

        # A tree can only be instantiated within an environment.
        self.environment = environment

        # Vertices (V), Adjacency List (A), Features (F)
        self.V = list()
        self.A = dict()
        self.F = list()

        # Initialize a basic tree, single vertex.
        # original vertex has id = 0, and position of origin
        self.add_vertex(0, origin)

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

    def plot(self, surf, offset=0):
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
            point1 = (coords[i1] + 0.5)*cell_size
            x1 = point1[0] + offset*cell_size
            y1 = self.environment.height*cell_size - point1[1]
            for v2 in n:
                i2 = self.V.index(v2)
                point2 = (coords[i2] + 0.5)*cell_size
                x2 = point2[0] + offset * cell_size
                y2 = self.environment.height*cell_size - point2[1]
                pygame.draw.line(surf, BROWN, (x1, y1), (x2, y2), 3)

        # Now plot all vertices. (Leaves)
        # Plot the vertices as green points
        for coord in coords:
            # Use the offset to update the coordinate
            x = coord[0] + offset
            y = self.environment.height - coord[1] - 1
            pygame.draw.rect(surf, GREEN, (x*cell_size, y*cell_size, cell_size, cell_size))

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
        """
        Create a copy of this tree, and modify its structure slightly (mutation)
        """
        child = copy.deepcopy(self)

        # Add vertex
        if flip(0.2):
            pass

        # Add edge
        if flip(0.1):
            pass

        # Modify vertex positions
        if flip(0.1):
            pass

        return child
