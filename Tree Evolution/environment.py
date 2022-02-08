"""
A discrete grid of cells, which represents the environment organisms will grow and live within
"""
import numpy as np
import matplotlib.pyplot as plt


class Environment:

    def __init__(self, height, width, step):

        self.height = height
        self.width = width

        X = np.arange(0, self.width, step, dtype='float32')
        Y = np.arange(0, self.height, step, dtype='float32')
        self.X, self.Y = np.meshgrid(X, Y)
        self.grid = np.stack([self.X, self.Y], axis=-1)

        # initial sunlight is a gradient from top of environment to bottom
        self.sunlight = np.ones_like(self.X)
        alpha = np.log(2) / self.sunlight.shape[0]
        for i, row in enumerate(self.sunlight):
            if i == 0:
                continue
            self.sunlight[i] = self.sunlight[i] * np.exp(-alpha*i)

    def get_grid(self):
        return np.copy(self.grid)

    def plot_sun(self):
        plt.imshow(self.sunlight)
        plt.colorbar()
        plt.show()
