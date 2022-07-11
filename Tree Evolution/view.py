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

        # Parameters
        self.cell_size = 20
        self.keyboard_speed = 5

        # Attach the model object, and then have the model attach a reference to this view
        self.env = env
        self.env.attach(self)

        # Surfaces
        self.display_surface = display_surface
        self.env_surface = pygame.Surface((env.width*self.cell_size, env.height*self.cell_size))
        self.env_rect = self.env_surface.get_rect(topleft=(0, 0))

        # Camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # Zoom
        self.zoom_scale = 1.0
        self.internal_surf_size = (2400, 1600)
        self.internal_surf = pygame.Surface(self.internal_surf_size)
        self.internal_surf_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
        self.internal_surf_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

        self.min_zoom = max(2*self.half_w/self.env_rect.width, 2*self.half_h/self.env_rect.height)

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

    # Keeps offset within defined boundaries
    def constrain_offset(self):
        # Get offset as position relative to center screen, after scaling
        x_pos = (self.offset.x - self.half_w) * self.zoom_scale
        y_pos = (self.offset.y - self.half_h) * self.zoom_scale

        # Get the height and width of the environment surface after scaling
        scaled_width = self.env_rect.width * self.zoom_scale
        scaled_height = self.env_rect.height * self.zoom_scale

        # pass
        if x_pos > -self.half_w:
            x_pos = -self.half_w
        elif x_pos + scaled_width < self.half_w:
            x_pos = self.half_w - scaled_width
        if y_pos > -self.half_h:
            y_pos = -self.half_h
        elif y_pos + scaled_height < self.half_h:
            y_pos = self.half_h - scaled_height

        self.offset.x = (x_pos / self.zoom_scale) + self.half_w
        self.offset.y = (y_pos / self.zoom_scale) + self.half_h

    # Updates zoom using keyboard input
    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom_scale -= 0.1
        if keys[pygame.K_e]:
            self.zoom_scale += 0.1

        self.zoom_scale = max(self.min_zoom, self.zoom_scale)
        # self.zoom_scale = min(1.25, self.zoom_scale)

    # Blit surface to display
    def draw(self):
        self.keyboard_control()
        self.zoom_keyboard_control()

        self.constrain_offset()

        self.display_surface.fill(BLUE)
        self.internal_surf.fill(BROWN)

        env_offset = self.internal_offset + self.offset
        self.internal_surf.blit(self.env_surface, env_offset)

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_size_vector*self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)

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
        pygame.draw.rect(self.env_surface, rbg, pygame.Rect(x, y, self.cell_size, self.cell_size))

        # Adds a blue border to the cells
        pygame.draw.rect(self.env_surface, BLUE, pygame.Rect(x, y, self.cell_size, self.cell_size), 1)

