import random

# Utility functions

def lerp(start, end, t):
    """Linear interpolation between start and end points"""
    x1, y1 = start
    x2, y2 = end
    return (
        x1 + (x2 - x1) * t,
        y1 + (y2 - y1) * t
    )

def get_segment_position(current, target, frame, total_frames):
    """Get interpolated position for a snake segment"""
    if frame >= total_frames:
        return target
    t = frame / total_frames
    t = max(0.0, min(1.0, t))  # Clamp between 0 and 1
    # Use cubic easing for smoother start/stop
    t = t * t * (3 - 2 * t)
    return lerp(current, target, t)

def generate_block_position(forbidden, width, height, side):
    """Generate a new random position for a block aligned to the grid"""
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
    """Get a random empty cell that's not occupied by snake or blocks"""
    forbidden = set()
    if snake_positions:
        forbidden.update(snake_positions)
    if block_positions:
        forbidden.update(block_positions)
    return generate_block_position(forbidden, width, height, side)

def get_tail_direction(prev_pos, tail_pos):
    """Calculate the direction vector from tail to previous segment"""
    dx = prev_pos[0] - tail_pos[0]
    dy = prev_pos[1] - tail_pos[1]
    # Normalize to unit vector
    if dx != 0:
        dx = dx // abs(dx)
    if dy != 0:
        dy = dy // abs(dy)
    return (dx, dy)

def get_direction_angle(direction):
    """Convert a direction vector to an angle in degrees."""
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
