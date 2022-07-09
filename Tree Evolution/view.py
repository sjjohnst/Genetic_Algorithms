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

    def __init__(self, env, display_surface):
        """
        Params
            env: The environment model instance to observe
            display_surface: the pygame surface on which to blit this environment view
        """

        self.cell_size = 20
        self.keyboard_speed = 5

        # Display attributes
        self.display_surface = display_surface
        self.internal_surface = pygame.Surface((env.width*self.cell_size, env.height*self.cell_size))

        # Camera offset
        self.offset = pygame.math.Vector2()
        self.offset.y = self.display_surface.get_size()[1] - self.internal_surface.get_size()[1]
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # Attach the model object, and then have the model attach a reference to this view
        self.env = env
        self.env.attach(self)

    # Receive notification of event from observed
    def notify(self, event):
        # Handle event(s)
        pass

    # Updates offset using keyboard input
    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.offset.x += self.keyboard_speed
        if keys[pygame.K_RIGHT]: self.offset.x -= self.keyboard_speed
        if keys[pygame.K_UP]: self.offset.y += self.keyboard_speed
        if keys[pygame.K_DOWN]: self.offset.y -= self.keyboard_speed

    def constrain_offset(self):

        display_width = self.display_surface.get_size()[0]
        display_height = self.display_surface.get_size()[1]

        intern_width = self.internal_surface.get_size()[0]
        intern_height = self.internal_surface.get_size()[1]

        if self.offset.x > 0:
            self.offset.x = 0
        elif self.offset.x < display_width - intern_width:
            self.offset.x = display_width - intern_width

        if self.offset.y < display_height - intern_height:
            self.offset.y = display_height - intern_height
        elif self.offset.y > 0:
            self.offset.y = 0

        if intern_width < display_width:
            self.offset.x = (display_width - intern_width) // 2

        if intern_height < display_height:
            self.offset.y = (display_height - intern_height) // 2

    # Blit surface to display
    def draw(self):
        self.keyboard_control()
        self.constrain_offset()
        self.display_surface.fill(BROWN)
        self.display_surface.blit(self.internal_surface, self.offset)

    # Blit everything to the surface
    def update(self):
        # For each cell of the environment, blit a rectangle representing its value(s)
        for y in range(self.env.height):
            for x in range(self.env.width):

                # No leaf at (x,y)
                if self.env.get_cell(x, y) is None:
                    # Plot sunlight
                    value = self.env.sun[y, x]
                    rgb = (value * 255, value*255, value*255)

                # There is a leaf at (x,y)
                else:
                    rgb = GREEN

                self.blit_cell([x, y], rgb)

    # Base function to blit a cell at pos, with rbg value provided
    def blit_cell(self, pos, rbg):
        # Convert the cell position to pixel position
        x = pos[0] * self.cell_size
        y = (self.env.height - 1 - pos[1]) * self.cell_size

        # Blit the rbg as square
        pygame.draw.rect(self.internal_surface, rbg, pygame.Rect(x, y, self.cell_size, self.cell_size))

        # Adds a blue border to the cells
        pygame.draw.rect(self.internal_surface, BLUE, pygame.Rect(x, y, self.cell_size, self.cell_size), 1)

