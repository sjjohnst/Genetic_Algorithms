import math
import random
import numpy as np
from parameters import *

"""
Tree data structure, defining node positions and mutation.
"""


def decision(prob):
    return random.random() < prob


def magnitude(pos1, pos2):
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)


def angle(pos1, pos2):
    return math.atan((pos1[1] - pos2[1]) / (pos1[0] - pos2[0] + 0.0000001))


class Tree:

    def __init__(self, position, strength=30):

        self.x, self.y = position
        self.strength = strength
        self.children = []

    def height(self):
        h = 1
        for child in self.children:
            h += child.height()
        return h

    def weight(self):
        w = self.strength / 10
        for child in self.children:
            w += child.weight()
        return w

    def pos(self):
        return (self.x, self.y)

    def add(self, pos):
        new_node = Tree(pos)
        self.children.append(new_node)

    def torque(self, child):
        this_pos = (self.x, self.y)
        child_pos = (child.x, child.y)
        weight = child.height()
        theta = angle(child_pos, this_pos)
        length = magnitude(child_pos, this_pos)
        torque = weight * length * math.cos(theta)
        return torque

    def break_branches(self):
        self.children[:] = [child for child in self.children if self.torque(child) <= self.strength]

    def mutate(self, depth, mutation_rates):
        """
        Mutate this specific node, using the 'mutation_rates' dictionary
            The depth of the node determines the likelihood of mutation,
            I.E. leaf nodes have the highest possible mutation rate, and root nodes have the lowest possible rate
        """
        # Mutation scalar, multiplies all other probabilities
        ms = depth / self.height()

        # First, mutate all children
        for child in self.children:
            child.mutate(depth+1, mutation_rates)

        # Now mutate this node
        pnn = ms * mutation_rates["p_new_node"]
        psx = ms * mutation_rates["p_shift_x"]
        psy = ms * mutation_rates["p_shift_y"]
        pis = ms * mutation_rates["p_up_strength"]

        if decision(pnn):
            # Add a child to this node
            new_x = np.random.normal(self.x, position_shift_x)
            new_y = np.random.normal(self.y, position_shift_y)
            if new_x < 0:
                new_x = 0
            elif new_x > SIM_WIDTH:
                new_x = SIM_WIDTH
            if new_y < 0:
                new_y = 0
            elif new_y > SIM_HEIGHT:
                new_y = SIM_HEIGHT
            new_pos = (new_x, new_y)
            self.add(new_pos)

        if decision(psx):
            self.x = np.random.normal(self.x, position_shift_x)
            if self.x < 0:
                self.x = 0
            elif self.x > SIM_WIDTH:
                self.x = SIM_WIDTH

        if decision(psy):
            self.y = np.random.normal(self.y, position_shift_x)
            if self.y < 0:
                self.y = 0
            elif self.y > SIM_HEIGHT:
                self.y = SIM_HEIGHT

        if decision(pis):
            self.strength = np.random.normal(self.strength, 10)
            if self.strength < 1:
                self.strength = 1

    def shift_x_positions(self, x):
        # update
        self.x = self.x + x
        # recurse
        for child in self.children:
            child.shift_x_positions(x)

    def shift_y_positions(self, y):
        # update
        self.y = self.y + y
        # recurse
        for child in self.children:
            child.shift_y_positions(y)

    def shift_to_position(self, dest):
        # Move the root to be at destination, update children accordingly
        diff_x = dest[0] - self.x
        diff_y = dest[1] - self.y
        self.shift_x_positions(diff_x)
        self.shift_y_positions(diff_y)
