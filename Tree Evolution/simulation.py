from parameters import *
from tree import Tree

"""
File describes the driver class Simulation, which runs the backend of the Tree evolution program
"""


class Simulation:

    def __init__(self, N):

        self.mutation_rates = dict()
        # Mutation probabilities
        self.mutation_rates["p_new_node"] = 0.01     # The probability that genetic code adds a new node
        self.mutation_rates["p_shift_x"] = 0.08  # Probability of moving the x position in a gene
        self.mutation_rates["p_shift_y"] = 0.08  # Probability of moving the y position in a gene

        # Tree storage. Initialize all trees as a single leaf node
        self.trees = [Tree((0, 0)) for i in range(N)]

        # Metrics
        self.average_depth = 0    # The average depth (in nodes) of the trees
        self.median_depth = 0     # The median depth (in nodes) of the trees
        self.average_fitness = 0
        self.median_fitness = 0

    def step(self):
        # perform one simulation step
        pass

    def reset(self):
        # Reset all progress
        pass

    def get_metrics(self):
        # Return stored metrics
        pass
