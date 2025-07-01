# globals.py

# Global variable to track the current game level
LEVEL = 1

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

def select_level(level):
    """
    Set the global LEVEL variable to the specified level.
    Args:
        level (int): The level to set.
    Returns:
        None
    """
    global LEVEL
    if isinstance(level, int) and level > 0:
        LEVEL = level
    else:
        raise ValueError("Level must be a positive integer.")

    if level == 1:
            print("Level 1 selected: Easy mode.")
            N_BLOCKS = 7             # The number of blocks in the game.
            TOTAL_SCORE_TO_WIN = 50 # The total score required to win the game.
            BORDER_GAME_OVER = False
            SELF_COLLISION_GAME_OVER = False
    elif level == 2:
            print("Level 2 selected: Medium mode.")
            N_BLOCKS = 6
            TOTAL_SCORE_TO_WIN = 100
            BORDER_GAME_OVER = True
            SELF_COLLISION_GAME_OVER = False
    elif level == 3:
            print("Level 3 selected: Hard mode.")
            N_BLOCKS = 5             # The number of blocks in the game.
            TOTAL_SCORE_TO_WIN = 150 # The total score required to win the game.
            BORDER_GAME_OVER = True
            SELF_COLLISION_GAME_OVER = True

def clear_display(screen):
    """
    Clear the display by filling it with black.
    Args:
        screen (Surface): The Pygame surface to clear.
    Returns:
        None
    """
    screen.fill((0, 0, 0))  # Fill the screen with black
    pygame.display.flip()

def display_level_selection(screen):
    """
    Display the level selection menu on a black background.
    Args:
        screen (Surface): The Pygame surface to draw the menu on.
    Returns:
        int: The selected level (1, 2, or 3).
    """
    clear_display(screen)

    font = pygame.font.SysFont(None, 60)
    title_text = font.render("SELECCIONA NIVEL", True, (255, 255, 255))  # White text
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(title_text, title_rect)

    easy_text = font.render("FACIL (1)", True, (0, 255, 0))  # Green text for easy
    easy_rect = easy_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    screen.blit(easy_text, easy_rect)

    medium_text = font.render("MEDIO (2)", True, (255, 255, 0))  # Yellow text for medium
    medium_rect = medium_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    screen.blit(medium_text, medium_rect)

    hard_text = font.render("DIFICIL (3)", True, (255, 0, 0))  # Red text for hard
    hard_rect = hard_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90))
    screen.blit(hard_text, hard_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_3:
                    return 3
        pygame.time.wait(50)
