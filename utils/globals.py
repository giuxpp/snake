# globals.py

# Global variable to track the current game level
LEVEL = 1

# Global counter to track the number of moves made by the snake
COUNTER = 1

# Global variable to track the game state
GAME_OVER = False
GAME_WIN = False

# Add a global variable to control the game running state
GAME_RUNNING = False

# Constants for snake movement: 1=Regular Movement  2=Snake Punch (faster)
SNAKE_PUNCH = 1

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

def get_tick_counter(counts):
    return COUNTER % counts == 0

def increase_counter():
    global COUNTER
    if COUNTER >= 100: COUNTER = 1
    else: COUNTER += 1
