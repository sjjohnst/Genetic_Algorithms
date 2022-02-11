import pygame
from parameters import *
import math


# SPRITES
class Leaf(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()

        self.x, self.y = pos
        self.r = 5

        self.image = pygame.Surface([self.r*2, self.r*2])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        pygame.draw.circle(self.image, GREEN, (self.r, self.r), self.r)
        self.rect = self.image.get_rect()

    def check_click(self, pos):

        dx = pos[0] - self.x
        dy = pos[1] - self.y
        r = math.sqrt(dx**2 + dy**2)

        if r <= self.r:
            return True
        else:
            return False

    def update(self):
        self.rect.center = self.x, self.y


class Branch(pygame.sprite.Sprite):

    def __init__(self, pos1, pos2):
        super().__init__()

        width = pos2[0] - pos1[0]
        height = pos2[1] - pos1[1]
            self.image = pygame.Surface([abs(width), abs(height)])
        # self.image.fill(WHITE)
        # self.image.set_colorkey(WHITE)

        self.x1, self.y1 = pos1
        self.x2, self.y2 = pos2

        pygame.draw.line(self.image, BROWN, (0, height), (width, 0), width=2)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = self.x1, self.x2


# Tree Sprite Group
class Tree(pygame.sprite.Group):

    def __init__(self, root):
        super().__init__()

        self.root = root
        self.tree = Node(root)
        # Dictionary maps position to tree node
        self.pos_to_node = {root: self.tree}

        # Add sprite for first node
        leaf = Leaf(root)
        self.add(leaf)
        self.leaves = [leaf]
        self.branches = []

    def insert(self, pos1, pos2):
        # Use pos1 to access parent node, then add child
        parent = self.pos_to_node[pos1]
        self.pos_to_node[pos2] = parent.add(pos2)

        # Now add leaf, and branch
        lf = Leaf(pos2)
        self.leaves.append(lf)
        self.add(lf)

        br = Branch(parent.pos, pos2)
        self.branches.append(br)
        self.add(br)

    def shift_root(self, x):
        # Move the entire tree by x
        self.tree.shift_positions(x)
        self.pos_to_node = {(pos[0]+x, pos[1]): value for pos, value in self.pos_to_node.items()}
        for lf in self.leaves:
            lf.x += x
        for br in self.branches:
            br.x1 += x
            br.x2 += x


class Node:

    def __init__(self, position):

        self.pos = position
        self.children = []

    def add(self, pos):
        new_node = Node(pos)
        self.children.append(new_node)
        return new_node

    def shift_positions(self, x):
        # update
        self.pos = self.pos[0] + x, self.pos[1]
        # recurse
        for child in self.children:
            child.shift_positions(x)
