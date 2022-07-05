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

    def __init__(self, width, height, cell_size, env):
        """
        Params
            width: The number of pixels in width
            height: The number of pixels in height
            cell_size: The size in pixels of an environment cell
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

    # Receive notification of event from observed
    def notify(self, event):
        # Handle event(s)
        pass

    # Blit everything to the surface
    def display(self):
        # Base colour is white
        self.surf.fill(BLACK)

        # Retrieve data from the environment
        sun = self.env.sun
        cells = self.env.env

        # For each cell of the environment, blit a rectangle representing its value(s)
        for y in range(self.env.height):
            for x in range(self.env.width):

                # No leaf at (x,y)
                if self.env.get_cell(x, y) is None:
                    # Plot sunlight
                    value = sun[y, x]
                    rgb = (value * 255, value*255, value*255)

                # There is a leaf at (x,y)
                else:
                    rgb = GREEN

                self.blit_cell([x, y], rgb)

    # Base function to blit a cell at pos, with rbg value provided
    def blit_cell(self, pos, rbg):
        # Convert the cell position to pixel position
        x = pos[0] * self.cell_size
        y = self.height - self.cell_size - pos[1] * self.cell_size

        # Blit the rbg as square
        pygame.draw.rect(self.surf, rbg, pygame.Rect(x, y, self.cell_size, self.cell_size))

        # Adds a blue border to the cells
        pygame.draw.rect(self.surf, BLUE, pygame.Rect(x, y, self.cell_size, self.cell_size), 1)
