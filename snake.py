import pygame
import random
import sys
from utils.utils import *
from utils.textures import *
from utils.blocks import HenBlock
from utils.matrix import generate_block_position, get_random_empty_cell
from utils.globals import *
from config import *

# The distance in pixels that all blocks move on every step. Equal to SIDE.
STEP = SIDE

FOOD_BLOCKS_TEXTURE = None

def init_textures():
    """Initialize all textures with gradient-dot pattern and special head texture
    This function initializes the textures used in the game, including the block texture,
    snake texture, snake head texture, snake tail texture, and dirt texture. It sets up the
    visual appearance of the game elements.
    Returns:
        None
    """
    global HEN_TEXTURE, APPLE_TEXTURE, RABBIT_TEXTURE, SNAKE_TEXTURE, SNAKE_HEAD_TEXTURE, SNAKE_TAIL_TEXTURE, BG_TEXTURE_LEVEL_1,  BG_TEXTURE_LEVEL_2,  BG_TEXTURE_LEVEL_3

    HEN_TEXTURE = create_hen_texture(SIDE)  # Hen texture for regular blocks
    APPLE_TEXTURE = create_apple_texture(SIDE)  # Apple texture for food blocks
    RABBIT_TEXTURE = create_rabbit_texture(SIDE)  # Rabbit texture for food blocks
    SNAKE_TEXTURE = create_gradient_dot_texture(SNAKE_COLOR)
    SNAKE_HEAD_TEXTURE = create_serpent_short_thong_head_texture(SNAKE_HEAD_COLOR)  # Start with open eyes
    SNAKE_TAIL_TEXTURE = create_snake_tail_texture(SNAKE_TAIL_COLOR)
    BG_TEXTURE_LEVEL_1 = create_dirt_texture_level_1(SIDE)  # Dirt texture for background
    BG_TEXTURE_LEVEL_2 = create_dirt_texture_level_2(SIDE)  # Dirt texture for background
    BG_TEXTURE_LEVEL_3 = create_dirt_texture_level_3(SIDE)  # Dirt texture for background

def update_head_snake_textures():
    """Update the head texture based on the current tick counter
    This function updates the snake head texture based on whether the snake's eyes are closed
    or open. It changes the texture to reflect the current state of the snake's head.
    Returns:
        None
    """
    global SNAKE_HEAD_TEXTURE
    if get_tick_counter(close_eyes_ticks):
        SNAKE_HEAD_TEXTURE = create_serpent_head_texture_closed_eyes(SNAKE_HEAD_COLOR)
    elif get_tick_counter(tongue_long_ticks):
        SNAKE_HEAD_TEXTURE = create_serpent_long_thong_head_texture(SNAKE_HEAD_COLOR)
    else:
        SNAKE_HEAD_TEXTURE = create_serpent_short_thong_head_texture(SNAKE_HEAD_COLOR)

def draw_block(display, pos, color, texture=None, rotation=0):
    """Draw a textured block with optional rotation
    This function draws a block on the display at the specified position with the given color.
    It can use a texture for the block and rotate the block if needed.
    Args:
        display (Surface): The Pygame surface to draw on.
        pos (tuple): The (x, y) position to draw the block.
        color (Color): The color of the block.
        texture (Surface, optional): The texture to use for the block. Defaults to None.
        rotation (int, optional): The rotation angle for the block. Defaults to 0.
    Returns:
        None
    """
    x, y = pos if isinstance(pos, tuple) else (pos[0], pos[1])

    # If no texture provided, use default textures
    if texture is None:
        if color == BLOCKS_COLOR:
            texture = APPLE_TEXTURE
        elif color == SNAKE_HEAD_COLOR:
            texture = SNAKE_HEAD_TEXTURE
        elif color == SNAKE_TAIL_COLOR:
            texture = SNAKE_TAIL_TEXTURE
        else:
            texture = SNAKE_TEXTURE

    if texture:  # Make sure texture exists
        if rotation != 0:
            # Rotate the texture
            rotated_texture = pygame.transform.rotate(texture, rotation)
            # Adjust position to keep the center aligned
            new_x = x + (SIDE - rotated_texture.get_width()) // 2
            new_y = y + (SIDE - rotated_texture.get_height()) // 2
            display.blit(rotated_texture, (new_x, new_y))
        else:
            display.blit(texture, (x, y))
    else:
        # Fallback to solid color if texture is not available
        pygame.draw.rect(display, color, pygame.Rect(x, y, SIDE, SIDE))

def show_game_over(screen, score):
    """Display the game over screen with the final score and elapsed time
    This function shows the game over screen when the game ends. It displays the "GAME OVER"
    message, the final score, and the elapsed time. It waits for the player to close the
    window or press ENTER to restart the game.
    Args:
        screen (Surface): The Pygame surface to draw the game over screen on.
        score (int): The final score to display.
    Returns:
        bool: True if the player wants to restart the game, False otherwise.
    """
    global game_start_time

    font = pygame.font.SysFont(None, 100)
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    # Display the final score
    font2 = pygame.font.SysFont(None, 60)
    total_score_to_win = game_config["total_score_to_win"]
    score_text = font2.render(f"Puntos: {score}/{total_score_to_win}", True, (255, 255, 255))  # White color for score
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    screen.blit(score_text, score_rect)

    # Display the elapsed time
    elapsed_time = get_current_time()
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    time_text = font2.render(f"TIEMPO: {format_time(elapsed_time)}", True, (255, 255, 255))  # White color for time
    time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(time_text, time_rect)
    set_game_start_time(int(time.time()))

    # Update the display
    pygame.display.flip()

    # Wait for user to close the window or press ENTER to restart
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                return True
        pygame.time.wait(50)

def show_game_win(screen, score):
    """Display the game win screen with the final score and elapsed time
    This function shows the game win screen when the player achieves the target score.
    It displays the "YOU WIN" message, the final score, and the elapsed time.
    Args:
        screen (Surface): The Pygame surface to draw the game win screen on.
        score (int): The final score to display.
    Returns:
        bool: True if the player wants to restart the game, False otherwise.
    """
    global game_start_time

    font = pygame.font.SysFont(None, 100)
    text = font.render("¡¡ GANASTE !!", True, (0, 255, 0))  # Green color for win message
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    # Display the final score
    font2 = pygame.font.SysFont(None, 60)
    total_score_to_win = game_config["total_score_to_win"]
    score_text = font2.render(f"Puntos: {score}/{total_score_to_win}", True, (255, 255, 255))  # White color for score
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    screen.blit(score_text, score_rect)

    # Display the elapsed time
    elapsed_time = get_current_time()
    time_text = font2.render(f"TIEMPO: {format_time(elapsed_time)}", True, (255, 255, 255))  # White color for time
    time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(time_text, time_rect)
    set_game_start_time(int(time.time()))

    # Update the display
    pygame.display.flip()

    # Wait for user to close the window or press ENTER to restart
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                return True
        pygame.time.wait(50)

def draw_score_time_and_level_label(screen, score, level):
    """Draw the score, time, and level labels on the screen
    This function displays the current score, elapsed time, and selected level on the screen.
    The score is displayed in the top-right corner, the elapsed time below it, and the level below the time.
    Args:
        screen (Surface): The Pygame surface to draw the labels on.
        score (int): The current score to display.
        level (str): The selected level to display.
    Returns:
        None
    """
    font = pygame.font.SysFont(None, 40)

    # Draw score label
    total_score_to_win  = game_config["total_score_to_win"]
    score_text = font.render(f"Puntos: {score}/{total_score_to_win}", True, (255, 255, 0))
    score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(score_text, score_rect)

    # Draw time label
    elapsed_time = get_current_time()
    time_text = font.render(f"TIEMPO: {format_time(elapsed_time)}", True, (255, 255, 255))
    time_rect = time_text.get_rect(topright=(WIDTH - 10, 50))
    screen.blit(time_text, time_rect)

    # Draw level label
    level_text = font.render(f"NIVEL: {level.upper()}", True, (255, 255, 255))
    level_rect = level_text.get_rect(topright=(WIDTH - 10, 90))
    screen.blit(level_text, level_rect)

# === Classes ===
class DirectionManager:
    def __init__(self, initial_direction=RIGHT):
        """Initialize the DirectionManager with an initial direction
        This class manages the current and queued directions for the snake. It ensures that
        the snake does not make invalid turns (e.g., 180-degree turns).
        Args:
            initial_direction (tuple, optional): The initial direction (dx, dy) for the snake.
                Defaults to RIGHT.
        """
        self.current_direction = initial_direction
        self.direction_queue = []

    def handle_key_press(self, key, is_pressed):
        """Handle keyboard input for direction changes and SNAKE_PUNCH logic
        This function handles the keyboard input for changing the snake's direction and
        updates the SNAKE_PUNCH state based on key press/release events.
        Args:
            key (int): The key code of the pressed/released key.
            is_pressed (bool): True if the key is pressed, False if released.
        Returns:
            None
        """
        global SNAKE_PUNCH

        new_direction = None
        if key == pygame.K_UP:
            new_direction = UP
        elif key == pygame.K_DOWN:
            new_direction = DOWN
        elif key == pygame.K_LEFT:
            new_direction = LEFT
        elif key == pygame.K_RIGHT:
            new_direction = RIGHT

        if is_pressed:
            # This will emulate a small delay after key press to start the punch
            if get_tick_counter(2):
                SNAKE_PUNCH = 2
            if new_direction:
                self.queue_direction(new_direction)
        else:
            SNAKE_PUNCH = 1

    def queue_direction(self, new_direction):
        """Try to queue a new direction, ensuring no 180-degree turns
        This function attempts to add a new direction to the queue of directions. It checks
        if the new direction is opposite to the current or last queued direction to prevent
        invalid turns.
        Args:
            new_direction (tuple): The new direction (dx, dy) to queue.
        Returns:
            None
        """
        # If queue is empty, check against current direction
        if not self.direction_queue:
            check_against = self.current_direction
        else:
            # Check against the last queued direction
            check_against = self.direction_queue[-1]

        if check_against is None:
            check_against = new_direction  # Default to new direction if no current direction is set

        if not is_opposite_direction(check_against, new_direction):
            self.direction_queue.append(new_direction)

    def get_next_direction(self):
        """Get the next valid direction from the queue
        This function retrieves the next valid direction from the queue of directions. It
        updates the current direction to the dequeued direction.
        Returns:
            tuple: The next valid direction (dx, dy) for the snake.
        """
        if self.direction_queue:
            self.current_direction = self.direction_queue.pop(0)
        return self.current_direction

# === Functions ===
def generate_initial_blocks():
    """Generate initial blocks for the game start
    This function generates the initial blocks for the game start. It creates a list of
    blocks placed at random positions on the grid, ensuring that they do not overlap with
    the initial snake position.
    Returns:
        list: A list of generated Food objects.
    """
    blocks = []
    forbidden = {(WIDTH // 4, HEIGHT // 2)}  # Initial snake position
    for _ in range(game_config["n_food_blocks"]):
        pos = generate_block_position(forbidden)
        if pos:
            blocks.append(HenBlock(pos))
            forbidden.add(pos)
    return blocks

def update_blocks(blocks, snake, score):
    """Update blocks positions and handle collisions
    This function updates the positions of the blocks and checks for collisions with the
    snake. If the snake collides with a block, the block is "eaten" by the snake, and a
    new block is generated in a random empty position.
    Args:
        blocks (list): The list of current blocks in the game.
        snake (list): The current snake body segments.
        score (int): The current score of the player.
    Returns:
        int: The updated score after handling block collisions.
    """
    snake_head = snake[0]

    # Check collisions with snake head
    for block in blocks[:]:  # Create a copy of the list to safely modify it
        # Check if the snake head overlaps with any block
        if block.pos[0] == snake_head[0] and block.pos[1] == snake_head[1]:
            if not block.hit:
                block.hit = True
                score += 1
                blocks.remove(block)

                # Keep the tail position for growing
                old_tail = snake[-1]

                # Grow the snake by adding a new segment at the tail position
                snake.append(old_tail)

                # Create a new block in a random empty position
                forbidden = set(snake)
                forbidden.update(b.pos for b in blocks)
                new_block_pos = generate_block_position(forbidden)
                if new_block_pos:
                    blocks.append(HenBlock(new_block_pos))
                break

    return score

def draw_food_blocks(blocks, display):
    """Draw all blocks on the display
    This function draws all the blocks in the game on the display. It iterates through the
    list of blocks and draws each block using its associated texture.
    Args:
        blocks (list): The list of blocks to draw.
        display (Surface): The Pygame surface to draw on.
    Returns:
        None
    """
    for block in blocks:
        block.draw(display)

def draw_snake(display, snake, direction_manager):
    """Draw the snake with special head and tail textures, rotating the head
    This function draws the snake on the display. It uses a special texture for the snake's
    head and tail, and it rotates the head texture based on the snake's movement direction.
    Args:
        display (Surface): The Pygame surface to draw on.
        snake (list): The current snake body segments.
        direction_manager (DirectionManager): The direction manager for handling snake direction.
    Returns:
        None
    """
    for i, pos in enumerate(snake):
        if i == 0:  # Head
            if len(snake) > 1:
                head_direction = get_tail_direction(snake[0], snake[1])
            else:
                head_direction = direction_manager.get_next_direction() or RIGHT
            head_angle = get_direction_angle(head_direction)
            draw_block(display, pos, SNAKE_HEAD_COLOR, rotation=head_angle)
        elif i == len(snake) - 1:  # Tail
            # Calculate tail direction
            if len(snake) > 1:
                tail_direction = get_tail_direction(snake[-2], snake[-1])
                tail_angle = get_direction_angle(tail_direction)
                draw_block(display, pos, SNAKE_TAIL_COLOR, rotation=tail_angle)
            else:
                draw_block(display, pos, SNAKE_TAIL_COLOR)  # No rotation for single-segment snake
        else:  # Body
            draw_block(display, pos, SNAKE_COLOR)

def draw_background(display, texture):
    """Draw the background texture to fill the screen
    This function fills the entire screen with the dirt texture, creating the background
    for the game. It tiles the texture across the screen dimensions.
    Args:
        display (Surface): The Pygame surface to draw on.
    Returns:
        None
    """
    for x in range(0, WIDTH, SIDE):
        for y in range(0, HEIGHT, SIDE):
            display.blit(texture, (x, y))

# Refactored main function to reduce cognitive complexity
# Extracted game initialization and game loop logic into separate functions

def initialize_game():
    """Initialize the game state
    This function initializes the game state, including the snake's initial position,
    direction manager, blocks, score, and game start flag.
    Returns:
        tuple: A tuple containing the initial snake, direction manager, blocks, score, and game started flag.
    """
    center_x = (WIDTH // SIDE // 2) * SIDE
    center_y = (HEIGHT // SIDE // 2) * SIDE
    snake = [(center_x, center_y), (center_x - STEP, center_y)]  # Start with head and tail
    direction_manager = DirectionManager(None)
    blocks = generate_initial_blocks()
    score = 0
    game_started = False
    return snake, direction_manager, blocks, score, game_started

# Further refactored game_loop to reduce cognitive complexity
# Extracted event handling and rendering logic into separate functions

def handle_events(game_started, direction_manager):
    """Handle Pygame events for the game
    This function processes the Pygame events, such as keyboard input and window events.
    It handles the game start, direction changes, and game over conditions.
    Args:
        game_started (bool): The current game started flag.
        direction_manager (DirectionManager): The direction manager for handling snake direction.
    Returns:
        tuple: A tuple containing the updated game started flag and game over flag.
    """
    GAME_OVER = False
    global GAME_RUNNING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            is_pressed = event.type == pygame.KEYDOWN
            if game_started and event.key == pygame.K_ESCAPE:
                GAME_OVER = True
                continue
            if not game_started and is_pressed and event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                game_started = True
                GAME_RUNNING = True  # Set GAME_RUNNING to True when the game starts
                direction_manager.current_direction = None
                if game_start_time is None:
                    set_game_start_time(int(time.time()))
                try:
                    direction_manager.handle_key_press(event.key, is_pressed)
                except Exception:
                    direction_manager.current_direction = LEFT
            direction_manager.handle_key_press(event.key, is_pressed)
    return game_started, GAME_OVER

def render_game(display, blocks, snake, score, direction_manager, level):
    """Render the game elements on the display
    This function renders all the game elements on the display, including the background,
    blocks, snake, score label, time label, and level label. It updates the display with the rendered content.
    Args:
        display (Surface): The Pygame surface to draw on.
        blocks (list): The list of current blocks in the game.
        snake (list): The current snake body segments.
        score (int): The current score of the player.
        direction_manager (DirectionManager): The direction manager for handling snake direction.
        level (str): The selected level to display.
    Returns:
        None
    """
    global GAME_RUNNING
    display.fill((0, 0, 0))

    # Draw the background based on the selected level
    if game_config["level"] == "baby":
        draw_background(display, BG_TEXTURE_LEVEL_1)
    elif game_config["level"] == "medium":
        draw_background(display, BG_TEXTURE_LEVEL_2)
    elif game_config["level"] == "hard":
        draw_background(display, BG_TEXTURE_LEVEL_3)
    else:
        draw_background(display, BG_TEXTURE_LEVEL_1)

    # Draw blocks and snake
    draw_food_blocks(blocks, display)
    draw_snake(display, snake, direction_manager)

    if GAME_RUNNING:
        draw_score_time_and_level_label(display, score, level)
    pygame.display.flip()

def update_snake(snake, direction_manager, blocks, score):
    """Update the snake's position and check for collisions
    This function updates the snake's position based on its current direction. It checks
    for collisions with the game boundaries, itself, and blocks. It returns a game over
    flag if a collision occurs.
    Args:
        snake (list): The current snake body segments.
        direction_manager (DirectionManager): The direction manager for handling snake direction.
        blocks (list): The list of current blocks in the game.
        score (int): The current score of the player.
    Returns:
        tuple: A tuple containing a game over flag and the updated score.
    """
    direction = direction_manager.get_next_direction() or RIGHT
    new_head = (
        (snake[0][0] + direction[0] * STEP) // SIDE * SIDE,
        (snake[0][1] + direction[1] * STEP) // SIDE * SIDE
    )

    # Ensure the initial movement does not trigger a collision
    if len(snake) == 2 and new_head == snake[1]:
        snake.insert(0, new_head)
        snake.pop()
        return False, score

    if game_config["border_game_over"]:
        # Check for collision with borders
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            return True, score
    else:
        # Handle border wrapping logic
        if new_head[0] < 0:  # Left border
            new_head = (WIDTH - SIDE, new_head[1])
        elif new_head[0] >= WIDTH:  # Right border
            new_head = (0, new_head[1])
        elif new_head[1] < 0:  # Top border
            new_head = (new_head[0], HEIGHT - SIDE)
        elif new_head[1] >= HEIGHT:  # Bottom border
            new_head = (new_head[0], 0)

    # Check for collision with itself
    if game_config["self_collision_game_over"]:
        if new_head in snake[1:]: return True, score

    snake.insert(0, new_head)
    increase_counter()
    old_score = score
    score = update_blocks(blocks, snake, score)

    if score == old_score:
        snake.pop()

    return False, score

def game_loop(display, clock, snake, direction_manager, blocks, score, game_started, level):
    """Main game loop
    This function is the main loop of the game. It handles the game events, updates the
    game state, and renders the game elements. It continues running until the game is
    over.
    Args:
        display (Surface): The Pygame surface to draw on.
        clock (Clock): The Pygame clock object for controlling the frame rate.
        snake (list): The current snake body segments.
        direction_manager (DirectionManager): The direction manager for handling snake direction.
        blocks (list): The list of current blocks in the game.
        score (int): The current score of the player.
        game_started (bool): The flag indicating if the game has started.
        level (str): The selected level to display.
    Returns:
        int: The final score when the game is over.
    """
    global SNAKE_PUNCH, GAME_RUNNING
    move_counter = 0
    game_over = False

    while not game_over:
        game_started, game_over = handle_events(game_started, direction_manager)

        if game_over:
            GAME_RUNNING = False  # Reset GAME_RUNNING to False when the game is over
        # Ensure SNAKE_PUNCH is reset to 1 if no button is pressed
        if not pygame.key.get_pressed():
            SNAKE_PUNCH = 1

        update_head_snake_textures()

        if not game_started:
            render_game(display, blocks, snake, score, direction_manager, level)
            clock.tick(FPS)
            continue

        move_counter += 1
        if move_counter >= MOVE_DELAY // SNAKE_PUNCH:
            move_counter = 0
            game_over, score = update_snake(snake, direction_manager, blocks, score)

        render_game(display, blocks, snake, score, direction_manager, level)
        clock.tick(FPS)

        if score >= game_config["total_score_to_win"]:
            GAME_RUNNING = False
            GAME_WIN = True
            game_over = True
            break

    return score

def display_level_selection_menu(screen):
    """Display a menu to select the game level.
    Args:
        screen (Surface): The Pygame surface to draw the menu on.
    Returns:
        int: The selected level (1 for Easy, 2 for Medium, 3 for Hard).
    """
    # Clear display
    screen.fill((0, 0, 0))  # Fill the screen with black
    pygame.display.flip()

    font = pygame.font.SysFont(None, 60)

    # Display the menu title
    title_text = font.render("SELECCIONA NIVEL", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(title_text, title_rect)

    # Display level options
    easy_text = font.render("Baby (1)", True, (0, 255, 0))
    easy_rect = easy_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    screen.blit(easy_text, easy_rect)

    medium_text = font.render("Medium (2)", True, (255, 255, 0))
    medium_rect = medium_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    screen.blit(medium_text, medium_rect)

    hard_text = font.render("Hard (3)", True, (255, 0, 0))
    hard_rect = hard_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90))
    screen.blit(hard_text, hard_rect)

    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "baby"
                elif event.key == pygame.K_2:
                    return "medium"
                elif event.key == pygame.K_3:
                    return "hard"
        pygame.time.wait(50)

def main():
    """Main entry point of the game
    This function is the main entry point of the game. It initializes Pygame, creates the
    game window, and runs the game loop. It also handles the game over screen and
    restarting the game.
    Returns:
        None
    """
    global game_start_time
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    init_textures()  # Initialize textures once at the start

    while True:
        snake, direction_manager, blocks, score, game_started = initialize_game()
        game_start_time = None  # Reset game start time on restart
        # Display level selection menu and set game configuration
        selected_level = display_level_selection_menu(display)
        set_game_config(selected_level)
        score = game_loop(display, clock, snake, direction_manager, blocks, score, game_started, selected_level)
        if GAME_WIN and not show_game_win(display, score):
            break
        if not show_game_over(display, score):
            break


if __name__ == "__main__":
    main()
