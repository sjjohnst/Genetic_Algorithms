from environment import Environment
from view import EnvView, CntrView
import pygame
from controller import Controller
from parameters import *
import events

# Initialize pygame and the scree surface
pygame.init()

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

pygame.display.set_caption("Tree Evolution")

FPS = 60
# time between each step of the simulation, in milliseconds
minimum_wait_time = 500

# Instantiate Environment
env = Environment(75, 30)

# Initialize population
env.init_population(20)

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

controller_surface = pygame.Surface(controller_size)
cntr_view = CntrView(controller_surface)
cntr_view.draw()

# Pygame code
running = True
pause = True

last_step_time = pygame.time.get_ticks()

while running:

    # Process input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
            if event.key == pygame.K_RETURN:
                env.step()
            if event.key == pygame.K_r:
                events.post_event("Reset", None)
                pause = True

    clock.tick(60)
    # print(clock.get_fps())

    view.update()
    cntr_view.update()
    screen.blit(env_surface, env_pos)
    screen.blit(controller_surface, controller_pos)

    current_time = pygame.time.get_ticks()
    if current_time - last_step_time > minimum_wait_time and not pause:
        env.step()
        last_step_time = pygame.time.get_ticks()

    pygame.display.update()

