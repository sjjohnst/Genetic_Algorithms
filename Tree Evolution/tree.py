

class Tree:

    def __init__(self, position, genes):

        self.pos = position
        self.genes = genes
        self.children = []

    def add(self, pos):
        new_node = Tree(pos)
        self.children.append(new_node)
        return new_node

    def shift_positions(self, x):
        # update
        self.pos = self.pos[0] + x, self.pos[1]
        # recurse
        for child in self.children:
            child.shift_positions(x)

    def get_weight(self):
        weight = 1
        for child in self.children:
            weight += child.get_weight()
        return weight


def build_from_genes(genes):
    # Genes is a list of tuples: (c, x ,y)
    # where c = number of children, and (x,y) is position of that node

    c, x, y = genes[0]
    root = Tree((x, y), genes)

    # Recurse for each child
    sub_children_seen = 0  # Helps keep track of skipping tuples in the array
    for i in range(c):
        idx = i + 1 + sub_children_seen
        if idx >= len(genes):
            # Run out of children, exit
            break
        child, sub_children = build_from_genes(genes[idx:])
        root.children.append(child)
        sub_children_seen += sub_children

    sub_children_seen += c
    return root, sub_children_seen

