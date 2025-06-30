# Configuration Parameters

WIDTH = 1200           # The width of the game window in pixels.
HEIGHT = 900           # The height of the game window in pixels.
SIDE = 30              # Size of each grid cell in the game.
STEP = SIDE            # The distance in pixels that all blocks move on every step. Equal to SIDE.
FPS = 60               # Frames per second. Increased for smoother animation.
SNAKE_SPEED = 8        # The speed at which the snake moves, measured in blocks per second.
MOVE_DELAY = FPS // SNAKE_SPEED  # The number of frames between each snake movement. Calculated as FPS // SNAKE_SPEED.
N_BLOCKS = 4           # The number of blocks in the game.
RED = (255, 0, 0)      # RGB color value for red color.
BLACK = (0, 0, 0)      # RGB color value for black color.
CYAN = (0, 255, 255)   # RGB color value for cyan color.
BLOCKS_COLOR = YELLOW_MUSTARD = (220, 220, 60)  # RGB color value for the color of the blocks. Also referred to as YELLOW_MUSTARD.
SNAKE_COLOR = GREEN_DARK = (100, 255, 100)      # RGB color value for the color of the snake. Also referred to as GREEN_DARK.
SNAKE_HEAD_COLOR = (max(0, int(SNAKE_COLOR[0] * 0.6)),
                    max(0, int(SNAKE_COLOR[1] * 0.6)),
                    max(0, int(SNAKE_COLOR[2] * 0.6)))  # RGB color value for the color of the snake's head. A darker shade of SNAKE_COLOR.
SNAKE_TAIL_COLOR = (min(250, int(SNAKE_COLOR[0] * 1.8)),
                    min(250, int(SNAKE_COLOR[1] * 1.6)),
                    min(250, int(SNAKE_COLOR[2] * 1.4)))  # RGB color value for the color of the snake's tail. A lighter shade of SNAKE_COLOR.
UP = (0, -1)           # A direction vector indicating upward movement.
DOWN = (0, 1)          # A direction vector indicating downward movement.
LEFT = (-1, 0)         # A direction vector indicating leftward movement.
RIGHT = (1, 0)         # A direction vector indicating rightward movement.

WIDTH = 1200
HEIGHT = 900
SIDE = 30
STEP = SIDE  # All blocks move SIDE on every step
FPS = 60  # Increased for smoother animation
SNAKE_SPEED = 8  # Snake moves per second
MOVE_DELAY = FPS // SNAKE_SPEED  # Frames between each snake movement
N_BLOCKS = 4
RED = (255, 0, 0)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
BLOCKS_COLOR = YELLOW_MUSTARD = (220, 220, 60)  # Yellow for blocks
SNAKE_COLOR = GREEN_DARK = (100, 255, 100)  # Darker green for snake
SNAKE_HEAD_COLOR = (max(0, int(SNAKE_COLOR[0] * 0.6)),
                    max(0, int(SNAKE_COLOR[1] * 0.6)),
                    max(0, int(SNAKE_COLOR[2] * 0.6)))
SNAKE_TAIL_COLOR = (min(250, int(SNAKE_COLOR[0] * 1.8)),
                    min(250, int(SNAKE_COLOR[1] * 1.6)),
                    min(250, int(SNAKE_COLOR[2] * 1.4)))
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
