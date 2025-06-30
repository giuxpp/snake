# Configuration Parameters

"""
WIDTH: int
    The width of the game window in pixels.

HEIGHT: int
    The height of the game window in pixels.

SIDE: int
    Size of each grid cell in the game.

STEP: int
    The distance in pixels that all blocks move on every step. Equal to SIDE.

FPS: int
    Frames per second. Increased for smoother animation.

SNAKE_SPEED: int
    The speed at which the snake moves, measured in blocks per second.

MOVE_DELAY: int
    The number of frames between each snake movement. Calculated as FPS // SNAKE_SPEED.

N_BLOCKS: int
    The number of blocks in the game.

RED: tuple
    RGB color value for red color.

BLACK: tuple
    RGB color value for black color.

CYAN: tuple
    RGB color value for cyan color.

BLOCKS_COLOR: tuple
    RGB color value for the color of the blocks. Also referred to as YELLOW_MUSTARD.

SNAKE_COLOR: tuple
    RGB color value for the color of the snake. Also referred to as GREEN_DARK.

SNAKE_HEAD_COLOR: tuple
    RGB color value for the color of the snake's head. A darker shade of SNAKE_COLOR.

SNAKE_TAIL_COLOR: tuple
    RGB color value for the color of the snake's tail. A lighter shade of SNAKE_COLOR.

UP: tuple
    A direction vector indicating upward movement.

DOWN: tuple
    A direction vector indicating downward movement.

LEFT: tuple
    A direction vector indicating leftward movement.

RIGHT: tuple
    A direction vector indicating rightward movement.
"""

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
