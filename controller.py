import numpy as np
from graph import Graph
from path import Path


class Controller:

    def __init__(self, no_paths: int, no_vertices: int, mutation_rate: float, graph: Graph):

        # Store parameters
        self.no_paths = no_paths
        self.no_vertices = no_vertices
        self.mu_rate = mutation_rate
        self.graph = graph

        # Create a set of paths for this graph, sort on their distance
        self.path_list = [Path(no_vertices, self.graph) for i in range(no_paths)]
        self.path_list.sort(key=lambda x: x.score)
        self.score_list = [path.score for path in self.path_list]

    def get_min_score(self):
        return min(self.score_list)

    def get_avg_score(self):
        return np.average(self.score_list)

    def draw(self, ax, color='black'):
        """ Draw the graph, and overlay the paths """

        # If a particular edge is common in all paths, it will show up as alpha 1.0
        alpha = (1.0 / self.no_paths)

        # First, plot all the paths edges
        for path in self.path_list:
            self.graph.draw_path(ax, path, alpha, color)

        # Overlay the vertices of the graph on top
        self.graph.draw(ax)

    def step(self):
        """ Kill half of the population, and breed the remaining """

        # Kill off half the population. The lower ones score, the higher the probability of survival
        # probabilities = 1 / (np.array(self.score_list) * np.sum(1 / np.array(self.score_list)))
        # survivors = np.random.choice(self.path_list, size=int(self.no_paths*0.5), p=probabilities)
        survivors = self.path_list[:-int(self.no_paths*0.5)]

        # Randomly select breeding pairs from the survivors
        # In real world genetics, fitness is also related to reproductive success,
        # but here we only consider survival in 'life'
        breeding_pairs_1 = np.random.choice(survivors, size=(len(survivors)//2, 2), replace=False)
        breeding_pairs_2 = np.random.choice(survivors, size=(len(survivors) // 2, 2), replace=False)
        children = []

        # For each of the pairs, create a child and append to child list
        for (p1, p2) in breeding_pairs_1:
            p3 = self.breed(p1, p2)
            children.append(p3)
        for (p1, p2) in breeding_pairs_2:
            p3 = self.breed(p1, p2)
            children.append(p3)

        # If this does not replace all killed paths, breed some more
        diff = self.no_paths - (len(survivors) + len(children))
        while diff > 0:
            [p1, p2] = np.random.choice(survivors, size=2, replace=False)
            last_child = self.breed(p1, p2)
            children.append(last_child)
            diff = diff - 1

        # Finally, concatenate the children with parents
        self.path_list = list(np.concatenate([survivors, children]))
        self.path_list.sort(key=lambda x: x.score)
        self.score_list = [path.score for path in self.path_list]

    def breed(self, p1, p2):
        """ Breed two Paths """

        # Retrieve a random slice of the path from parent 1 (self)
        start_ind = np.random.randint(self.no_vertices)
        slice_length = np.random.randint(low=int(self.no_vertices*0.2), high=int(self.no_vertices*0.8))

        # Retrieve this path section from p1
        path_section = []
        j = 0
        for i in range(slice_length):
            if start_ind + j >= self.no_vertices:
                j = -start_ind
            path_section.append(p1.path[start_ind+j])
            j = j + 1

        # Now we need to fill in the rest of the path from the mate
        # Iterate over the mate's path, and add each vertex we encounter not already in new path
        for vertex in p2.path:
            if vertex in path_section:
                pass
            else:
                path_section.append(vertex)

        assert (self.no_vertices == len(path_section)), print(len(path_section))

        # Finally, mutate the path using mutation rate probability
        mutate = np.random.choice([False, True], p=[1-self.mu_rate, self.mu_rate])
        if mutate:
            # select two indices randomly
            indices = np.random.choice(self.no_vertices, 2)

            # Swap the items at selected indices
            path_section[indices[0]], path_section[indices[1]] = path_section[indices[1]], path_section[indices[0]]

        # Finally, create a new path object and return
        child = Path(self.no_vertices, self.graph, path=path_section)
        return child
