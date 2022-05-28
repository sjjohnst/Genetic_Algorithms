# from tree import Tree
from environment import Environment
import pygame
from controller import Controller
from parameters import *

pygame.init()
screen = pygame.display.set_mode(screen_size)
sim_surf = pygame.Surface(simulation_size)
clock = pygame.time.Clock()

pygame.display.set_caption("Tree Evolution")

FPS = 60

controller = Controller()
environment = Environment(100, 60, "env1")

environment.zoom = 1
#
# test_tree = environment.add_tree()
# test_tree.add_vertex(0, [10, 3])
# test_tree.add_vertex(1, [15, 6])
# test_tree.add_vertex(3, [12, 0])
#
# test_tree.add_edge(3, 1)
# test_tree.add_edge(3, 0)

environment.init_population(10)

scroll_x = 0
scroll_y = 0
zoom = 0

controller.update()
environment.update()

running = True
while running:

    # 1 Process input/events
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                scroll_x = -2
            if event.key == pygame.K_LEFT:
                scroll_x = 2
            if event.key == pygame.K_UP:
                scroll_y = 2
            if event.key == pygame.K_DOWN:
                scroll_y = -2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                scroll_x = 0
            if event.key == pygame.K_LEFT:
                scroll_x = 0
            if event.key == pygame.K_UP:
                scroll_y = 0
            if event.key == pygame.K_DOWN:
                scroll_y = 0

    # environment.offset += scroll
    # environment.zoom = max(environment.zoom + zoom, 0)

    # Handle scrolling around the simulation window
    environment.scroll(scroll_x, scroll_y)

    # Blit the environment onto the simulation surface
    sim_surf.blit(environment.surf, environment.pos)

    # Blit the simulation surface onto the game window, then blit the controller.
    screen.blit(sim_surf, simulation_pos)
    screen.blit(controller.surf, controller_pos)

    pygame.display.flip()

