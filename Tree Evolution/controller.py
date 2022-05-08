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
from environment import Environment


class Controller:

    def __init__(self):
        # The number of timesteps to do for a given population
        self.population_length = 100

        # The controller holds a dictionary of environments. Maps env name to its instance
        self.environments = dict()

    def new_environment(self, name):
        # Break if name is invalid
        if name in self.environments.keys():
            print("Name provided is already associated with an environment.")
        # Create the new environment and add to the dictionary
        else:
            new_env = Environment()
            self.environments[name] = new_env

    def remove_environment(self, name):
        # Delete the environment
        if name in self.environments.keys():
            del self.environments[name]
        # Can't find the environment
        else:
            print("Could not find an environment associated with the provided name.")

    def step(self, env):
        # Do a simulation step for a given environment
        pass
