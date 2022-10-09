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
import events


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

        # Features: [x, y, strength, #children, energy]
        self.F = dict()

        # Initialize a basic tree, single vertex.
        # original vertex has id = 0, and position of origin (0,0)
        self.root = 0
        self.age = 0
        self.last_id = -1
        self.add_vertex((0, 0))

        # We store the provided position, which is the 'true' position of the root in the environment
        # All node positions are therefore relative to (0,0).
        self.origin = (x, y)

        # Genetics
        self.d = 5  # number of features
        self.e = 5  # number of possible decisions
        self.W1 = np.random.randn(self.d, self.e)
        self.W2 = np.random.randn(self.d, self.e)

    # Equality operator to compare two trees in the environment
    def __eq__(self, other):
        return self.W1 == other.W1 and self.W2 == other.W2

    # Hash function so that environment can map leaves to tree instances
    def __hash__(self):
        return hash(self.origin)

    # Return all edges in this tree
    def get_edges(self):
        edges = set()
        for v1, adj in self.Adj.items():
            for v2 in adj:
                edge = (v1, v2)
                edges.add(edge)
        return edges

    # Return the position of vertex v
    def get_vertex_pos(self, v):
        if v in self.F.keys():
            return self.F[v][0] + self.origin[0], self.F[v][1] + self.origin[1]

    # Return total number of vertices in the Tree
    def get_number_vertices(self):
        return len(self.Adj.keys())

    # Return the sum of all nodes stored energy
    def get_total_energy(self):
        # Convert F to numpy array
        F = np.asarray(list(self.F.values()))

        # Slice last column to get stored energy
        stored_energy = np.sum(F[:,4])

        return stored_energy

    # Add a new vertex at position (pos)
    def add_vertex(self, pos):
        """
        Adds a new vertex, with default features f: [x,y,strength,energy]
        Params
            pos: vertex position (x,y)
        """

        assert len(pos) == 2

        # Create a new id for this vertex
        self.last_id = self.last_id + 1

        # Add a new empty list to the adjacency list
        self.Adj[self.last_id] = list()

        # Create default feature list, [x, y, strength, #children, energy]
        features = [pos[0], pos[1], 1, 0, 0]
        self.F[self.last_id] = features

    # Add an edge between vertex v1 and v2
    def add_edge(self, v1, v2):
        """
        Adds an edge between vertex v1 and v2.
        Params
            v1: vertex index 1 (parent)
            v2: vertex index 2 (child)
        """

        # Add edges v1 <-> v2 to Adjacency list
        self.Adj[v1].append(v2)
        self.Adj[v2].append(v1)

        # Need to update number of children feature for parent and all ancestors
        # Number of children is feature at index 3
        ancestors = []
        dfs(self.Adj, ancestors, self.root, v1)

        for a in ancestors:
            self.F[a][3] += 1

    # Remove a vertex and all its children from the tree
    def delete_vertex(self, v):
        """
        v: the vertex id to delete
        """

        # First, find the node of question
        seq = []
        dfs(self.Adj, seq, self.root, v)

        if len(seq) == 0:
            # Node not found
            return

        # Recursively delete all children of this vertex
        children = self.Adj[v]
        for c in children:
            # For now, skip parent
            if c in seq:
                continue
            # Else, recursively delete nodes down the tree
            else:
                self.delete_vertex(c)

        # Get number of children of this node
        num_children = self.F[v][3] + 1

        # Update the num children feature of all ancestors
        for a in seq:
            if a == v:
                pass
            else:
                self.F[a][3] -= num_children

        # Update parents adjacency list to remove v
        if len(seq) > 1:
            self.Adj[seq[-2]].remove(v)

        # Post the 'delete node' event
        x_pos, y_pos = self.F[v][:2]
        true_pos = [x_pos + self.origin[0], y_pos+self.origin[1]]
        data = [hash(self), true_pos]
        events.post_event("DeleteNode", data)

        # Remove node from Adjacency list and feature list
        self.Adj.pop(v)
        self.F.pop(v)

    # Gather resources from the environment
    def gather(self):
        """
        For every node position, query the environment and collect the associated sunlight
        """
        for n, f in self.F.items():
            # n is node name
            # f is : [x, y, strength, num children, energy]
            x, y, strength = tuple(f[:3])
            sun = self.env.get_sun(x+self.origin[0], y+self.origin[1])

            # Update feature list
            strength = max(1, strength) # avoid zero division
            self.F[n][4] += sun / strength

    # Do the forward pass of the GNN
    def forward(self):
        """
        The tree is a graph, and its genetics are weight matrices.
        This effectively makes the Tree a GNN.
        This function applies a forward pass of this GNN over the tree.
        """
        # Convert the adjacency list into a numpy adjacency matrix
        self.A = convert_adj(self.Adj)

        # Add the identity to add self connections
        A = np.asarray(self.A)
        A = A + np.identity(A.shape[0])

        # Convert the feature matrix into a numpy array
        F = np.asarray(list(self.F.values()))

        # Pass through the MLPs. Matrix multiplication is associative.
        Y = np.matmul(A, np.matmul(F, self.W1))
        Z = np.matmul(A, np.matmul(F, self.W2))

        # Apply activation function
        Z = np.tanh(Z)

        # Return Z and Y
        return [Z, Y]

    # Perform action 'a' on vertex 'v', by factor of 'f'
    def execute(self, v, a, f):
        """
        Params:
            v: index of vertex.
            a: action id.
            f: Some actions require a factor. f is 'quantity' of change.
        """
        # Features: [x, y, strength, num children, energy]

        self.F[v][4] -= 0.25

        # Move position of node
        if 2 > a >= 0:
            # Change feature x,y by factor of f
            # Grab old node position (shifted by origin), then update it, and spend energy
            x_old, y_old = self.F[v][:2]

            # Update position
            if a == 0:
                x_old += round(f)
            else:
                y_old += round(f)

            # Grab new position, shifted by origin
            new_pos = [x_old, y_old]

            # Check if new position is available and in bounds
            if self._pos_available(new_pos):
                old_pos = [self.F[v][0] + self.origin[0], self.F[v][1] + self.origin[1]]
                new_pos = [x_old + self.origin[0], y_old + self.origin[1]]

                self.F[v][a] += round(f)

                events.post_event("MoveNode", [old_pos, new_pos])

        # Increase strength
        elif a == 2:
            # Increase strength by 1
            self.F[v][2] += 1

        # Grow a leaf
        elif a == 3:
            # Add a child to the node
            # The leafs position will be same as v_pos, but with y+1
            leaf_pos = [self.F[v][0], self.F[v][1] + 1]

            if self._pos_available(leaf_pos):
                # Add new node, add edge to parent, and finally update energy
                self.add_vertex(leaf_pos)
                self.add_edge(v, self.last_id)

                # Shift l_pos to be in environment grid space
                leaf_env_pos = [leaf_pos[0]+self.origin[0], leaf_pos[1]+self.origin[1]]
                events.post_event("NewNode", [hash(self), leaf_env_pos])

        # Produce a seed
        elif a == 4:
            x, y = self.F[v][:2]
            new_x = x + np.random.choice([-1, 1])
            self.produce_offspring(new_x, y)

        else:
            # Do nothing / Invalid
            self.F[4] += 0.5
            pass

    # Perform a simulation step; Gather resources, Forward pass GNN, Execute actions
    def step(self):
        """
        The tree can do a number of actions:
            - Grow a new leaf
            - Shift a node
            - Strengthen a leaf
            - ETC
        """
        # Gather resources from environment
        self.gather()

        # Do a forward pass of the GNN
        Z, Y = self.forward()
        V = len(self.Adj)

        # Every node makes a choice
        for v in range(V):
            # For the first vertex (the root), cannot shift x or y
            if v == 0:
                # Use the probabilistic distribution of this row to select an action (a)
                a = np.random.choice(self.e-2, p=softmax(Y[v, 2:]))
                a += 2

            else:
                # Use the probabilistic distribution of this row to select an action (a)
                a = np.random.choice(self.e, p=softmax(Y[v]))

            # Get the factor f, located at vertex v, action a, from the Z matrix
            f = Z[v, a]

            # Perform action (a) on vertex (v) in helper function, by factor f
            self.execute(v, a, f)

        # Increment age by 1
        self.age += 1

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

    # Create a seedling, with mutated genetics, at position (x,y)
    def produce_offspring(self, x, y):

        # Copy the weight matrices
        W1_copy = self.W1.copy()
        W2_copy = self.W2.copy()

        # Create two 'mutation' matrices
        W1_mutation = np.random.normal(0.0, 0.05, (self.d, self.e))
        W2_mutation = np.random.normal(0.0, 0.05, (self.d, self.e))

        # Combine the copied genes with their mutation matrices
        W1_new = W1_copy + W1_mutation
        W2_new = W2_copy + W2_mutation

        # post a new tree event, the environment will handle it
        events.post_event("NewOffspring", [x, y, W1_new, W2_new])

    # Return true if environment cell at 'pos' is empty, false otherwise
    def _pos_available(self, pos):
        return self.env.get_cell(pos[0]+self.origin[0], pos[1]+self.origin[1]) is None


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

# seq = []
# dfs(tree1.Adj, seq, 0, 3)
# print(seq)
# seq = []
# dfs(tree1.Adj, seq, 0, 2)
# print(seq)

# print(tree1.F)
# tree1.delete_vertex(3)
# print(tree1.Adj)
# print(tree1.F)

# tree2 = Tree(None, 0, 0)
#
# print(tree2.F)
# print(tree2.Adj)
# for i in range(20):
#     tree2.step()
# print(tree2.F)
# print(tree2.Adj)
