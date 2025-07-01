import utils.globals

# Configuration Parameters

# General Game Configurations (used for different levels)
N_BLOCKS = 6                     # The number of blocks in the game.
TOTAL_SCORE_TO_WIN = 100         # The total score required to win the game.
BORDER_GAME_OVER = False         # Global variable to control border collision game over
SELF_COLLISION_GAME_OVER = False # Global variable to control self-collision game over

game_config = {
    "n_food_blocks": 6,
    "total_score_to_win": 100,
    "border_game_over": False,
    "self_collision_game_over": False
}

# Display Configuration and Resolution Parameters
WIDTH = 1000             # The width of the game window in pixels.
HEIGHT = 750             # The height of the game window in pixels.
SIDE = 30                # Size of each grid cell in the game.
FPS = 60                 # Frames per second. Increased for smoother animation.
SNAKE_SPEED = 5          # The speed at which the snake moves, measured in blocks per second.
MOVE_DELAY = FPS // SNAKE_SPEED  # The number of frames between each snake movement. Calculated as FPS // SNAKE_SPEED.

# Color Definitions
BLOCKS_COLOR = YELLOW_MUSTARD = (220, 220, 60)  # RGB color value for the color of the blocks. Also referred to as YELLOW_MUSTARD.
SNAKE_COLOR = GREEN_DARK = (100, 255, 100)      # RGB color value for the color of the snake. Also referred to as GREEN_DARK.
SNAKE_HEAD_COLOR = (max(0, int(SNAKE_COLOR[0] * 0.6)),
                    max(0, int(SNAKE_COLOR[1] * 0.6)),
                    max(0, int(SNAKE_COLOR[2] * 0.6)))  # RGB color value for the color of the snake's head. A darker shade of SNAKE_COLOR.
SNAKE_TAIL_COLOR = (min(250, int(SNAKE_COLOR[0] * 1.8)),
                    min(250, int(SNAKE_COLOR[1] * 1.6)),
                    min(250, int(SNAKE_COLOR[2] * 1.4)))  # RGB color value for the color of the snake's tail. A lighter shade of SNAKE_COLOR.

# Configuration for different levels
levels_config = {
    "baby": {
        "n_blocks": 6,
        "total_score_to_win": 50,
        "border_game_over": False,
        "self_collision_game_over": False
    },
    "medium": {
        "n_blocks": 8,
        "total_score_to_win": 100,
        "border_game_over": True,
        "self_collision_game_over": True
    },
    "hard": {
        "n_blocks": 10,
        "total_score_to_win": 150,
        "border_game_over": True,
        "self_collision_game_over": True
    }
}

def set_game_config(level):
    """
    Set the game configuration parameters based on the selected level.
    """
    global N_BLOCKS, TOTAL_SCORE_TO_WIN, BORDER_GAME_OVER, SELF_COLLISION_GAME_OVER

    if level not in levels_config:
        raise ValueError(f"Invalid level: {level}. Choose from 'baby', 'medium', 'hard'.")

    if   level == "baby":   config = levels_config["baby"]
    elif level == "medium": config = levels_config["medium"]
    elif level == "hard":   config = levels_config["hard"]

    game_config["n_food_blocks"] = config["n_blocks"]
    game_config["total_score_to_win"] = config["total_score_to_win"]
    game_config["border_game_over"] = config["border_game_over"]
    game_config["self_collision_game_over"] = config["self_collision_game_over"]
