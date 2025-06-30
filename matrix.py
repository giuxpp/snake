import random

# === Position Calculation Functions ===
def generate_block_position(forbidden):
    """
    Generate a new random position for a block aligned to the grid.

    This function generates a random position for a block in a grid
    where the block's position does not overlap with any of the forbidden
    positions provided. The grid is defined by the constants WIDTH and HEIGHT,
    and the block's position is aligned to this grid.

    Parameters:
    - forbidden (set): A set of positions that are forbidden for the new block.
      These are typically the positions currently occupied by other blocks or the snake.

    Returns:
    - tuple: A tuple (x, y) representing the new position of the block, or None
      if no valid position can be found.
    """
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
    """
    Get a random empty cell that's not occupied by snake or blocks.

    This function determines a random position in the grid that is not currently
    occupied by the snake or any blocks. It does this by generating a block position
    with the set of forbidden positions being the union of the snake's positions and
    the blocks' positions.

    Parameters:
    - snake_positions (list): A list of positions occupied by the snake. Default is None.
    - block_positions (list): A list of positions occupied by blocks. Default is None.

    Returns:
    - tuple: A tuple (x, y) representing a random empty cell in the grid, or None
      if no empty cell can be found.
    """
    forbidden = set()
    if snake_positions:
        forbidden.update(snake_positions)
    if block_positions:
        forbidden.update(block_positions)
    return generate_block_position(forbidden)
