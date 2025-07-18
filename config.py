import utils.globals
import sys

# Configuration Parameters

# General Game Configurations (used for different levels)
game_config = {
    # Default level set to 'baby'
    "level": "baby",
    "n_food_blocks": 6,
    "total_score_to_win": 100,
    "border_game_over": False,
    "self_collision_game_over": False,
    "food_texture": "apple"
}

# Display Configuration and Resolution Parameters
WIDTH = 800             # The width of the game window in pixels.
HEIGHT = 600             # The height of the game window in pixels.
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
        "total_score_to_win": 10,
        "border_game_over": False,
        "self_collision_game_over": False,
    },
    "medium": {
        "n_blocks": 8,
        "total_score_to_win": 75,
        "border_game_over": True,
        "self_collision_game_over": False,
    },
    "hard": {
        "n_blocks": 10,
        "total_score_to_win": 100,
        "border_game_over": True,
        "self_collision_game_over": True,
    }
}

def set_game_config(level):
    """
    Set the game configuration parameters based on the selected level.
    """
    if level not in levels_config:
        raise ValueError(f"Invalid level: {level}. Choose from 'baby', 'medium', 'hard'.")

    if   level == "baby":   config = levels_config["baby"]
    elif level == "medium": config = levels_config["medium"]
    elif level == "hard":   config = levels_config["hard"]

    game_config["level"] = level
    game_config["n_food_blocks"] = config["n_blocks"]
    game_config["total_score_to_win"] = config["total_score_to_win"]
    game_config["border_game_over"] = config["border_game_over"]
    game_config["self_collision_game_over"] = config["self_collision_game_over"]

# Added logic to reset game data and restart from level selection menu after WIN
def reset_game_data():
    """
    Reset all game data and return to level selection menu.
    """
    utils.globals.GAME_RUNNING = False
    utils.globals.select_level = True
    utils.globals.clear_display()
    set_game_config("baby")  # Default level reset

# Updated WIN state logic to handle ENTER key press
def handle_win_state(screen):
    """
    Handle the WIN state logic.
    """
    from snake import display_level_selection_menu  # Moved import inside function to avoid circular dependency

    if utils.globals.GAME_RUNNING:
        return

    if utils.globals.select_level:
        display_level_selection_menu(screen)
        return

    # Logic for ENTER key press
    if utils.globals.enter_key_pressed:
        reset_game_data()
        display_level_selection_menu(screen)

    # Logic for ESC key press
    if utils.globals.esc_key_pressed:
        utils.globals.GAME_RUNNING = False
        sys.exit()
