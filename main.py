import matplotlib.pyplot as plt
import numpy as np
from graph import Graph
from controller import Controller

# Parameters
mutation_rate = 0.3
n_vertices = 20
n_paths = 50
dx = 40
dy = 40
pause = 0.01

# Create objects
g = Graph(n_vertices, dx, dy)
c = Controller(n_paths, n_vertices, mutation_rate, g)

plt.ion()
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(121)
ax_score = fig.add_subplot(122)

running = True
total_iterations = 1
steps = 0

# Draw the plot
c.draw(ax)

# Draw scores over time
min_score = c.get_min_score()
avg_score = c.get_avg_score()
min_scores = [min_score]
avg_scores = [avg_score]
ax_score.plot(np.arange(total_iterations), min_scores, color='blue', label='minimum')
ax_score.plot(np.arange(total_iterations), avg_scores, color='orange', label='average')
ax_score.legend()
ax_score.set_title("Minimum/Average Distance over Time")


while running:

    plt.pause(0.005)

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
        # Take a step
        c.step()
        total_iterations += 1

        # update graph drawing
        ax.clear()
        c.draw(ax)

        # Update metrics graph
        ax_score.clear()

        min_score = c.get_min_score()
        avg_score = c.get_avg_score()
        min_scores.append(min_score)
        avg_scores.append(avg_score)

        ax_score.plot(np.arange(total_iterations), min_scores, color='blue', label='minimum')
        ax_score.plot(np.arange(total_iterations), avg_scores, color='orange', label='average')
        ax_score.legend()
        ax_score.set_title("Minimum/Average Distance over Time")

    elif command.lower() == "run":
        steps = int(input("How many iterations to run for?: "))

    else:
        print(f"Unrecognized command: '{command}'")
        continue
