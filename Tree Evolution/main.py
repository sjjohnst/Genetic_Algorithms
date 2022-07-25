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
env = Environment(30, 50)

# Initialize population
env.init_population(5)

# Test environment
# print("Pop size:", env.get_population())
# print("Height: %d   Width: %d" % (env.height, env.width))
# print("Cell (4,0): ", env.get_cell(4, 0))
# print("Sun (2,5): ", env.get_sun(9, 5))

# Instantiate the Environment view
# Params: env, surface
env_surface = pygame.Surface(env_size)
view = EnvView(env, env_surface)
view.draw()

# Pygame code
running = True
pause = True
while running:

    # Process input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause

    clock.tick(60)
    # print(clock.get_fps())

    view.update()
    screen.blit(env_surface, env_pos)

    if not pause:
        env.step()

    pygame.display.update()

