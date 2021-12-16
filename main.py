import matplotlib.pyplot as plt
import time
from graph import Graph
from controller import Controller

mutation_rate = 0.3
n_vertices = 30
n_paths = 10
dx = 100
dy = 100

g = Graph(n_vertices, dx, dy)
c = Controller(n_paths, n_vertices, mutation_rate, g)

fig, ax = plt.subplots(figsize=(0.05*dx, 0.05*dy))

c.draw(ax)

plt.show()
