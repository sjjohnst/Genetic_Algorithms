from environment import Environment
from view import EnvView
import pygame
from controller import Controller
from parameters import *

# Initialize pygame and the scree surface
pygame.init()
screen = pygame.display.set_mode(screen_size)
sim_surf = pygame.Surface(simulation_size)
clock = pygame.time.Clock()

FPS = 60
pygame.display.set_caption("Tree Evolution")

# Instantiate Environment
env = Environment(60, 60)

# Initialize population
env.init_population(10)

# Test environment
print("Pop size:", env.get_population())
print("Height: %d   Width: %d" % (env.height, env.width))
print("Cell (4,0): ", env.get_cell(4, 0))
print("Sun (2,5): ", env.get_sun(9, 5))

# Add a view
view = EnvView(600, 600, 11, env)

# Pygame code
running = True
pause = True
while running:

    # 1 Process input/events
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Blit the simulation surface onto the game window, then blit the controller.
    screen.blit(sim_surf, simulation_pos)
    view.display()
    screen.blit(view.surf, view.pos)

    pygame.display.flip()

