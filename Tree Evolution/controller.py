"""
Date: May 1st 2022
Author: Sam Johnston

A Controller Class.
The controller provides a user interface.
It handles the interaction(s) between the environment and the tree classes.
Handles overarching simulation variables and changes.

The controller will handle reproduction and mutation of new trees at the end of a simulation cycle.
Handles tree death if they die early.
"""

class Controller:

    def __init__(self):
        # The number of timesteps to do for a given population
        self.population_length = 100

        self.environments = list()

    def step(self, env):
        # Do a simulation step for a given environment
        pass

    def new_environment(self):
        # Create a new environment
        pass

    def remove_environment(self):
        # Delete an environment
        pass
