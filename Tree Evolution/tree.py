import pygame
from parameters import *
import math


# SPRITES
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

        pygame.draw.line(self.image, BROWN, (self.x1, self.y1), (self.x2, self.y2), width = 2)


# Tree Sprite Group
class Tree(pygame.sprite.Group):

    def __init__(self, root):
        super().__init__()

        self.root = root
        self.tree = Node(root)
        # Dictionary maps position to tree node
        self.pos_to_node = {root: self.tree}

        # Add sprite for first node
        leaf = Leaf(WIDTH, HEIGHT, root)
        self.add(leaf)
        self.leaves = [leaf]
        self.branches = []

    def insert(self, pos1, pos2):
        # Use pos1 to access parent node, then add child
        parent = self.pos_to_node[pos1]
        self.pos_to_node[pos2] = parent.add(pos2)

        # Now add leaf, and branch
        lf = Leaf(WIDTH, HEIGHT, pos2)
        self.leaves.append(lf)
        self.add(lf)

        br = Branch(WIDTH, HEIGHT, parent.pos, pos2)
        self.branches.append(br)
        self.add(br)


class Node:

    def __init__(self, position):

        self.pos = position
        self.children = []

    def add(self, pos):
        new_node = Node(pos)
        self.children.append(new_node)
        return new_node
