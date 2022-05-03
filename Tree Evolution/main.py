from tree import Tree
import matplotlib.pyplot as plt

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,10))

tree1 = Tree()
tree1.add_vertex(1, [1,3])
tree1.add_vertex(2, [2,4])
tree1.add_vertex(3, [1,2])
tree1.add_vertex(4, [4,1])
tree1.add_vertex(5, [3,3])
tree1.add_edge(1,2)
tree1.add_edge(1,3)
tree1.add_edge(4,5)
tree1.add_edge(3,4)

tree1.plot(ax)
plt.show()