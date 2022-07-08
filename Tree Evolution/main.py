from environment import Environment
from view import EnvView
import pygame
from controller import Controller
from parameters import *

# Initialize pygame and the scree surface
pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

FPS = 60
pygame.display.set_caption("Tree Evolution")

# Instantiate Environment
env = Environment(60, 40)

# Initialize population
env.init_population(10)

# Test environment
print("Pop size:", env.get_population())
print("Height: %d   Width: %d" % (env.height, env.width))
print("Cell (4,0): ", env.get_cell(4, 0))
print("Sun (2,5): ", env.get_sun(9, 5))

# Instantiate the Environment view
# Params: env, surface position, width, height, cell_size
view = EnvView(env, env_size[0], env_size[1], 10)
view.display()

# Scroll variables for controlling view scrolling
scroll_x = 0
scroll_y = 0

# Pygame code
running = True
pause = True
while running:

    # 1 Process input/events
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_x = -3
            if event.key == pygame.K_RIGHT:
                scroll_x = 3
            if event.key == pygame.K_UP:
                scroll_y = -3
            if event.key == pygame.K_DOWN:
                scroll_y = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_x = 0
            if event.key == pygame.K_RIGHT:
                scroll_x = 0
            if event.key == pygame.K_UP:
                scroll_y = 0
            if event.key == pygame.K_DOWN:
                scroll_y = 0

    # Update the view offset
    view.scroll(scroll_x, scroll_y)

    # Blit the simulation surface onto the game window, then blit the controller.
    screen.blit(view.get_window(), env_pos)

    pygame.display.flip()

