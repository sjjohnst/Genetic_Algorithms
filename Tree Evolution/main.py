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

# Define objects in the simulation
env = Environment(WIDTH, HEIGHT, step=1)
tree = Tree((100, HEIGHT-10 ))

# Game loop
running = True
while running:

    # 1 Process input/events
    clock.tick(FPS)  # will make the loop run at the same speed all the time
    for event in pygame.event.get():  # gets all the events which have occured till now and keeps tab of them.
        # listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONUP:
            if leaf1hit:
                for s in tree.leaves:
                    hit = s.check_click(event.pos)
                    if hit:
                        print("Hit")
                        leaf1hit = False
                        leaf2pos = (s.x, s.y)
                        b = Branch(WIDTH, HEIGHT, leaf1pos, leaf2pos)
                        tree.add(b)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            leaf1hit = False
            for s in tree.leaves:
                hit = s.check_click(event.pos)
                if hit:
                    print("Hit")
                    leaf1hit = True
                    leaf1pos = (s.x, s.y)
                    break

            # add a leaf
            if not hit:
                pos = pygame.mouse.get_pos()
                leaf = Leaf(WIDTH, HEIGHT, pos)
                tree.add_leaf(leaf)



    # 2 Update

    # 3 Draw/render
    pygame.surfarray.blit_array(screen, env.get_sun_im())
    tree.draw(screen)

    ############


    ############

    # Done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()
