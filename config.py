# Configuration Parameters
WIDTH = 1000
HEIGHT = 750
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
