import numpy as np
import math


class Path:
    """
    A path is a sequence of vertices, representing a walk on a graph.
    Each vertex is seen exactly once, so these paths are loops.
    """
    def __init__(self, no_vertices, graph, path=None):

        # Store parameters
        self.no_vertices = no_vertices

        # Define the path
        if path is None:
            # Use graph to get the vertices
            path = list(range(no_vertices))
            # Shuffle the list of vertices to get a random path
            np.random.shuffle(path)
            self.path = list(path)
        else:
            self.path = path

        # Create a list of vertex pairs (edges)
        shifted_path = self.path.copy()
        shifted_path.append(shifted_path.pop(0))
        self.edges = list(zip(self.path, shifted_path))

        self.score = 0
        for (a, b) in self.edges:
            self.score += graph.distance(a, b)
