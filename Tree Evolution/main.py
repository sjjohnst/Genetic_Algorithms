from sprites import *
import copy

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

N = 100
mutation_rates = {
    "p_new_node": 0.0002,
    "p_shift_x": 0.008,
    "p_shift_y": 0.008
}

trees = []
for i in range(N):
    x = np.random.uniform(0, SIM_WIDTH)
    new_tree = Tree((x, HEIGHT))
    trees.append(TreeSprite(new_tree))


def get_fittest_trees(tree_list):
    ordered_trees = sorted(tree_list, key=lambda tree: tree.calculate_sun(env.get_sun()))
    return ordered_trees[-len(tree_list)//2:]


# ======================================================================================================
# SIMULATION LOOP
running = True
current_tree = None
run_sim = False

fittest_tree = copy.deepcopy(get_fittest_trees(trees)[0].root)
desired_fittest_pos = (FIT_WIDTH//2, FIT_HEIGHT)
fittest_tree.shift_to_position(desired_fittest_pos)
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
        trees[:] = []

        for i, stree in enumerate(fittest_trees):

            if i == 0:
                # Fittest tree
                fittest_tree = copy.deepcopy(stree.root)
                fittest_tree.shift_to_position(desired_fittest_pos)
                fittest_tree = TreeSprite(fittest_tree)

            for j in range(2):
                x = np.random.uniform(0, SIM_WIDTH)
                new_tree = copy.deepcopy(stree.root)
                new_tree.shift_to_position((x, HEIGHT))
                new_tree.mutate(1, mutation_rates)
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
