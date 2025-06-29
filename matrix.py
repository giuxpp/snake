import random

# === Position Calculation Functions ===
def generate_block_position(forbidden):
    """Generate a new random position for a block aligned to the grid"""
    cols = 800 // 30  # WIDTH // SIDE
    rows = 600 // 30  # HEIGHT // SIDE

    # Create a list of all valid grid positions
    all_positions = []
    for x in range(cols):
        for y in range(rows):
            pos = (x * 30, y * 30)  # SIDE
            if pos not in forbidden:
                all_positions.append(pos)

    if not all_positions:
        return None

    return random.choice(all_positions)

def get_random_empty_cell(snake_positions=None, block_positions=None):
    """Get a random empty cell that's not occupied by snake or blocks"""
    forbidden = set()
    if snake_positions:
        forbidden.update(snake_positions)
    if block_positions:
        forbidden.update(block_positions)
    return generate_block_position(forbidden)
