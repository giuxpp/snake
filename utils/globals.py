# globals.py

# Global counter to track the number of moves made by the snake
COUNTER = 1

# Global variable to track the game state
game_over = False

# Add a global variable to control the game running state
GAME_RUNNING = False

# Constants for snake movement: 1=Regular Movement  2=Snake Punch (faster)
SNAKE_PUNCH = 1

# Create textures at module level
BLOCK_TEXTURE = None
SNAKE_TEXTURE = None
SNAKE_HEAD_TEXTURE = None
SNAKE_TAIL_TEXTURE = None
DIRT_TEXTURE = None  # Background texture

# Global variables for key direction
UP = (0, -1)           # A direction vector indicating upward movement.
DOWN = (0, 1)          # A direction vector indicating downward movement.
LEFT = (-1, 0)         # A direction vector indicating leftward movement.
RIGHT = (1, 0)         # A direction vector indicating rightward movement.

# Color Definitions
RED = (255, 0, 0)      # RGB color value for red color.
BLACK = (0, 0, 0)      # RGB color value for black color.
CYAN = (0, 255, 255)   # RGB color value for cyan color.

# Global variable to determine the tick interval for closed eyes
close_eyes_ticks = 21
tongue_long_ticks = 33

# Add a global variable to control border collision game over
BORDER_GAME_OVER = False

def get_tick_counter(counts):
    """
    Check if the global COUNTER is a multiple of the given `counts`.
    Args:
        counts (int): The number to check divisibility against.
    Returns:
        bool: True if COUNTER is a multiple of `counts`, False otherwise.
    Example:
        get_tick_counter(5) will return True if COUNTER is 5, 10, 15, etc.,
        and False for other values like 2, 3, 4, 6, 7, etc.
    """
    return COUNTER % counts == 0

def increase_counter():
    """
    Increment the global COUNTER variable, resetting it to 1 if it exceeds 100.
    Args:
        None
    Returns:
        None
    """
    global COUNTER
    if COUNTER >= 100:
        COUNTER = 1
    else:
        COUNTER += 1