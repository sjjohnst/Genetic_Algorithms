import numpy as np
from graph import Graph
from path import Path


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

    def draw(self, ax, color='black'):
        """ Draw the graph, and overlay the paths """

        alpha = (1.0 / self.no_paths) # if a particular edge is common in all paths, it will show up as alpha 1.0

        # First, plot all the paths edges
        for path in self.path_list:
            self.graph.draw_path(ax, path, alpha, color)

        # Overlay the vertices of the graph on top
        self.graph.draw(ax)
