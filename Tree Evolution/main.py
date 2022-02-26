from sprites import *

# Initialize pygame and create window
pygame.init()
pygame.display.set_caption("Treevolution")
clock = pygame.time.Clock()  # For syncing the FPS

# Full screen surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BGR)

# Simulation surface
simulation = pygame.Surface((SIM_WIDTH, SIM_HEIGHT))
simulation.fill(BGR)

# fittest tree surface
fittest = pygame.Surface((FIT_WIDTH, FIT_HEIGHT))
fittest.fill(BGR)

# ======================================================================================================
# SETUP THE BACKEND SIMULATION
env = Environment(SIM_WIDTH, SIM_HEIGHT, step=1)
gene = [(2, 100, HEIGHT), (0, 110, 780), (0, 95, 781)]
tree, _ = build_from_genes(gene)

trees = [TreeSprite(tree)]

gene_pool = []
num_trees = 2
for i in range(num_trees):
    new_gene = tree.mutate_genes()
    new_tree, _ = build_from_genes(new_gene)
    random_x = np.random.choice(np.arange(WIDTH))
    diff = random_x - tree.pos[0]
    new_tree.shift_x_positions(diff)
    trees.append(TreeSprite(new_tree))


def get_fittest_trees(trees):
    tree_list = []
    for stree in trees:
        sun = stree.calculate_sun(env.get_sun())
        tree_list.append((sun, stree))

    ordered_trees = sorted(tree_list, key=lambda x: x[0])[-(num_trees//2):]
    return [stree for _,stree in ordered_trees]


# ======================================================================================================
# SIMULATION LOOP
running = True
current_tree = None
run_sim = False

fittest_stree = get_fittest_trees(trees)
fittest_gene = fittest_stree[0].root.genes
fittest_tree, _ = build_from_genes(fittest_gene)
fittest_dest = (FIT_WIDTH//2, FIT_HEIGHT-20)
fittest_tree.shift_to_position(fittest_dest)

fittest_tree = TreeSprite(fittest_tree)

while running:

    # 1 Process input/events
    clock.tick(FPS)  # will make the loop run at the same speed all the time
    for event in pygame.event.get():  # gets all the events which have occured till now and keeps tab of them.
        # listening for the X button at the top
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                for stree in trees:
                    stree.shift_root(10)
            if event.key == pygame.K_LEFT:
                for stree in trees:
                    stree.shift_root(-10)

            # Take genetic step
            if event.key == pygame.K_SPACE:
                run_sim = not run_sim
                # print(len(trees))

    # Mutation loop
    if run_sim:
        fittest_trees = get_fittest_trees(trees)
        del trees
        trees = []

        for i, stree in enumerate(fittest_trees):

            if i == 0:
                # Fittest tree
                fittest_gene = stree.root.genes
                fittest_tree, _ = build_from_genes(fittest_gene)
                fittest_tree.shift_to_position(fittest_dest)

                fittest_tree = TreeSprite(fittest_tree)

            for j in range(2):
                new_gene = stree.root.mutate_genes()
                new_tree, _ = build_from_genes(new_gene)
                random_x = np.random.choice(np.arange(WIDTH))
                diff = random_x - stree.root.pos[0]
                new_tree.shift_x_positions(diff)

                trees.append(TreeSprite(new_tree))

    # 2 Update
    env.update_sun(trees)
    for stree in trees:
        stree.clear(simulation, screen)
        stree.update()

    # 3 Draw/render
    screen.fill(BGR)

    # Simulation surface
    pygame.surfarray.blit_array(simulation, env.get_sun_im())
    for stree in trees:
        stree.draw(simulation)

    # pygame.draw.rect(simulation, BLACK, (350,0,100,100))
    screen.blit(simulation, SIM_POS)

    # Fittest tree surface
    fittest_tree.clear(fittest, screen)
    fittest_tree.update()
    fittest.fill(WHITE)
    fittest_tree.draw(fittest)
    screen.blit(fittest, FIT_POS)

    # Done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()
