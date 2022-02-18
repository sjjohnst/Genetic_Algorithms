import pygame
import random
from parameters import *
from environment import *
from tree import *

# initialize pygame and create window
pygame.init()
pygame.mixer.init()  # For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treevolution")
clock = pygame.time.Clock()  # For syncing the FPS

# background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0,0,0))

# Define objects in the simulation
env = Environment(WIDTH, HEIGHT, step=1)
gene = [(3, 100, 800), (2, 95, 750), (0, 90, 700), (0, 105, 702), (1, 129, 770), (0, 140, 750), (0, 73, 765)]
tree, _ = build_from_genes(gene)
trees = [TreeSprite(tree)]

# Game loop
running = True
hit = False
leaf1hit = False
leaf1pos = (0, 0)
current_tree = None
while running:

    # 1 Process input/events
    clock.tick(FPS)  # will make the loop run at the same speed all the time
    for event in pygame.event.get():  # gets all the events which have occured till now and keeps tab of them.
        # listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_RIGHT:
        #         for tree in trees:
        #             tree.shift_root(10)
        #         leaf1pos = leaf1pos[0]+10, leaf1pos[1]
        #     if event.key == pygame.K_LEFT:
        #         for tree in trees:
        #             tree.shift_root(-10)
        #         leaf1pos = leaf1pos[0]-10, leaf1pos[1]
        #
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 1:
        #         for tree in trees:
        #             for s in tree.leaves:
        #                 hit = s.check_click(event.pos)
        #                 if hit:
        #                     leaf1pos = (s.x, s.y)
        #                     break
        #
        #             if hit:
        #                 current_tree = tree
        #                 break
        #
        #         # add a leaf
        #         if not hit:
        #             pos = pygame.mouse.get_pos()
        #             current_tree.insert(leaf1pos, pos)
        #             leaf1pos = pos
        #             break
        #
        #     if event.button == 3:
        #         pos = pygame.mouse.get_pos()
        #         pos = pos[0], HEIGHT
        #         tree = Tree(pos)
        #         trees.append(tree)
        #         leaf1pos = pos
        #         current_tree = tree

    # 2 Update
    env.update_sun(trees)
    for stree in trees:
        stree.clear(screen, background)
        stree.update()

    # 3 Draw/render
    screen.blit(background, (0,0))
    pygame.surfarray.blit_array(screen, env.get_sun_im())
    for stree in trees:
        stree.draw(screen)

    ############


    ############

    # Done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()
