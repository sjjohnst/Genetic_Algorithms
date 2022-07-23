"""
Date: July 5th 2022
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
import copy


def flip(p):
    # Flip a coin with probability p of heads
    # Return True if heads, False if tails
    return np.random.uniform(0,1) <= p


def softmax(x):
    f = np.exp(x - np.max(x))  # shift values
    return f / f.sum(axis=0)


# Convert adjacency list to adjacency matrix
def convert_adj(adj):
    """
    Converts adjacency list into adjacency matrix
    Params:
        Adj: The adjacency list. A python list of lists
    """

    # The number of vertices V, will always be length of Adj
    # Enforced because we have no 'floating' leaves
    V = len(adj)

    # Initialize a matrix of zeros, shape (V,V)
    matrix = [[0 for j in range(V)]
              for i in range(V)]

    # Add a 1 to every entry where an edge exists
    for i in range(V):
        for j in adj[i]:
            matrix[i][j] = 1

    return matrix


# Find the path from node to target in tree
def dfs(tree: dict, seq: list, node: int, target: int):
    """
    tree: a Tree object
    seq: current path taken
    node: current node visiting
    target: target node to find
    """

    # Add current node to sequence
    seq.append(node)

    # Found target, break
    if node == target:
        return
    else:
        for n in tree[node]:
            # Skip parent nodes
            if n in seq:
                continue
            # Recurse into child node
            dfs(tree, seq, n, target)
            # Found target, break
            if seq[-1] == target:
                return

    # Dead end, remove from sequence
    seq.pop()


class Tree:

    def __init__(self, environment, x, y):
        """
        Params:
            environment: The Environment instance that holds this tree
            x: the trees x position
            y: the trees y position
        """

        # A tree can only be instantiated within an environment.
        self.env = environment

        # Adjacency List (Adj), Adjacency Matrix (A), Features (F)
        self.Adj = dict()
        self.A = list()

        # Features: [x, y, strength, #children, sunlight, stored energy]
        self.F = dict()

        # Genetics
        self.d = 6  # number of features
        self.e = 5  # number of possible decisions
        self.W1 = np.random.randn(self.d, self.e)
        self.W2 = np.random.randn(self.d, self.e)

        # Initialize a basic tree, single vertex.
        # original vertex has id = 0, and position of origin
        self.root = 0
        self.last_id = -1
        self.add_vertex((x, y))

    # Equality operator to compare two trees in the environment
    def __eq__(self, other):
        return self.W1 == other.W1 and self.W2 == other.W2

    # Hash function so that environment can map leaves to tree instances
    def __hash__(self):
        return hash(self.W1.sum() + self.W2.sum())

    # Add a new vertex at position (pos)
    def add_vertex(self, pos):
        """
        Adds a new vertex, with default features f: [x,y,strength,sunlight,stored energy]
        Params
            pos: vertex position (x,y)
        """

        assert len(pos) == 2

        # Create a new id for this vertex
        self.last_id = self.last_id + 1

        # Add a new empty list to the adjacency list
        self.Adj[self.last_id] = list()

        # Create default feature list, [x,y,strength,#children,sunlight,stored energy]
        features = [pos[0], pos[1], 1, 0, 0, 0]
        self.F[self.last_id] = features

    # Add an edge between vertex v1 and v2
    def add_edge(self, v1, v2):
        """
        Adds an edge between vertex v1 and v2.
        Params
            v1: vertex index 1 (parent)
            v2: vertex index 2 (child)
        """

        # Assert that both indices provided are in range
        assert v1 < len(self.Adj) and v2 < len(self.Adj)

        # Add edges v1 <-> v2 to Adjacency list
        self.Adj[v1].append(v2)
        self.Adj[v2].append(v1)

        # Need to update number of children feature for parent and all ancestors
        # Number of children is feature at index 3
        ancestors = []
        dfs(self.Adj, ancestors, self.root, v2)

        for a in ancestors:
            self.F[a][3] += 1

    # Perform a simulation step; Make decisions and perform actions for this time step.
    def step(self):
        """
        The tree can do a number of actions:
            - Grow a new leaf
            - Extend a branch
            - Strengthen a leaf
            - ETC
        """

        # Convert the adjacency list into a numpy adjacency matrix
        V = len(self.Adj)
        self.A = convert_adj(self.Adj)

        # Add the identity to add self connections
        A = np.asarray(self.A)
        A = A + np.identity(A.shape[0])

        # Convert the feature matrix into a numpy array
        F = np.asarray(list(self.F.values()))
        F = (F - F.min()) / (F.max() - F.min())

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

    # Perform action a on vertex v, by factor f
    def execute(self, v, a, f):
        """
        Params:
            v: index of vertex.
            a: action id.
            f: Some actions require a factor. f is 'quantity' of change.
        """
        # Features: [x, y, strength, num children, sunlight, stored energy]
        if 3 > a >= 0:
            # Change feature x,y,or strength by factor f
            self.F[v][a] += round(f)
        elif a == 3:
            print("Trying to add child")
            # Add a child to the node
            self.add_leaf(v)
        else:
            # Invalid
            pass

    # Add a leaf node directly above parent v
    def add_leaf(self, v):
        """
        Adds a new node, and connects it to node v.
        Params
            v: the parent node to add a leaf to
        """

        # Assert its a valid index
        assert v < len(self.Adj)

        # Perform strength check, to determine if new leaf can be added
        if not self.strength_check(v):
            return

        # The leafs position will be same as v_pos, but with y+1
        l_pos = [self.F[v][0], self.F[v][1] + 1]
        # if not self._pos_available(l_pos):
        #     return

        # Now add a new vertex, then a leaf
        self.add_vertex(l_pos)
        self.add_edge(v, self.last_id)

    # Check if v and all its ancestors can support an additional child
    def strength_check(self, v):
        """
        v: node to find in tree
        """

        # Use DFS to find all ancestors of node v. Result is stored in seq
        seq = []
        dfs(self.Adj, seq, self.root, v)

        # Perform a strength check, to determine if tree can add a new leaf
        meets_strength = True
        for a in seq:
            # strength is index 2
            # number of children is index 3
            # if strength is less than or equal to number children, fail
            if self.F[a][2] <= self.F[a][3]:
                meets_strength = False
                break

        return meets_strength

    # Return true if environment cell at 'pos' is empty, false otherwise
    def _pos_available(self, pos):
        return self.env.get_cell(pos[0], pos[1]) is None


""" Test """
# tree1 = Tree(None, 0, 0)
# print(tree1.Adj)
#
# tree1.add_vertex((1, 1))
# tree1.add_vertex((2, 3))
# tree1.add_vertex((4, 1))
# tree1.add_vertex((4, 3))
# tree1.add_vertex((2, 5))
#
# tree1.add_edge(0, 1)
# tree1.add_edge(0, 3)
# tree1.add_edge(1, 2)
# tree1.add_edge(2, 4)
# tree1.add_edge(3, 5)
#
# print(tree1.Adj)
# print(convert_adj(tree1.Adj))
#
# seq = []
# dfs(tree1.Adj, seq, 0, 3)
# print(seq)
# seq = []
# dfs(tree1.Adj, seq, 0, 2)
# print(seq)

tree2 = Tree(None, 0, 0)

print(tree2.F)
print(tree2.Adj)
for i in range(20):
    tree2.step()
print(tree2.F)
print(tree2.Adj)
