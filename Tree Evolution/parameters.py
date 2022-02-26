
# Surface parameters
WIDTH = 800
HEIGHT = 400

SIM_WIDTH = 400
SIM_HEIGHT = 400
SIM_POS = (400, 0)

FPS = 30

# Define Colours
WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (33, 54, 18)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

# Background colour
BGR = (170, 170, 170)

# Tree parameters
snap_force = 100  # The force at which a branch will break (prevents over reaching structures)

# Mutation probabilities
p_new_node = 0.1  # The probability that genetic code adds a new node
p_swap_genes = 0.1  # The probability that two random genes get swapped
p_change_c = 0.1  # Probability that the c parameter in genetic code is increased/decreased
p_shift_x_pos = 0.2  # Probability of moving the x position in a gene
p_shift_y_pos = 0.2  # Probability of moving the y position in a gene

# Mutation shifts
position_shift_x = 5  # STD for normal distribution that shifts x / y values
position_shift_y = 10

