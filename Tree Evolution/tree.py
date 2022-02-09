import pygame
from parameters import *
import math


class Leaf(pygame.sprite.Sprite):

    def __init__(self, width, height, pos):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.x, self.y = pos
        self.r = 5

        pygame.draw.circle(self.image, GREEN, (self.x, self.y), self.r)

    def check_click(self, pos):

        dx = pos[0] - self.x
        dy = pos[1] - self.y
        r = math.sqrt(dx**2 + dy**2)

        if r <= self.r:
            return True
        else:
            return False


class Branch(pygame.sprite.Sprite):

    def __init__(self, width, height, pos1, pos2):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.x1, self.y1 = pos1
        self.x2, self.y2 = pos2

        pygame.draw.line(self.image, BLUE, (self.x1, self.y1), (self.x2, self.y2))


class Tree(pygame.sprite.Group):

    def __init__(self, root):
        super().__init__()

        # The location of the tree base
        self.root = root

        # Leaves
        leaf = Leaf(WIDTH, HEIGHT, root)
        self.add(leaf)
        self.leaves = [leaf]

    def add_leaf(self, sprite):
        self.add(sprite)
        self.leaves.append(sprite)
