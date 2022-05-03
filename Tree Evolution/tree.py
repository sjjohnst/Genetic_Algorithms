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


class Tree:

    def __init__(self):

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

    def plot(self, ax):
        """
        Params:
            ax: A matplotlib axis to plot this tree onto
        """

        # Feature matrix has len(V) and second dimension 2
        coords = np.array(self.F)

        # Plot the vertices as blue points
        ax.scatter(coords[:,0], coords[:,1], color='blue')

        # Now plot all the edges.
        # Loop over all vertices and their neighbours in Adjacency matrix
        for v1, n in self.A.items():
            i1 = self.V.index(v1)
            for v2 in n:
                i2 = self.V.index(v2)
                edges = coords[[i1, i2], :]
                ax.plot(edges[:, 0], edges[:, 1], color='orange')

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

