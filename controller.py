import numpy as np
from graph import Graph
from path import Path
from itertools import combinations


class Controller:

    def __init__(self, no_paths, no_vertices, mutation_rate, graph):

        # Store parameters
        self.no_paths = no_paths
        self.no_vertices = no_vertices
        self.mu_rate = mutation_rate
        self.graph = graph

        # Create a set of paths for this graph, sort on their distance
        self.path_list = [Path(no_vertices, mutation_rate) for i in range(no_paths)]
        self.path_list.sort(key=lambda x: x.score(self.graph))
        self.score_list = [path.score(graph) for path in self.path_list]

    def draw(self, ax, color='black'):
        """ Draw the graph, and overlay the paths """

        alpha = (1.0 / self.no_paths) # if a particular edge is common in all paths, it will show up as alpha 1.0

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
        breeding_pairs = np.random.choice(survivors, size=(len(survivors)//2, 2), replace=False)
        children = []

        # For each of the pairs, create two children and append to chil list
        for (p1, p2) in breeding_pairs:
            p3 = p1 + p2
            p4 = p2 + p1
            children.append(p3)
            children.append(p4)

        # If this does not replace all killed paths, breed some more
        diff = self.no_paths - (len(survivors) + len(children))
        while diff > 0:
            last_pair = np.random.choice(survivors, size=2, replace=False)
            last_child = last_pair[0] + last_pair[1]
            children.append(last_child)
            diff = diff - 1

        # Finally, concatenate the children with parents
        self.path_list = np.ndarray.tolist(np.concatenate([survivors, children]))
        self.path_list.sort(key=lambda x: x.score(self.graph))
        self.score_list = [path.score(self.graph) for path in self.path_list]

    def get_min_score(self):
        return min(self.score_list)