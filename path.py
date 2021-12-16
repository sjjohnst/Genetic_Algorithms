import numpy as np
import math

class Path:
    """
    A path is a sequence of vertices, representing a walk on a graph.
    Each vertex is seen exactly once, so these paths are loops.
    """
    def __init__(self, no_vertices, mutation_rate, path=None):

        # Store parameters
        self.no_vertices = no_vertices
        self.mutation_rate = mutation_rate

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

    def score(self, graph):
        """ Calculate the total distance of this path, on graph """
        score = 0

        for (a, b) in self.edges:
            score += graph.distance(a, b)

        return score

    def __add__(self, mate):
        """ Breed two Paths """

        # Retrieve a random slice of the path from parent 1 (self)
        start_ind = np.random.randint(len(self.path))
        slice_length = np.random.randint(low=2, high=len(self.path)-1)

        # Retrieve this path section
        path_section = []
        j = 0
        for i in range(slice_length):
            if start_ind + j >= len(self.path):
                j = -start_ind
            path_section.append(self.path[start_ind+j])
            j = j + 1

        # Now we need to fill in the rest of the path from the mate
        # Iterate over the mate's path, and add each vertex we encounter not already in new path
        for vertex in mate.path:
            if vertex in path_section:
                pass
            else:
                path_section.append(vertex)

        # Finally, mutate the path using mutation rate probability
        mutate = np.random.choice([False, True], p=[1-self.mutation_rate, self.mutation_rate])
        assert(len(self.path) == len(path_section)), print(len(path_section))
        if mutate:
            # select two indices randomly
            indices = np.random.choice(len(self.path), 2)

            # Swap the items at selected indices
            try:
                path_section[indices[0]], path_section[indices[1]] = path_section[indices[1]], path_section[indices[0]]
            except:
                print(indices)

        # Finally, create a new path object and return
        child = Path(self.no_vertices, self.mutation_rate, path=path_section)
        return child
