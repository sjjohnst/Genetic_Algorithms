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


def softmax(x):
    f = np.exp(x - np.max(x))  # shift values
    return f / f.sum(axis=0)


class Tree:

    def __init__(self, environment, origin=(0, 0)):
        """
        Params:
            environment: The Environment instance that holds this tree
            origin (optional): The position of the trees 'root' vertex. Default is (0,0).
        """

        # A tree can only be instantiated within an environment.
        self.environment = environment

        # Adjacency List (Adj), Adjacency Matrix (A), Features (F)
        self.Adj = list()
        self.A = list()

        # Features: [x, y, strength, sunlight, stored energy]
        self.F = list()

        # Genetics
        self.d = 5  # number of features
        self.e = 5  # number of possible decisions
        self.W1 = np.random.randn(self.d, self.e)
        self.W2 = np.random.randn(self.d, self.e)

        # Initialize a basic tree, single vertex.
        # original vertex has id = 0, and position of origin
        self.add_vertex(origin)

    def add_vertex(self, pos):
        """
        Adds a new vertex, with default features f: [x,y,strength,sunlight,stored energy]
        Params
            pos: vertex position (x,y)
        """

        assert len(pos) == 2

        # Add a new empty list to the adjacency list
        self.Adj.append(list())

        # Create default feature list, [x,y,strength,sunlight,stored energy]
        features = [pos[0], pos[1], 1, 0, 0]
        self.F.append(features)

    def add_edge(self, v1, v2):
        """
        Adds an edge between vertex v1 and v2
        Params
            v1: vertex index 1
            v2: vertex index 2
        """

        # Assert that both indices provided are in range
        assert v1 < len(self.Adj) and v2 < len(self.Adj)

        # Add edges v1 <-> v2 to Adjacency list
        self.Adj[v1].append(v2)
        self.Adj[v2].append(v1)

    def add_leaf(self, v):
        """
        Adds a new node, and connects it to node v.
        Params
            v: the parent node to add a leaf to
        """

        # Assert its a valid index
        assert v < len(self.F)

        n = len(self.F)

        # The leafs position will be same as v_pos, but with y+1
        l_pos = [self.F[v][0], self.F[v][1]+1]
        if not self._pos_available(l_pos):
            return

        # Now add a new vertex, then a leaf
        self.add_vertex(l_pos)
        self.add_edge(v, n)

    def plot(self, surf, offset=0):
        """
        Params:
            surf: a pygame surface to blit onto
        """
        # Extract coordinates from the feature matrix
        coords = np.array(self.F)[:,:2]

        # Plot edges first (branches)
        # Loop over all vertices and their neighbours in Adjacency matrix
        for v1, n in enumerate(self.Adj):
            point1 = (coords[v1] + 0.5)*cell_size
            x1 = point1[0] + offset*cell_size
            y1 = self.environment.height*cell_size - point1[1]
            for v2 in n:
                point2 = (coords[v2] + 0.5)*cell_size
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
        """
        The genes W as well as status variables are used to determine
        how the tree behaves in this step.

        The tree can do a number of actions:
            - Grow a new leaf
            - Extend a branch
            - Strengthen a leaf
            - ETC
        """

        # Convert the adjacency list into a numpy adjacency matrix
        V = len(self.Adj)
        self.A = self._convert_adj(self.Adj)

        # Add the identity to add self connections
        A = np.asarray(self.A)
        A = A + np.identity(A.shape[0])

        # Convert the feature matrix into a numpy array
        F = np.asarray(self.F)

        # Pass through the MLPs. Matrix multiplication is associative.
        Y = np.matmul(A, np.matmul(F, self.W1))
        Z = np.matmul(A, np.matmul(F, self.W2))

        # Apply activation function
        Z = np.tanh(Z)

        # Use Y for decision
        for v in range(V):
            # For the first vertex (the root), cannot shift x or y
            if v == 0:
                a = np.random.choice(self.e-2, p=softmax(Y[v, 2:]))
                a += 2

            else:
                # Use the probabilistic distribution of this row to select an action (a)
                a = np.random.choice(self.e, p=softmax(Y[v]))

            # Get the factor f, located at vertex v, action a, from the Z matrix
            f = Z[v, a]

            # Perform action (a) on vertex (v) in helper function, by factor f
            self.execute(v, a, f)

    def execute(self, v, a, f):
        """
        Performs action a on vertex v, by factor f
        Params:
            v: index of vertex.
            a: action id.
            f: Some actions require a factor. f is 'quantity' of change.
        """
        # Features: [x, y, strength, sunlight, stored energy]
        if 3 > a >= 0:
            # Change feature x,y,or strength by factor f
            self.F[v][a] += round(f)
        elif a == 3:
            # Add a child to the node
            self.add_leaf(v)
        else:
            # Invalid
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

    def _convert_adj(self, Adj):
        """
        Converts adjacency list into adjacency matrix
        Params:
            Adj: The adjacency list. A python list of lists
        """

        # The number of vertices V, will always be length of Adj
        # Enforced because we have no 'floating' leaves
        V = len(Adj)

        # Initialize a matrix of zeros, shape (V,V)
        matrix = [[0 for j in range(V)]
                  for i in range(V)]

        # Add a 1 to every entry where an edge exists
        for i in range(V):
            for j in Adj[i]:
                matrix[i][j] = 1

        return matrix

    def _pos_available(self, pos):
        """
        Queries the environment, checks if a grid position is available
        Params:
            pos: [x,y]
        """

        # First check if this tree occupies the position
        coords = [f[:2] for f in self.F]
        if pos in coords:
            return False

        # Now check against the other trees

        # If all checks pass, return True
        return True

