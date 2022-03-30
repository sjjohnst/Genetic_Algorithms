import pygame
from parameters import *

# Initialize pygame and create window
pygame.init()
pygame.display.set_caption("Treevolution")
clock = pygame.time.Clock()  # For syncing the FPS

# Full screen surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BGR)

# ======================================================================================================
# SIMULATION LOOP
running = True

while running:

    # 1 Process input/events
    clock.tick(FPS)  # will make the loop run at the same speed all the time
    for event in pygame.event.get():  # gets all the events which have occured till now and keeps tab of them.
        # listening for the X button at the top
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
