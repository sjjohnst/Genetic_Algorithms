"""
A discrete grid of cells, which represents the environment organisms will grow and live within
"""
import numpy as np
import matplotlib.pyplot as plt


class Environment:

    def __init__(self, height, width, step):

        self.height = height
        self.width = width

        X = np.arange(0, self.width,  step, dtype='float32')
        Y = np.arange(0, self.height, step, dtype='float32')
        self.X, self.Y = np.meshgrid(X, Y)
        self.grid = np.stack([self.X, self.Y], axis=-1)

        # Initial sunlight is a gradient from top of environment to bottom
        self.sunlight = np.ones_like(self.X)
        alpha = np.log(4) / self.sunlight.shape[0]
        for i in range(self.sunlight.shape[1]):
            if i == 0:
                continue
            self.sunlight[:, i] = self.sunlight[:, i] * np.exp(-alpha*i)

        # Parameters for plotting onto pygame surface

    def get_grid(self):
        return np.copy(self.grid)

    def get_sun_im(self):
        sun_im = np.expand_dims(np.copy(self.sunlight), axis=-1).repeat(3, axis=-1) * 255
        return sun_im

    def plot_sun(self):
        plt.imshow(self.sunlight)
        plt.colorbar()
        plt.show()
