import pygame
import random
from parameters import *

# initialize pygame and create window
pygame.init()
pygame.mixer.init()  # For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treevolution")
clock = pygame.time.Clock()  # For syncing the FPS

# Game loop
running = True
while running:

    # 1 Process input/events
    clock.tick(FPS)  # will make the loop run at the same speed all the time
    for event in pygame.event.get():  # gets all the events which have occured till now and keeps tab of them.
        # listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

    # 2 Update

    # 3 Draw/render
    screen.fill(BLACK)

    ############


    ############

    # Done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()
