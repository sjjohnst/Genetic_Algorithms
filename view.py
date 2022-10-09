"""
Date: June 28th 2022
Author: Sam Johnston

Viewport class
The viewport maps the data of the model (environment) onto the screen.
"""
import pygame
from parameters import *
import events


# Fonts
pygame.font.init()
font1 = pygame.font.SysFont('chalkduster.ttf', 20)


class CntrView:

    def __init__(self, surface):
        """
        Params
            surface: The surface to display to
        """

        # Surfaces
        self.display_surface = surface
        self.width, self.height = self.display_surface.get_size()
        self.cntr_surf = pygame.Surface((self.width, self.height))
        self.cntr_rect = self.display_surface.get_rect(topleft=(0, 0))

        # Events
        events.subscribe("SimulationStep", self.update_stats)
        events.subscribe("Reset", self.reset)

        # PERMANENT TEXT
        # Simulation step
        self.step_text = font1.render('Simulation Step:', True, BLACK)
        self.step_text_rect = self.step_text.get_rect()
        self.step_text_rect.topleft = (10, (self.height*1.5 - self.step_text_rect.height)//2)

        # Population Size
        self.pop_text = font1.render('Population Size:', True, BLACK)
        self.pop_text_rect = self.pop_text.get_rect()
        self.pop_text_rect.topleft = (10, (self.height*1.25 - self.step_text_rect.height)//2)

    # Reset to have time and population both 0
    def reset(self, data):
        self.update_stats([0, 0])

    # Blit the controller surface onto the display
    def update(self):
        self.display_surface.blit(self.cntr_surf, self.cntr_rect)

    # Blit everything to the controller surface
    def draw(self):
        # Fill grey
        self.cntr_surf.fill(GREY)

        # Add Border to controller
        pygame.draw.rect(self.cntr_surf, (5, 125, 110), pygame.Rect(0, 0, self.width, self.height), 5)

        # Add border in center of the controller to separate Stats from buttons
        pygame.draw.line(self.cntr_surf, (5, 125, 110), (0, self.height//2), (self.width, self.height//2), 4)

        # Display text(s)
        self.cntr_surf.blit(self.step_text, self.step_text_rect)
        self.cntr_surf.blit(self.pop_text, self.pop_text_rect)

    # Update all the statistics displayed on the controller
    def update_stats(self, data):
        """
        data: [current step, no. organisms]
        """

        curr_step, num_orgs = data

        # Render simulation step
        step_number = font1.render(str(curr_step)+"   ", True, BLACK)
        step_num_rect = step_number.get_rect()
        step_num_rect.topleft = (self.step_text_rect.width+20, (self.height*1.5 - self.step_text_rect.height)//2)

        # Render population size
        pop_size = font1.render(str(num_orgs)+"   ", True, BLACK)
        pop_size_rect = pop_size.get_rect()
        pop_size_rect.topleft = (self.pop_text_rect.width+20, (self.height*1.25 - self.pop_text_rect.height)//2)

        # Cover old text, then draw the new text to the screen.
        pygame.draw.rect(self.cntr_surf, GREY, step_num_rect)
        self.cntr_surf.blit(step_number, step_num_rect)

        pygame.draw.rect(self.cntr_surf, GREY, pop_size_rect)
        self.cntr_surf.blit(pop_size, pop_size_rect)


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

        # Subscribe to events
        events.subscribe("CellUpdates", self.update_cells)
        events.subscribe("Reset", self.draw)
        events.subscribe("NewOffspring", self.new_seed)
        events.subscribe("SeedUpdates", self.update_seeds)

        # Attach the model object, and then have the model attach a reference to this view
        self.env = env

        # Surfaces
        self.display_surface = display_surface
        self.env_surface = pygame.Surface((env.width*self.cell_size, env.height*self.cell_size))
        self.env_rect = self.env_surface.get_rect(topleft=(0, 0))

        # Camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # position at bottom left corner
        self.offset.y = 2*self.half_h - self.env_rect.height

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
    def update(self):
        self.keyboard_control()
        self.zoom_keyboard_control()

        self.constrain_offset()

        self.display_surface.fill(BLUE)
        self.internal_surf.fill(BROWN)

        env_offset = self.internal_offset + self.offset
        self.internal_surf.blit(self.env_surface, env_offset)

        self.draw_branches(env_offset)

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_size_vector*self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)

    # Blit all branches (graph edges) to env_surface
    def draw_branches(self, offset):
        # First, retrieve all edges from the environment
        # Edges is a dictionary, mapping tree key to set of edges
        edges = self.env.get_edges()

        # Iterate over all edges
        for pos1, pos2 in edges.items():
            x1, y1 = pos1
            x2, y2 = pos2

            x1 = self.cell_size * (x1 + 0.5) + offset.x
            y1 = (self.env.height - 0.5 - y1) * self.cell_size + offset.y

            x2 = self.cell_size * (x2 + 0.5) + offset.x
            y2 = (self.env.height - 0.5 - y2) * self.cell_size + offset.y

            pygame.draw.line(self.internal_surf, BROWN, (x1, y1), (x2, y2), width=2)

    # Blit everything to the surface
    def draw(self):
        # For each cell of the environment, blit a rectangle representing its value(s)
        for y in range(self.env.height):
            for x in range(self.env.width):

                # No leaf at (x,y)
                if self.env.get_cell(x, y) is None:
                    # Plot sunlight
                    value = self.env.get_sun(x, y)
                    rgb = (value * 255 / 2, value*255 / 2, value*255 / 2)

                # There is a leaf at (x,y)
                else:
                    rgb = GREEN

                self.blit_cell([x, y], rgb)

        # Draw all branches (edges of the trees)
        # self.draw_branches()

    # Handle single cell updates. Called when 'CellUpdates' event is pushed
    def update_cells(self, data: dict):
        """
        data: dictionary of mappings from old_cell -> new_cell to look at and update on display
        """
        for old_pos, new_pos in data.items():

            # Extract information
            old_x, old_y = old_pos
            old_cell = self.env.get_cell(old_x, old_y)

            # Only covert the old cell with sunlight if no leaf is here
            if old_cell is None:
                # print("Covert old cell", old_pos)
                # Get sunlight value at old cell
                value = self.env.get_sun(old_x, old_y)
                sun_rgb = (value * 255 / 2, value * 255 / 2, value * 255 / 2)

                # Now blit sun onto old cell, and leaf (GREEN) onto new cell
                # print("Blit sun: ", old_pos)
                self.blit_cell(old_pos, sun_rgb)

            # Fill the new cell with node, if node there
            if new_pos is not None:
                # print("Blit leaf: ", new_pos)
                self.blit_cell(new_pos, GREEN)

    # Handle single cell updates. Called when 'CellSeeds' event is pushed
    def update_seeds(self, data: dict):
        """
        data: dictionary of mappings from old_cell -> new_cell to look at and update on display
        """
        for old_pos, new_pos in data.items():

            # Extract information
            old_x, old_y = old_pos
            old_cell = self.env.get_cell(old_x, old_y)

            # Only covert the old cell with sunlight if no leaf is here
            if old_cell is None:
                # print("Covert old cell", old_pos)
                # Get sunlight value at old cell
                value = self.env.get_sun(old_x, old_y)
                sun_rgb = (value * 255 / 2, value * 255 / 2, value * 255 / 2)

                # Now blit sun onto old cell, and leaf (GREEN) onto new cell
                # print("Blit sun: ", old_pos)
                self.blit_cell(old_pos, sun_rgb)

            else:
                self.blit_cell(old_pos, GREEN)

            # Now at new_pos, blit the seed
            self.blit_cell(new_pos, SEED_BROWN)

    # Base function to blit a cell at pos, with rbg value provided
    def blit_cell(self, pos, rbg):
        # Convert the cell position to pixel position
        x = pos[0] * self.cell_size
        y = (self.env.height - 1 - pos[1]) * self.cell_size

        # Blit the rbg as square
        pygame.draw.rect(self.env_surface, rbg, pygame.Rect(x, y, self.cell_size, self.cell_size))

        # Adds a blue border to the cells
        pygame.draw.rect(self.env_surface, BLUE, pygame.Rect(x, y, self.cell_size, self.cell_size), 1)

    # For when a new seedling is produced
    def new_seed(self, data):
        """
        data: [x, y, W1, W2]
        """
        pos = data[:2]
        self.blit_cell(pos, BROWN)
