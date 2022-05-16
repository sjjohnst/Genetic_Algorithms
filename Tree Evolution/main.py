# from tree import Tree
# from environment import Environment
from controller import Controller
import matplotlib.pyplot as plt

plt.ion()

controller = Controller()

env = controller.new_environment("ENV")

tree1 = env.add_tree()
tree1.add_vertex(1, [1,3])
tree1.add_vertex(2, [2,4])
tree1.add_vertex(3, [1,2])
tree1.add_vertex(4, [4,1])
tree1.add_vertex(5, [3,3])
tree1.add_edge(1,2)
tree1.add_edge(1,3)
tree1.add_edge(4,5)
tree1.add_edge(3,4)

controller.plot_environment("ENV")
plt.pause(1.0)

tree2 = env.add_tree()
tree2.add_vertex(1, [4,1.5])
tree2.add_vertex(2, [2,3.4])
tree2.add_vertex(3, [1.2,1.5])
tree2.add_vertex(4, [4.1,1])
tree2.add_vertex(5, [1.2,2.6])
tree2.add_edge(1,3)
tree2.add_edge(1,5)
tree2.add_edge(2,5)
tree2.add_edge(3,4)

controller.plot_environment("ENV")
plt.pause(1.0)

env2 = controller.new_environment("ENV2")

tree3 = tree1 = env2.add_tree()
tree1.add_vertex(1, [1,3])
tree1.add_vertex(2, [2,4])
tree1.add_vertex(3, [1,2])
tree1.add_vertex(4, [4,1])
tree1.add_vertex(5, [3,3])
tree1.add_edge(1,2)
tree1.add_edge(1,3)
tree1.add_edge(4,5)
tree1.add_edge(3,4)

controller.plot_environment("ENV2")
plt.pause(1.0)

