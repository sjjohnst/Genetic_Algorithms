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
from parameters import *
import pygame


class Controller:

    def __init__(self):
        # Create the pygame surface for this Controller
        self.surf = pygame.Surface(controller_size)

        # The number of timesteps to do for a given population
        self.population_length = 100

        # The controller holds a dictionary of environments. Maps env name to its instance
        self.environments = dict()

    def update(self):
        # Base controller is filled black
        self.surf.fill(GREEN)

        # Add a rectangle within the surface to give illusion of black border
        pygame.draw.rect(self.surf, GREY, (5, 5, controller_size[0]-10, controller_size[1]-10))

    def run(self):
        """
        Driver function of the controller.
        Main loop:
            1. Query User Input
            2. Process Input, Do Associated Action
            3. Repeat or Exit
        """

        is_running = True
        while is_running:
            command = input("Enter Command")
            try:
                self._process_command(command)
            except CommandError as cerr:
                print("An error occurred with the provided command:")
                print("    \"" + cerr + "\"")

    def _query_user(self):
        pass

    def _process_command(self, command):
        pass

    def new_environment(self, name):
        if name in self.environments.keys():
            # Break if name is invalid
            print("Name provided is already associated with an environment.")

            return None

        else:
            # Create the new environment and add to the dictionary
            new_env = Environment(name)
            self.environments[name] = new_env

            return new_env

    def remove_environment(self, name):
        if name in self.environments.keys():
            # Delete the environment
            del self.environments[name]
        else:
            # Can't find the environment
            print("Could not find an environment associated with the provided name.")

    def plot_environment(self, name):
        if name in self.environments.keys():
            self.environments[name].update_plot()
        else:
            print("Could not find an environment associated with the provided name.")

    def step(self, env):
        # Do a simulation step for a given environment
        pass


class CommandError(Exception):
    """
    Custom exception class for user command request related errors
    """
    # Define an attribute, a set of available command names
    commands = {
        "step",
        "new_env",
        "del_env",
        "help"
    }

    def __init__(self, cmd, *args):
        super().__init__(args)
        self.cmd = cmd

    def __str__(self):
        return f'The command {self.cmd} is not recognized.'
