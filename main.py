import matplotlib.pyplot as plt
import time
from graph import Graph
from controller import Controller

# Parameters
mutation_rate = 0.1
n_vertices = 10
n_paths = 10
dx = 100
dy = 100
pause = 0.1

# Create objects
g = Graph(n_vertices, dx, dy)
c = Controller(n_paths, n_vertices, mutation_rate, g)

plt.ion()
fig, ax = plt.subplots(figsize=(0.05*dx, 0.05*dy))

running = True
total_iterations = 0
steps = 0

while running:

    # Draw the plot
    c.draw(ax)
    plt.draw()
    plt.pause(pause)

    # If running a set of steps do so. Otherwise ask for new command
    if steps > 0:
        steps = steps-1
        command = "step"
    else:
        command = input("Enter command: [stop/step/run]: ")

    ## Commands
    if command.lower() == "stop":
        running = False

    elif command.lower() == "step":
        c.step()
        ax.clear()
        total_iterations += 1

    elif command.lower() == "run":
        steps = int(input("How many iterations to run for?: "))

    else:
        print(f"Unrecognized command: '{command}'")
        continue
