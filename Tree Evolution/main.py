# from tree import Tree
from environment import Environment
import pygame
from controller import Controller
from parameters import *

pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

pygame.display.set_caption("Tree Evolution")

FPS = 60

controller = Controller()
environment = Environment(simulation_size[0], simulation_size[1], "env1")

test_tree = environment.add_tree()
test_tree.add_vertex(0, [10, 30])
test_tree.add_vertex(1, [15, 33])
test_tree.add_vertex(3, [12, int(simulation_size[1]/cell_size)-1])

test_tree.add_edge(3, 1)
test_tree.add_edge(3, 0)

running = True
while running:

    # 1 Process input/events
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    controller.update()
    environment.update()
    screen.blit(controller.surf, controller_pos)
    screen.blit(environment.surf, simulation_pos)

    pygame.display.flip()

