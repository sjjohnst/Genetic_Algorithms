import math
import random
import numpy as np
from parameters import *


def decision(prob):
    return random.random() < prob


def magnitude(pos1, pos2):
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)


def angle(pos1, pos2):
    return math.atan((pos1[1] - pos2[1]) / (pos1[0] - pos2[0]))


class Tree:

    def __init__(self, position, genes):

        self.pos = position
        self.genes = genes
        self.children = []
        self.sunlight = 0

    def add(self, pos):
        new_node = Tree(pos)
        self.children.append(new_node)
        return new_node

    def shift_positions(self, x):
        # update
        self.pos = self.pos[0] + x, self.pos[1]
        # recurse
        for child in self.children:
            child.shift_positions(x)

    def get_weight(self):
        weight = 1
        for child in self.children:
            weight += child.get_weight()
        return weight

    def mutate_genes(self):
        # Take genetic code, mutate, return new genetic code
        new_genes = self.genes.copy()

        for i, gene in enumerate(new_genes):
            c, x, y = gene

            change_c = decision(p_change_c)
            change_x = decision(p_shift_x_pos)
            change_y = decision(p_shift_y_pos)
            swap_genes = decision(p_swap_genes)

            if i == 0:
                # Root gene, only make variations to c
                if change_c:
                    if random.random() < 0.7:
                        c += 1
                    else:
                        c -= 1

            else:
                if change_c:
                    if random.random() < 0.7:
                        c += 1
                    else:
                        c -= 1

                if change_x:
                    x += np.random.normal(0, position_shift_x)
                if change_y:
                    y += random.uniform(0, position_shift_y)

                if swap_genes:
                    j = np.random.choice(len(new_genes))
                    new_genes[i], new_genes[j] = new_genes[j], new_genes[i]
                    i = j
                    c, x, y = new_genes[j]

            if c < 0:
                c = 0
            if x < 0:
                x = 0
            elif x > WIDTH:
                x = WIDTH
            if y < 0:
                y = 0
            elif y > HEIGHT:
                y = HEIGHT

            new_genes[i] = (c, x, y)

        add_node = decision(p_new_node)

        if add_node:
            new_x = np.random.normal(x,2.0)
            new_y = np.random.normal(y,2.0)
            c = 0
            new_genes.append((c,new_x,new_y))

        return new_genes


def build_from_genes(genes):
    # Genes is a list of tuples: (c, x ,y)
    # where c = number of children, and (x,y) is position of that node

    c, x, y = genes[0]
    this_pos = (x, y)
    root = Tree(this_pos, genes)

    # Recurse for each child
    sub_children_seen = 0  # Helps keep track of skipping tuples in the array
    for i in range(c):
        idx = i + 1 + sub_children_seen
        if idx >= len(genes):
            # Run out of children, exit
            break
        child, sub_children = build_from_genes(genes[idx:])
        sub_children_seen += sub_children

        # Check for branch breakage
        weight = child.get_weight()
        r = magnitude(this_pos, child.pos)
        theta = angle(this_pos, child.pos)
        force = weight * r * math.cos(theta)
        # print(r, theta, force)
        # if force > snap_force:
        #     # branch can't support its children, skip
        #     continue

        # Otherwise, valid child, add
        root.children.append(child)

    sub_children_seen += c
    return root, sub_children_seen
