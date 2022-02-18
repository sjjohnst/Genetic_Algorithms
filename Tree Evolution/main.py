import pygame
import random
from parameters import *
from environment import *
from tree import *
from display import *

# initialize pygame and create window
pygame.init()
pygame.mixer.init()  # For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treevolution")
clock = pygame.time.Clock()  # For syncing the FPS

# background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0,0,0))

# Define objects in the simulation
env = Environment(WIDTH, HEIGHT, step=1)
gene = [(2, 100, HEIGHT-10), (0, 110, 780), (0, 95, 781)]
tree, _ = build_from_genes(gene)

trees = [TreeSprite(tree)]

gene_pool = []
num_trees = 200
for i in range(100):
    new_gene = tree.mutate_genes()
    new_tree, _ = build_from_genes(new_gene)
    random_x = np.random.choice(np.arange(WIDTH))
    diff = random_x - tree.pos[0]
    new_tree.shift_positions(diff)
    trees.append(TreeSprite(new_tree))


def get_fittest_trees(trees):
    tree_list = []
    for stree in trees:
        sun = stree.calculate_sun(env.get_sun())
        tree_list.append((sun, stree))

    ordered_trees = sorted(tree_list, key=lambda x: x[0])[-(num_trees//2):]
    return [stree for _,stree in ordered_trees]


# Game loop
running = True
hit = False
leaf1hit = False
leaf1pos = (0, 0)
current_tree = None
run_sim = False
while running:

    # 1 Process input/events
    clock.tick(FPS)  # will make the loop run at the same speed all the time
    for event in pygame.event.get():  # gets all the events which have occured till now and keeps tab of them.
        # listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                for stree in trees:
                    stree.shift_root(10)
                leaf1pos = leaf1pos[0]+10, leaf1pos[1]
            if event.key == pygame.K_LEFT:
                for stree in trees:
                    stree.shift_root(-10)
                leaf1pos = leaf1pos[0]-10, leaf1pos[1]

            # Take genetic step
            if event.key == pygame.K_SPACE:
                run_sim = not run_sim
                # print(len(trees))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(pygame.mouse.get_pos())
        #         for tree in trees:
        #             for s in tree.leaves:
        #                 hit = s.check_click(event.pos)
        #                 if hit:
        #                     leaf1pos = (s.x, s.y)
        #                     break
        #
        #             if hit:
        #                 current_tree = tree
        #                 break
        #
        #         # add a leaf
        #         if not hit:
        #             pos = pygame.mouse.get_pos()
        #             current_tree.insert(leaf1pos, pos)
        #             leaf1pos = pos
        #             break
        #
        #     if event.button == 3:
        #         pos = pygame.mouse.get_pos()
        #         pos = pos[0], HEIGHT
        #         tree = Tree(pos)
        #         trees.append(tree)
        #         leaf1pos = pos
        #         current_tree = tree

    if run_sim:
        fittest_trees = get_fittest_trees(trees)
        del trees
        trees = []

        for i, stree in enumerate(fittest_trees):
            for j in range(2):
                new_gene = stree.root.mutate_genes()
                new_tree, _ = build_from_genes(new_gene)
                random_x = np.random.choice(np.arange(WIDTH))
                diff = random_x - stree.root.pos[0]
                new_tree.shift_positions(diff)

                trees.append(TreeSprite(new_tree))

    # 2 Update
    env.update_sun(trees)
    for stree in trees:
        stree.clear(screen, background)
        stree.update()

    # 3 Draw/render
    screen.blit(background, (0, 0))
    pygame.surfarray.blit_array(screen, env.get_sun_im())
    for stree in trees:
        stree.draw(screen)

    ############


    ############

    # Done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()
