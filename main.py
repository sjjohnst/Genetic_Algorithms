import matplotlib.pyplot as plt
import time
from Graph import Graph
from path import Path

mutation_rate = 0.3
no_vertices = 15
dx = 100
dy = 100

g = Graph(no_vertices, dx, dy)
n_paths = 5
paths = [Path(no_vertices, mutation_rate) for i in range(n_paths)]

fig, ax = plt.subplots(figsize=(0.05*dx, 0.05*dy))
g.draw(ax)
# for p in paths:
#     g.draw_path(ax, p, n_paths)
g.draw_path(ax, paths[0], n_paths)
g.draw_path(ax, paths[1], n_paths)
child = paths[0] + paths[1]

g.draw_path(ax, child, n_paths, color='blue')

plt.show()
