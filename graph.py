import numpy as np
import math
import matplotlib.pyplot as plt
from path import Path

class Graph:
    """
    Graph class for python.

    A graph is a collection of edges and vertices.
    For the TSP, we want a graph to encode all possible paths, i.e. graphs should contain all possible edges.
    Edges must also have associated weights (to represent distance).
    A graph is passed the dimensions of the board, x_width, y_height, which define where vertices can exist.
    All vertices will be assigned a random (unique) location on this space.
    """

    def __init__(self, no_vertices, x_width, y_height):

        # Store parameters
        self.no_vertices = no_vertices
        self.x_width = x_width
        self.y_height = y_height

        # Name all the vertices, assign each a position
        self.vertex_ids = list(range(no_vertices))

        # Get a random x,y for each vertex
        x_pos = np.random.choice(x_width, no_vertices, replace=False)
        y_pos = np.random.choice(y_height, no_vertices, replace=False)
        self.vertex_positions = [(x, y) for x, y in zip(x_pos, y_pos)]

        # Create dictionary mapping vertex ids to their position
        self.vertices = dict(zip(self.vertex_ids, self.vertex_positions))

    def distance(self, a: int, b: int):
        """ Calculate distance between two vertices, a,b """

        x_a, y_a = self.vertices[a]
        x_b, y_b = self.vertices[b]

        x_diff = x_a - x_b
        y_diff = y_a - y_b

        distance = math.sqrt(x_diff**2 + y_diff**2)
        return distance

    def draw(self, ax):
        """ Draw the graph onto a matplotlib axis """

        r = np.mean(0.01*np.array([self.x_width, self.y_height]))

        # Define the size of the axis, with some padding (for vertices on the edges)
        ax.set_xlim(-r, self.x_width+r)
        ax.set_ylim(-r, self.y_height+r)

        for coord in self.vertices.values():
            cc = plt.Circle(coord, radius=r)
            ax.add_artist(cc)

    def draw_path(self, ax, p: Path, a_scale, color='black'):
        """ Draw the path onto graph """

        for (a, b) in p.edges:
            a_coord = self.vertices[a]
            b_coord = self.vertices[b]

            x = [a_coord[0], b_coord[0]]
            y = [a_coord[1], b_coord[1]]

            ax.plot(x, y, color=color, alpha=(1.0/a_scale))
