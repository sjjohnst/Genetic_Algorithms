import pygame
from parameters import *
from tree import *
from environment import *
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

        # Swap position 1 and 2 such that we only need to check two cases later on fro drawing the branch
        if pos1[0] > pos2[0]:
            temp = pos1
            pos1 = pos2
            pos2 = temp

        self.x1, self.y1 = pos1
        self.x2, self.y2 = pos2

        # Calculate the width and height of bounding box
        width = abs(self.x2 - self.x1)
        height = abs(self.y2 - self.y1)

        # Different cases for line drawing
        if width == 0:
            # Edge case where width is 0, place line in middle
            # print("zero width")
            width = 10
            pos1 = (width/2, 0)
            pos2 = (width/2, height)

        elif height == 0:
            # Edge case where height is 0, place line in middle
            height = 10
            pos1 = (0, height/2)
            pos2 = (width, height/2)

        else:
            # Two other cases, line goes from one corner to another

            # Line goes top left to bottom right
            if pos1[1] < pos2[1]:
                pos1 = (0,0)
                pos2 = (width,height)
            # Line goes bottom left to top right
            else:
                pos1 = (0, height)
                pos2 = (width, 0)

        # Create rectangle and add a line
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.line(self.image, BROWN, pos1, pos2, width=3)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = (self.x1 + self.x2) / 2.0, (self.y1 + self.y2) / 2.0


# Tree Sprite Group: Takes a physical tree structure and turns into sprite for pygame display
class TreeSprite(pygame.sprite.Group):

    def __init__(self, root: Tree):
        super().__init__()

        self.root = root
        self.leaves = []
        self.branches = []

        self.__build_from_tree(self.root)

    def calculate_sun(self, env_grid):
        sun, X, Y = env_grid

        energy_gathered = 0
        for s in self.leaves:
            min_x = s.x - s.r
            max_x = s.x + s.r
            x_idx_min = find_nearest(X, min_x)
            x_idx_max = find_nearest(X, max_x)

            min_y = s.y - s.r
            max_y = s.y + s.r
            y_idx_min = find_nearest(Y, min_y)
            y_idx_max = find_nearest(Y, max_y)

            # Decrease sunlight everywhere below the array index found
            energy_gathered += np.sum(sun[x_idx_min:x_idx_max, y_idx_min:y_idx_max])
        return energy_gathered

    def __build_from_tree(self, node: Tree):
        # Recursive function to add in leaf and branch sprites
        # Input: a node of the Tree structure

        # Add a leaf for this node
        lf = Leaf(node.pos)
        self.leaves.append(lf)
        self.add(lf)

        # Add a branch to every child
        for child in node.children:
            br = Branch(node.pos, child.pos)
            self.branches.append(br)
            self.add(br)
            self.__build_from_tree(child)

    def shift_root(self, x):
        # Move the entire tree by x
        self.root.shift_positions(x)
        for lf in self.leaves:
            lf.x += x
        for br in self.branches:
            br.x1 += x
            br.x2 += x
