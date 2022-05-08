from tree import Tree
from environment import Environment
import matplotlib.pyplot as plt

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))

env = Environment()

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

env.plot(ax)
plt.show()