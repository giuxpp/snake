import utils.globals

# Configuration Parameters

# Display Configuration and Resolution Parameters
WIDTH = 1200             # The width of the game window in pixels.
HEIGHT = 900             # The height of the game window in pixels.
SIDE = 30                # Size of each grid cell in the game.
FPS = 60                 # Frames per second. Increased for smoother animation.
SNAKE_SPEED = 5          # The speed at which the snake moves, measured in blocks per second.
MOVE_DELAY = FPS // SNAKE_SPEED  # The number of frames between each snake movement. Calculated as FPS // SNAKE_SPEED.
N_BLOCKS = 6             # The number of blocks in the game.
TOTAL_SCORE_TO_WIN = 100 # The total score required to win the game.

# Color Definitions
BLOCKS_COLOR = YELLOW_MUSTARD = (220, 220, 60)  # RGB color value for the color of the blocks. Also referred to as YELLOW_MUSTARD.
SNAKE_COLOR = GREEN_DARK = (100, 255, 100)      # RGB color value for the color of the snake. Also referred to as GREEN_DARK.
SNAKE_HEAD_COLOR = (max(0, int(SNAKE_COLOR[0] * 0.6)),
                    max(0, int(SNAKE_COLOR[1] * 0.6)),
                    max(0, int(SNAKE_COLOR[2] * 0.6)))  # RGB color value for the color of the snake's head. A darker shade of SNAKE_COLOR.
SNAKE_TAIL_COLOR = (min(250, int(SNAKE_COLOR[0] * 1.8)),
                    min(250, int(SNAKE_COLOR[1] * 1.6)),
                    min(250, int(SNAKE_COLOR[2] * 1.4)))  # RGB color value for the color of the snake's tail. A lighter shade of SNAKE_COLOR.
