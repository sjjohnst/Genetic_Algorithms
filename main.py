import matplotlib.pyplot as plt
import numpy as np
from graph import Graph
from controller import Controller

# Parameters
mutation_rate = 0.1
n_vertices = 30
n_paths = 100
dx = 100
dy = 100
pause = 0.05

# Create objects
g = Graph(n_vertices, dx, dy)
c = Controller(n_paths, n_vertices, mutation_rate, g)

plt.ion()
fig = plt.figure(figsize=(0.1*dx, 0.05*dy))
ax = fig.add_subplot(121)
ax_score = fig.add_subplot(122)

running = True
total_iterations = 1
steps = 0
min_score = c.get_min_score()
min_scores = [min_score]

# Draw the plot
c.draw(ax)
ax.set_title(str(min_score))

# Draw scores over time
ax_score.plot(np.arange(total_iterations), min_scores)
ax_score.set_title("Minimum Distance over Time")

while running:

    plt.draw()

    # If running a set of steps do so. Otherwise ask for new command
    if steps > 0:
        steps = steps-1
        command = "step"
    else:
        command = input("Enter command: [stop/step/run]: ")

    # Commands
    if command.lower() == "stop":
        running = False

    elif command.lower() == "step":
        # Take a step, update min score
        c.step()
        total_iterations += 1
        min_score = c.get_min_score()
        min_scores.append(min_score)

        # update graph drawing
        ax.clear()
        c.draw(ax)
        ax.set_title(str(min_score))

        # Update metrics graph
        ax_score.clear()
        ax_score.plot(np.arange(total_iterations), min_scores)
        ax_score.set_title("Minimum Distance over Time")

        plt.pause(pause)

    elif command.lower() == "run":
        steps = int(input("How many iterations to run for?: "))

    else:
        print(f"Unrecognized command: '{command}'")
        continue
