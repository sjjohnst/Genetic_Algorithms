"""
Date: June 28th 2022
Author: Sam Johnston

Viewport class
The viewport maps the data of the model (environment) onto the screen.
"""
import numpy as np
import pygame

from parameters import *


class CntrView:

    def __init__(self, height, width, controller):
        """
        Params
            height: The number of pixels in height
            width: The number of pixels in width
            controller: The controller instance to observe
        """

        self.height = height
        self.width = width
        self.controller = controller


class EnvView:

    def __init__(self, height, width, cell_size, env):
        """
        Params
            height: The number of pixels in height
            width: The number of pixels in width
            cell_size: The size in pixels of an environment cells
            env: The environment model instance to observe
        """

        # Display attributes
        self.height = height
        self.width = width
        self.cell_size = cell_size

        # Attach the model object, and then have the model attach a reference to this view
        self.env = env
        self.env.attach(self)

        # Plotting variables
        self.surf = pygame.Surface((width, height))

        # Where to blit the surface within the simulation window. Default is (0,0)
        self.pos = (0, 0)

    def notify(self, event):
        """
        Receive a notification of event from model or controller
        """
        ## Handle event(s)
        pass

    def display(self):
        # Base colour is white
        self.surf.fill(WHITE)

        # Use getter to retrieve data from environment model
        # Nodes: list of numpy arrays, each of shape (N,2)
        # Edges: list of Adjacency lists
        sunlight, nodes, edges = self.env.get_state()

        # For each cell, pad out to be the size of a cell
        sunlight_pixels = np.repeat(np.repeat(sunlight, self.cell_size, axis=0), self.cell_size, axis=1)
        pygame.surfarray.blit_array(self.surf, sunlight_pixels)

        # Plot grid lines over all
        # Vertical bars
        for i in range(0, self.env.width):
            pygame.draw.rect(self.surf, BLACK_A, (i * self.cell_size, 0, 1, self.env.height * self.cell_size))

        # Horizontal bars
        for i in range(0, self.env.height):
            pygame.draw.rect(self.surf, BLACK_A, (0, i * self.cell_size, self.env.width * self.cell_size, 1))

        # Plot all the nodes
        # Condense the list of arrays into one large array
        for coord in np.asarray(nodes):
            x = coord[0]
            y = self.env.height - coord[1] - 1
            pygame.draw.rect(self.surf, GREEN, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

        # Plot all the edges
        # For each Adjacency list
        for t, Adj in enumerate(edges):
            seen = []

            # Plot all edges contained in the adjacency list
            for v1, n in enumerate(Adj):
                point1 = (nodes[t][v1] + 0.5) * self.cell_size
                x1 = point1[0]
                y1 = self.env.height * self.cell_size - point1[1]

                for v2 in n:
                    # Pass if duplicate edge
                    if {v1, v2} in seen:
                        pass

                    # Plot the edge
                    point2 = (nodes[t][v2] + 0.5) * self.cell_size
                    x2 = point2[0]
                    y2 = self.env.height * self.cell_size - point2[1]
                    pygame.draw.line(self.surf, BROWN, (x1, y1), (x2, y2), 5)

                    # Add to seen list
                    seen.append({v1, v2})
