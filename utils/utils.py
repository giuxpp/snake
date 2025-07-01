import random
import pygame  # Import pygame for key constants
import time

# Global variable to track the game start time
game_start_time = None


# Utility functions

def lerp(start, end, t):
    """
    Linear interpolation between start and end points.

    Args:
        start (tuple): Starting point (x, y).
        end (tuple): Ending point (x, y).
        t (float): Interpolation factor (0 <= t <= 1).

    Returns:
        tuple: Interpolated point (x, y).
    """
    x1, y1 = start
    x2, y2 = end
    return (
        x1 + (x2 - x1) * t,
        y1 + (y2 - y1) * t
    )

def get_segment_position(current, target, frame, total_frames):
    """
    Get interpolated position for a snake segment.

    Args:
        current (tuple): Current position of the segment (x, y).
        target (tuple): Target position of the segment (x, y).
        frame (int): Current frame number.
        total_frames (int): Total number of frames for the movement.

    Returns:
        tuple: Interpolated position (x, y).
    """
    MOVE_RESOLUTION = 0.25

    if frame >= total_frames:
        return target
    t = frame / total_frames
    t = max(0.0, min(1.0, t))  # Clamp between 0 and 1
    # Use cubic easing for smoother start/stop
    t = t * t * (3 - 2 * t)

    # Adjust interpolation to move half the pixels
    adjusted_target = (
        current[0] + (target[0] - current[0]) * MOVE_RESOLUTION,
        current[1] + (target[1] - current[1]) * MOVE_RESOLUTION
    )

    return lerp(current, adjusted_target, t)

def generate_block_position(forbidden, width, height, side):
    """
    Generate a new random position for a block aligned to the grid.

    Args:
        forbidden (set): Set of positions that cannot be used.
        width (int): Width of the game area.
        height (int): Height of the game area.
        side (int): Size of each grid cell.

    Returns:
        tuple: Random position (x, y) or None if no valid positions are available.
    """
    cols = width // side
    rows = height // side

    # Create a list of all valid grid positions
    all_positions = []
    for x in range(cols):
        for y in range(rows):
            pos = (x * side, y * side)
            if pos not in forbidden:
                all_positions.append(pos)

    if not all_positions:
        return None

    return random.choice(all_positions)

def get_random_empty_cell(snake_positions=None, block_positions=None, width=None, height=None, side=None):
    """
    Get a random empty cell that's not occupied by snake or blocks.

    Args:
        snake_positions (list): List of positions occupied by the snake.
        block_positions (list): List of positions occupied by blocks.
        width (int): Width of the game area.
        height (int): Height of the game area.
        side (int): Size of each grid cell.

    Returns:
        tuple: Random empty position (x, y) or None if no valid positions are available.
    """
    forbidden = set()
    if snake_positions:
        forbidden.update(snake_positions)
    if block_positions:
        forbidden.update(block_positions)
    return generate_block_position(forbidden, width, height, side)

def get_tail_direction(prev_pos, tail_pos):
    """
    Calculate the direction vector from tail to previous segment.

    Args:
        prev_pos (tuple): Position of the previous segment (x, y).
        tail_pos (tuple): Position of the tail segment (x, y).

    Returns:
        tuple: Direction vector (dx, dy).
    """
    dx = prev_pos[0] - tail_pos[0]
    dy = prev_pos[1] - tail_pos[1]
    # Normalize to unit vector
    if dx != 0:
        dx = dx // abs(dx)
    if dy != 0:
        dy = dy // abs(dy)
    return (dx, dy)

def get_direction_angle(direction):
    """
    Convert a direction vector to an angle in degrees.

    Args:
        direction (tuple): Direction vector (dx, dy).

    Returns:
        int: Angle in degrees corresponding to the direction.
    """
    dx, dy = direction
    if dx == 0 and dy == -1:  # UP
        return 0
    elif dx == 1 and dy == 0:  # RIGHT
        return 270
    elif dx == 0 and dy == 1:  # DOWN
        return 180
    elif dx == -1 and dy == 0:  # LEFT
        return 90
    return 0  # Default to 0 degrees if direction is invalid

# Moved `handle_input` function from `snake.py` to `utils.py`.
def handle_input(key, current_direction):
    """
    Handle keyboard input for direction changes.

    Args:
        key (int): Key pressed (pygame key constant).
        current_direction (tuple): Current direction vector (dx, dy).

    Returns:
        tuple: New direction vector (dx, dy).
    """
    new_direction = current_direction
    if key == pygame.K_UP and current_direction != (0, 1):  # DOWN
        new_direction = (0, -1)  # UP
    elif key == pygame.K_DOWN and current_direction != (0, -1):  # UP
        new_direction = (0, 1)  # DOWN
    elif key == pygame.K_LEFT and current_direction != (1, 0):  # RIGHT
        new_direction = (-1, 0)  # LEFT
    elif key == pygame.K_RIGHT and current_direction != (-1, 0):  # LEFT
        new_direction = (1, 0)  # RIGHT
    return new_direction

def set_game_start_time(start_time):
    """Set the game start time
    This function sets the global game start time.
    Args:
        start_time (int): The start time in seconds since the epoch.
    Returns:
        None
    """
    global game_start_time
    game_start_time = start_time

def get_current_time():
    """Get the elapsed time since the game started
    This function returns the elapsed time in seconds since the game started.
    Returns:
        int: The elapsed time in seconds.
    """
    global game_start_time
    if game_start_time is None:
        return 0
    return int(time.time()) - game_start_time
