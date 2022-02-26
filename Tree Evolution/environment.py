"""
A discrete grid of cells, which represents the environment organisms will grow and live within
"""
import numpy as np
import matplotlib.pyplot as plt


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array-value)).argmin()
    return idx


class Environment:

    def __init__(self, height, width, step):

        self.height = height
        self.width = width
        self.step = step

        self.X = np.arange(0, self.width,  step, dtype='float32')
        self.Y = np.arange(0, self.height, step, dtype='float32')
        X, Y = np.meshgrid(self.X, self.Y)
        self.grid = np.stack([X, Y], axis=-1)

        # Use uniform initial sunlight
        self.sunlight = np.ones_like(X)

        # Initial sunlight is a gradient from top of environment to bottom
        self.sunlight = self.reset_sunlight()

    def reset_sunlight(self):
        sunlight = np.ones_like(self.sunlight)
        alpha = np.log(4) / sunlight.shape[0]
        for i in range(sunlight.shape[1]):
            if i == 0:
                continue
            sunlight[:, i] = sunlight[:, i] * np.exp(-alpha * i)
        return sunlight

    def get_grid(self):
        return np.copy(self.grid)

    def get_sun(self):
        return self.sunlight, self.X, self.Y

    def update_sun(self, trees):
        # Take a Tree (pygame sprite group), and calculate shadows
        self.sunlight = self.reset_sunlight()
        for tree in trees:
            for s in tree.leaves:
                min_x = s.x - s.r
                max_x = s.x + s.r
                x_idx_min = find_nearest(self.X, min_x)
                x_idx_max = find_nearest(self.X, max_x)
                y_idx = find_nearest(self.Y, s.y)

                # Decrease sunlight everywhere below the array index found
                self.sunlight[x_idx_min:x_idx_max, y_idx+1:] = self.sunlight[x_idx_min:x_idx_max, y_idx+1:] * 0.90

    def get_sun_im(self):
        # For plotting the greyscale background
        sun_im = np.expand_dims(np.copy(self.sunlight), axis=-1).repeat(3, axis=-1) * 200
        return sun_im

    def plot_sun(self):
        plt.imshow(self.sunlight)
        plt.colorbar()
        plt.show()
