import pygame
import random
import sys

# === Configuration Parameters and Global Variables ===
WIDTH, HEIGHT = 800, 600
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
game_over = False

# === Texture Generation ===
def create_gradient_dot_texture(color, size=SIDE, dot_size=4):
    """Create a gradient texture with dots overlay"""
    texture = pygame.Surface((size, size), pygame.SRCALPHA)

    # Create gradient from darker to lighter
    lighter = (min(255, int(color[0] * 1.3)),
              min(255, int(color[1] * 1.3)),
              min(255, int(color[2] * 1.3)))
    darker = (max(0, int(color[0] * 0.7)),
             max(0, int(color[1] * 0.7)),
             max(0, int(color[2] * 0.7)))

    # Draw gradient background
    for y in range(size):
        blend = y / size
        line_color = (
            int(darker[0] + (lighter[0] - darker[0]) * blend),
            int(darker[1] + (lighter[1] - darker[1]) * blend),
            int(darker[2] + (lighter[2] - darker[2]) * blend)
        )
        pygame.draw.line(texture, line_color, (0, y), (size, y))

    # Add dots overlay
    highlight_color = (min(255, int(color[0] * 1.2)),
                      min(255, int(color[1] * 1.2)),
                      min(255, int(color[2] * 1.2)))

    for y in range(dot_size, size-dot_size, dot_size*2):
        for x in range(dot_size, size-dot_size, dot_size*2):
            pygame.draw.circle(texture, highlight_color, (x, y), dot_size//2)

    return texture  # Return the created texture surface

def create_serpent_head_texture(color, size=SIDE):
    """Create a special serpent head texture with scales and eyes"""
    texture = pygame.Surface((size, size), pygame.SRCALPHA)
    texture.fill(color)  # Base color
    if not texture:  # Check if surface was created successfully
        return None

    # Create darker and lighter shades for details
    darker = (max(0, int(color[0] * 0.6)),
             max(0, int(color[1] * 0.6)),
             max(0, int(color[2] * 0.6)))
    lighter = (min(255, int(color[0] * 1.2)),
              min(255, int(color[1] * 1.2)),
              min(255, int(color[2] * 1.2)))

    # Draw base gradient
    for y in range(size):
        blend = y / size
        line_color = (
            int(darker[0] + (color[0] - darker[0]) * blend),
            int(darker[1] + (color[1] - darker[1]) * blend),
            int(darker[2] + (color[2] - darker[2]) * blend)
        )
        pygame.draw.line(texture, line_color, (0, y), (size, y))

    # Add snake scales pattern (triangular scales)
    scale_size = size // 6
    for row in range(3):
        for col in range(4):
            x = col * scale_size + (row % 2) * (scale_size // 2)
            y = row * scale_size + size // 3
            if x + scale_size <= size and y + scale_size <= size:
                points = [
                    (x + scale_size//2, y),  # top
                    (x + scale_size, y + scale_size),  # bottom right
                    (x, y + scale_size)  # bottom left
                ]
                pygame.draw.polygon(texture, darker, points)
                pygame.draw.polygon(texture, color, points, 1)

    # Add eyes (two glowing circles)
    eye_color = (255, 255, 0)  # Bright yellow eyes
    eye_size = size // 6
    eye_pos_left = (size // 4, size // 3)
    eye_pos_right = (3 * size // 4, size // 3)

    # Draw eye outlines (slightly larger)
    pygame.draw.circle(texture, darker, eye_pos_left, eye_size)
    pygame.draw.circle(texture, darker, eye_pos_right, eye_size)
    # Draw the actual eyes (smaller)
    pygame.draw.circle(texture, eye_color, eye_pos_left, eye_size-1)
    pygame.draw.circle(texture, eye_color, eye_pos_right, eye_size-1)
    # Add eye pupils (black)
    pygame.draw.circle(texture, (0, 0, 0), eye_pos_left, eye_size//2)
    pygame.draw.circle(texture, (0, 0, 0), eye_pos_right, eye_size//2)

    # Add a larger forked tongue
    tongue_color = (200, 0, 0)  # Red tongue
    tongue_width = 3  # Increased width
    tongue_length = size * 0.6  # Make tongue longer
    tongue_start = (size//2, size-scale_size)
    tongue_mid = (size//2, size + tongue_length//2)
    tongue_left = (size//3 - 5, size + tongue_length)
    tongue_right = (2*size//3 + 5, size + tongue_length)

    # Draw tongue with anti-aliasing
    pygame.draw.line(texture, tongue_color, tongue_start, tongue_mid, tongue_width)
    pygame.draw.line(texture, tongue_color, tongue_mid, tongue_left, tongue_width)
    pygame.draw.line(texture, tongue_color, tongue_mid, tongue_right, tongue_width)

    # Add small circles at tongue tips for smoother appearance
    tip_radius = tongue_width // 2
    pygame.draw.circle(texture, tongue_color, (int(tongue_left[0]), int(tongue_left[1])), tip_radius)
    pygame.draw.circle(texture, tongue_color, (int(tongue_right[0]), int(tongue_right[1])), tip_radius)

    return texture

def create_snake_tail_texture(color, size=SIDE):
    """Create a special snake tail texture with a tapered, forked end"""
    texture = pygame.Surface((size, size), pygame.SRCALPHA)

    # Create darker and lighter shades for details
    darker = (max(0, int(color[0] * 0.7)),
             max(0, int(color[1] * 0.7)),
             max(0, int(color[2] * 0.7)))
    lighter = (min(255, int(color[0] * 1.2)),
              min(255, int(color[1] * 1.2)),
              min(255, int(color[2] * 1.2)))

    # Draw base gradient (vertical, getting narrower)
    for y in range(size):
        blend = y / size
        width_factor = 1.0 - (y / size) * 0.5  # Tail gets narrower towards the end
        line_color = (
            int(darker[0] + (color[0] - darker[0]) * blend),
            int(darker[1] + (color[1] - darker[1]) * blend),
            int(darker[2] + (color[2] - darker[2]) * blend)
        )
        line_width = int(size * width_factor)
        start_x = (size - line_width) // 2
        pygame.draw.line(texture, line_color, (start_x, y), (start_x + line_width, y))

    # Add a subtle forked end
    fork_color = darker
    fork_start_y = int(size * 0.7)  # Start fork at 70% of the way down
    fork_width = size // 4
    center_x = size // 2

    # Draw the fork
    points = [
        (center_x, fork_start_y),  # Top center
        (center_x - fork_width, size),  # Bottom left
        (center_x - fork_width//2, fork_start_y + size//6),  # Inner left
        (center_x, size - size//6),  # Center bottom
        (center_x + fork_width//2, fork_start_y + size//6),  # Inner right
        (center_x + fork_width, size),  # Bottom right
    ]
    pygame.draw.polygon(texture, fork_color, points)

    # Add scales (small triangles) on the top half
    scale_size = size // 8
    for y in range(0, fork_start_y, scale_size):
        width_at_y = int(size * (1.0 - (y / size) * 0.5))
        start_x = (size - width_at_y) // 2
        for x in range(start_x, start_x + width_at_y - scale_size, scale_size):
            points = [
                (x + scale_size//2, y),  # top
                (x + scale_size, y + scale_size),  # bottom right
                (x, y + scale_size)  # bottom left
            ]
            pygame.draw.polygon(texture, darker, points, 1)

    return texture

def create_dirt_texture(size=SIDE):
    """Create a grainy brown dirt texture for the background"""
    # Base brown color
    base_color = (139, 69, 19)  # Saddle brown
    texture = pygame.Surface((size, size), pygame.SRCALPHA)

    # Create variations of brown for the grainy effect
    darker = (
        max(0, base_color[0] - 30),
        max(0, base_color[1] - 30),
        max(0, base_color[2] - 30)
    )
    lighter = (
        min(255, base_color[0] + 30),
        min(255, base_color[1] + 30),
        min(255, base_color[2] + 30)
    )

    # Fill with base color
    texture.fill(base_color)

    # Add random noise for grainy effect
    for y in range(size):
        for x in range(size):
            if random.random() < 0.3:  # 30% chance for a grain
                color = random.choice([darker, lighter])
                texture.set_at((x, y), color)

    return texture

# Create textures at module level
BLOCK_TEXTURE = None
SNAKE_TEXTURE = None
SNAKE_HEAD_TEXTURE = None
SNAKE_TAIL_TEXTURE = None
DIRT_TEXTURE = None  # Background texture

def init_textures():
    """Initialize all textures with gradient-dot pattern and special head texture"""
    global BLOCK_TEXTURE, SNAKE_TEXTURE, SNAKE_HEAD_TEXTURE, SNAKE_TAIL_TEXTURE, DIRT_TEXTURE

    BLOCK_TEXTURE = create_gradient_dot_texture(BLOCKS_COLOR)
    SNAKE_TEXTURE = create_gradient_dot_texture(SNAKE_COLOR)
    SNAKE_HEAD_TEXTURE = create_serpent_head_texture(SNAKE_HEAD_COLOR)  # Special head texture
    SNAKE_TAIL_TEXTURE = create_snake_tail_texture(SNAKE_TAIL_COLOR)  # Special tail texture
    DIRT_TEXTURE = create_dirt_texture()  # Dirt texture for background

def draw_block(display, pos, color, texture=None, rotation=0):
    """Draw a textured block with optional rotation"""
    x, y = pos if isinstance(pos, tuple) else (pos[0], pos[1])

    # If no texture provided, use default textures
    if texture is None:
        if color == BLOCKS_COLOR:
            texture = BLOCK_TEXTURE
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
    font = pygame.font.SysFont(None, 100)
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)
    font2 = pygame.font.SysFont(None, 60)
    score_text = font2.render(f"Score: {score}", True, (255, 255, 255))  # White color for score
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    screen.blit(score_text, score_rect)
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

def draw_score_label(screen, score):
    font = pygame.font.SysFont(None, 40)
    text = font.render(f"Score: {score}", True, (255, 255, 0))
    text_rect = text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(text, text_rect)

def is_opposite_direction(current, new):
    """Check if new direction is opposite to current direction"""
    return (current[0] == -new[0] and current[1] == -new[1])

# === Classes ===
class Block:
    def __init__(self, pos, color=None):
        self.pos = pos
        self._color = color
        self.hit = False
        self.attached = False
        self.path_index = None
        self.ready_to_attach = False
        self.texture = None

    @property
    def color(self):
        return self._color if self._color is not None else BLOCKS_COLOR

    def update_texture(self):
        """Update the block's texture based on its color"""
        if not self.texture:
            self.texture = create_gradient_dot_texture(self.color)

    def draw(self, display):
        """Draw the block on the display"""
        if not self.texture:
            self.update_texture()
        draw_block(display, self.pos, self.color, self.texture)

    def handle_collision(self, snake):
        """Handle collision with snake. Returns score increase."""
        return 0

class RegularBlock(Block):
    def __init__(self, pos):
        super().__init__(pos, BLOCKS_COLOR)

    def handle_collision(self, snake):
        """Regular blocks add 1 to score and make the snake grow"""
        return 1

class DirectionManager:
    def __init__(self, initial_direction=RIGHT):
        self.current_direction = initial_direction
        self.direction_queue = []

    def handle_key_press(self, key):
        """Handle keyboard input for direction changes"""
        new_direction = None
        if key == pygame.K_UP:
            new_direction = UP
        elif key == pygame.K_DOWN:
            new_direction = DOWN
        elif key == pygame.K_LEFT:
            new_direction = LEFT
        elif key == pygame.K_RIGHT:
            new_direction = RIGHT

        if new_direction:
            self.queue_direction(new_direction)

    def queue_direction(self, new_direction):
        """Try to queue a new direction, ensuring no 180-degree turns"""
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
        """Get the next valid direction from the queue"""
        if self.direction_queue:
            self.current_direction = self.direction_queue.pop(0)
        return self.current_direction

# === Functions ===
def lerp(start, end, t):
    """Linear interpolation between start and end points"""
    x1, y1 = start
    x2, y2 = end
    return (
        x1 + (x2 - x1) * t,
        y1 + (y2 - y1) * t
    )

def get_segment_position(current_pos, target_pos, frame, total_frames):
    """Get interpolated position for a snake segment"""
    if frame >= total_frames:
        return target_pos
    t = frame / total_frames
    t = max(0.0, min(1.0, t))  # Clamp between 0 and 1
    # Use cubic easing for smoother start/stop
    t = t * t * (3 - 2 * t)
    return lerp(current_pos, target_pos, t)

def get_tail_direction(prev_pos, tail_pos):
    """Calculate the direction vector from tail to previous segment"""
    dx = prev_pos[0] - tail_pos[0]
    dy = prev_pos[1] - tail_pos[1]
    # Normalize to unit vector
    if dx != 0:
        dx = dx // abs(dx)
    if dy != 0:
        dy = dy // abs(dy)
    return (dx, dy)

# Movement interpolation parameters
def lerp(start, end, t):
    """Linear interpolation between two points"""
    x1, y1 = start
    x2, y2 = end
    return (
        x1 + (x2 - x1) * t,
        y1 + (y2 - y1) * t
    )

def get_segment_position(current, target, frame, total_frames):
    """Get interpolated position for a snake segment"""
    if frame >= total_frames:
        return target
    t = frame / total_frames
    t = max(0.0, min(1.0, t))  # Clamp between 0 and 1
    # Use cubic easing for smoother start/stop
    t = t * t * (3 - 2 * t)
    return lerp(current, target, t)

def generate_initial_blocks():
    """Generate initial blocks for the game start"""
    blocks = []
    forbidden = {(WIDTH // 4, HEIGHT // 2)}  # Initial snake position
    for _ in range(N_BLOCKS):
        pos = generate_block_position(forbidden)
        if pos:
            blocks.append(RegularBlock(pos))
            forbidden.add(pos)
    return blocks

def generate_block_position(forbidden):
    """Generate a new random position for a block aligned to the grid"""
    cols = WIDTH // SIDE
    rows = HEIGHT // SIDE

    # Create a list of all valid grid positions
    all_positions = []
    for x in range(cols):
        for y in range(rows):
            pos = (x * SIDE, y * SIDE)
            if pos not in forbidden:
                all_positions.append(pos)

    if not all_positions:
        return None

    return random.choice(all_positions)

def get_random_empty_cell(snake_positions=None, block_positions=None):
    """Get a random empty cell that's not occupied by snake or blocks"""
    forbidden = set()
    if snake_positions:
        forbidden.update(snake_positions)
    if block_positions:
        forbidden.update(block_positions)
    return generate_block_position(forbidden)

def update_blocks(blocks, snake, score):
    """Update blocks positions and handle collisions"""
    snake_head = snake[0]
    print(f"Snake head at: {snake_head}")
    print(f"Block positions: {[block.pos for block in blocks]}")

    # Check collisions with snake head
    for block in blocks[:]:  # Create a copy of the list to safely modify it
        # Print comparison of positions for debugging
        if block.pos[0] == snake_head[0]:
            print(f"X match found at {block.pos[0]}")
        if block.pos[1] == snake_head[1]:
            print(f"Y match found at {block.pos[1]}")

        # Check if the snake head overlaps with any block
        if block.pos[0] == snake_head[0] and block.pos[1] == snake_head[1]:
            print(f"Collision detected with block at {block.pos}!")
            if not block.hit:
                print("Processing collision...")
                block.hit = True
                score_increase = block.handle_collision(snake)
                score += score_increase
                print(f"Score increased by {score_increase}")
                blocks.remove(block)
                print(f"Block removed. Remaining blocks: {len(blocks)}")

                # Keep the tail position for growing
                old_tail = snake[-1]

                # Grow the snake by adding a new segment at the tail position
                snake.append(old_tail)
                print(f"Snake grown. New length: {len(snake)}")

                # Create a new block in a random empty position
                forbidden = {pos for pos in snake}
                forbidden.update(b.pos for b in blocks)
                new_block_pos = generate_block_position(forbidden)
                if new_block_pos:
                    blocks.append(RegularBlock(new_block_pos))
                    print(f"New block added at {new_block_pos}")
                break

    return score

def draw_blocks(blocks, display):
    """Draw all blocks on the display"""
    for block in blocks:
        block.draw(display)

def draw_snake(display, snake):
    """Draw the snake with special head and tail textures"""
    for i, pos in enumerate(snake):
        if i == 0:  # Head
            draw_block(display, pos, SNAKE_HEAD_COLOR)
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

def handle_input(key, current_direction):
    """Handle keyboard input for direction changes"""
    new_direction = current_direction
    if key == pygame.K_UP and current_direction != DOWN:
        new_direction = UP
    elif key == pygame.K_DOWN and current_direction != UP:
        new_direction = DOWN
    elif key == pygame.K_LEFT and current_direction != RIGHT:
        new_direction = LEFT
    elif key == pygame.K_RIGHT and current_direction != LEFT:
        new_direction = RIGHT
    return new_direction

def get_direction_angle(direction):
    """Convert a direction vector to an angle in degrees."""
    dx, dy = direction
    if dx == 0 and dy == -1:  # UP
        return 0
    elif dx == 1 and dy == 0:  # RIGHT
        return 270
    elif dx == 0 and dy == 1:  # DOWN
        return 180
    elif dx == -1 and dy == 0:  # LEFT
        return 90
    return 0  # Default to 0 degrees if direction is invalid

def draw_background(display):
    """Draw the background texture to fill the screen."""
    for x in range(0, WIDTH, SIDE):
        for y in range(0, HEIGHT, SIDE):
            display.blit(DIRT_TEXTURE, (x, y))

# === Main Function ===
def main():
    # Initialize Pygame and create the display
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)  # Make the window non-resizable
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    # Initialize textures once
    init_textures()

    while True:  # Main game loop for multiple plays
        # Initialize game state
        center_x = (WIDTH // SIDE // 2) * SIDE
        center_y = (HEIGHT // SIDE // 2) * SIDE
        snake = [(center_x, center_y)]  # Start at the center of the screen
        snake_length = len(snake)  # Track snake length for growth
        direction_manager = DirectionManager(None)  # Initialize with no direction
        blocks = generate_initial_blocks()
        score = 0
        game_over = False
        move_counter = 0  # Counter for move delay
        game_started = False  # Flag to track if the game has started

        # Game loop for one play
        while not game_over:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # End game if ESC is pressed during gameplay
                    if game_started and event.key == pygame.K_ESCAPE:
                        game_over = True
                        continue
                    # Start game on first arrow key press
                    if not game_started and event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        game_started = True
                        direction_manager.current_direction = None  # Reset initial direction
                        direction_manager.handle_key_press(event.key)  # Set initial direction based on first key press
                    direction_manager.handle_key_press(event.key)

            # Don't update snake position until game has started
            if not game_started:
                # Just draw the initial state
                display.fill((0, 0, 0))  # Clear screen
                draw_background(display)  # Draw background texture
                draw_blocks(blocks, display)
                draw_snake(display, snake)
                draw_score_label(display, score)
                pygame.display.flip()
                clock.tick(FPS)
                continue

            # Update game state
            move_counter += 1
            if move_counter >= MOVE_DELAY:
                move_counter = 0

                # Update snake position
                direction = direction_manager.get_next_direction()
                if direction is None:
                    direction = RIGHT  # Default to RIGHT if no direction is set
                # Ensure we're moving in grid-aligned steps
                new_head = (
                    (snake[0][0] + direction[0] * STEP) // SIDE * SIDE,
                    (snake[0][1] + direction[1] * STEP) // SIDE * SIDE
                )
                print(f"Moving to new head position: {new_head}")

                # Check wall collision
                if (new_head[0] < 0 or new_head[0] >= WIDTH or
                    new_head[1] < 0 or new_head[1] >= HEIGHT):
                    print("Wall collision detected!")
                    game_over = True
                    continue

                # Check for collisions with self
                if new_head in snake[1:]:
                    game_over = True
                    continue

                # Move snake
                snake.insert(0, new_head)

                # Update blocks and score - this will grow the snake if a block is hit
                old_score = score
                score = update_blocks(blocks, snake, score)

                # Only remove tail if we didn't collect a block (score didn't change)
                if score == old_score:
                    snake.pop()

            # Drawing
            display.fill((0, 0, 0))  # Clear screen
            draw_background(display)  # Draw the background texture
            draw_blocks(blocks, display)
            draw_snake(display, snake)
            draw_score_label(display, score)
            pygame.display.flip()
            clock.tick(FPS)

        # Game Over screen
        if not show_game_over(display, score):  # If show_game_over returns False, exit game
            break

if __name__ == "__main__":
    main()
