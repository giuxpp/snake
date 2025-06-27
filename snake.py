import pygame
import random
import sys

# === General Configuration Parameters ===
WIDTH, HEIGHT = 800, 600
SIDE = 30
STEP = SIDE  # All blocks move SIDE on every step
FPS = 15  # Increase FPS for smoother movement
SNAKE_MOVE_INTERVAL = 2  # Move snake every 2 frames for classic speed
N_BLOCKS = 4

# === Colors ===
RED = (255, 0, 0)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)

# === Shape Configuration Parameters ===
BLOCKS_COLOR = YELLOW_MUSTARD = (220, 220, 60)  # Yellow for blocks
SNAKE_COLOR = GREEN_DARK = (100, 255, 100)  # Darker green for snake
# Head is 20% darker than the snake color
SNAKE_HEAD_COLOR = (max(0, int(SNAKE_COLOR[0] * 0.6)),
                    max(0, int(SNAKE_COLOR[1] * 0.6)),
                    max(0, int(SNAKE_COLOR[2] * 0.6)))
# Tail is 20% lighter than the snake color
SNAKE_TAIL_COLOR = (min(250, int(SNAKE_COLOR[0] * 1.8)),
                    min(250, int(SNAKE_COLOR[1] * 1.6)),
                    min(250, int(SNAKE_COLOR[2] * 1.4)))

# === Directions ===
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

game_over = False  # Global variable to track game state

# Generate random positions for blocks
def generate_blocks(n, forbidden=None):
    blocks = []
    cols = WIDTH // SIDE
    rows = HEIGHT // SIDE
    if forbidden is None:
        forbidden = set()
    # Generate all possible grid positions
    all_positions = [(x * SIDE, y * SIDE) for x in range(cols) for y in range(rows)]
    available_positions = [pos for pos in all_positions if pos not in forbidden]
    random.shuffle(available_positions)
    for pos in available_positions:
        if len(blocks) >= n:
            break
        blocks.append({'pos': pos, 'color': BLOCKS_COLOR})
    return blocks

def init_block(block):
    """Initialize a block with default properties"""
    block['hit'] = False
    block['attached'] = False
    block['path_index'] = None
    block['ready_to_attach'] = False
    return block

def generate_single_block(forbidden=None):
    cols = WIDTH // SIDE
    rows = HEIGHT // SIDE
    if forbidden is None:
        forbidden = set()
    all_positions = [(x * SIDE, y * SIDE) for x in range(cols) for y in range(rows)]
    available_positions = [pos for pos in all_positions if pos not in forbidden]
    if not available_positions:
        return None
    pos = random.choice(available_positions)
    return {'pos': pos, 'color': BLOCKS_COLOR}

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

# Create textures at module level
BLOCK_TEXTURE = None
SNAKE_TEXTURE = None
SNAKE_HEAD_TEXTURE = None
SNAKE_TAIL_TEXTURE = None

def init_textures():
    """Initialize all textures with gradient-dot pattern and special head texture"""
    global BLOCK_TEXTURE, SNAKE_TEXTURE, SNAKE_HEAD_TEXTURE, SNAKE_TAIL_TEXTURE

    BLOCK_TEXTURE = create_gradient_dot_texture(BLOCKS_COLOR)
    SNAKE_TEXTURE = create_gradient_dot_texture(SNAKE_COLOR)
    SNAKE_HEAD_TEXTURE = create_serpent_head_texture(SNAKE_HEAD_COLOR)  # Special head texture
    SNAKE_TAIL_TEXTURE = create_snake_tail_texture(SNAKE_TAIL_COLOR)  # Special tail texture

def draw_block(screen, x, y, color=SNAKE_COLOR, rotation=0):
    """Draw a textured block with optional rotation"""
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
            screen.blit(rotated_texture, (new_x, new_y))
        else:
            screen.blit(texture, (x, y))

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

class DirectionManager:
    def __init__(self, initial_direction):
        self.current_direction = initial_direction
        self.direction_queue = []

    def queue_direction(self, new_direction):
        """Try to queue a new direction, ensuring no 180-degree turns"""
        # If queue is empty, check against current direction
        if not self.direction_queue:
            check_against = self.current_direction
        else:
            # Check against the last queued direction
            check_against = self.direction_queue[-1]

        if not is_opposite_direction(check_against, new_direction):
            self.direction_queue.append(new_direction)

    def get_next_direction(self):
        """Get the next valid direction from the queue"""
        if self.direction_queue:
            self.current_direction = self.direction_queue.pop(0)
        return self.current_direction

def get_direction_angle(pos1, pos2):
    """Calculate rotation angle based on movement direction between two positions"""
    x1, y1 = pos1  # Tail position
    x2, y2 = pos2  # Previous segment position
    # Calculate movement vector from previous segment to tail
    # This gives us the direction the tail is moving
    dx = x2 - x1
    dy = y2 - y1
    # Convert to angle (default orientation is UP)
    # Calculate the angle the tail should point, opposite to movement direction
    if dx == 0:
        if dy > 0:  # Tail below previous segment (moving DOWN)
            return 180  # Point UP
        else:  # Tail above previous segment (moving UP)
            return 0  # Point DOWN
    elif dy == 0:
        if dx > 0:  # Tail right of previous segment (moving RIGHT)
            return -90  # Point LEFT
        else:  # Tail left of previous segment (moving LEFT)
            return 90  # Point RIGHT
    return 0  # Default case

def main():
    global game_over
    try:
        # Initialize Pygame and display once
        pygame.init()
        if not pygame.display.get_init():  # Check if display was initialized
            print("Could not initialize display")
            return

        display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Classic - Demo - By Giuxpp")
        clock = pygame.time.Clock()
        # Initialize textures once
        init_textures()

        while True:  # Main game loop for restarts
            # Reset game state for each new game
            game_over = False
            # Initial snake: list of positions (classic movement)
            start_pos = ((WIDTH - SIDE) // 2 // SIDE * SIDE, (HEIGHT - SIDE) // 2 // SIDE * SIDE)
            snake = [start_pos]  # HEAD
            direction = RIGHT
            move_counter = 0  # Always increments, controls movement interval
            # Store the path of the head
            path = [snake[0]]
            # Generate blocks, forbid initial snake position
            blocks = generate_blocks(N_BLOCKS, forbidden={start_pos})
            for block in blocks:
                init_block(block)
            running = True
            score = 0  # Initialize score

            # Track the current direction for preventing 180-degree turns
            direction_manager = DirectionManager(direction)

            while running:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        new_direction = None
                        if event.key == pygame.K_UP:
                            new_direction = UP
                        elif event.key == pygame.K_DOWN:
                            new_direction = DOWN
                        elif event.key == pygame.K_LEFT:
                            new_direction = LEFT
                        elif event.key == pygame.K_RIGHT:
                            new_direction = RIGHT

                        # Queue the new direction if valid
                        if new_direction:
                            direction_manager.queue_direction(new_direction)

                if not game_over:
                    move_counter += 1
                    if move_counter > SNAKE_MOVE_INTERVAL:
                        move_counter = 0
                        # Get the next direction from the manager
                        direction = direction_manager.get_next_direction()
                        # Move snake: insert new head, pop tail
                        new_head = (snake[0][0] + direction[0]*STEP, snake[0][1] + direction[1]*STEP)
                        snake.insert(0, new_head)
                        snake.pop()
                        path.insert(0, new_head)
                        if len(path) > 1000:
                            path = path[:1000]
                        # Check for border collision (HEAD only)
                        hx, hy = snake[0]
                        if hx < 0 or hx + SIDE > WIDTH or hy < 0 or hy + SIDE > HEIGHT:
                            game_over = True

                        # Only check body collision when moving
                        # Check for collision with own body (skip the head)
                        head_pos = snake[0]
                        # Skip the first element (head) and check only against actual snake body
                        for i in range(1, len(snake)):
                            # Only check against actual snake body segments
                            if head_pos == snake[i]:
                                game_over = True
                                break

                    # Check collision with blocks (using position matrix)
                    tail_pos = snake[-1]
                    head_pos = snake[0]
                    for block in blocks:
                        # HIT: Head covers block
                        if not block['hit'] and head_pos == block['pos']:
                            block['color'] = SNAKE_COLOR
                            block['hit'] = True
                        # ATTACH: Tail covers block (after hit)
                        if block['hit'] and not block['attached'] and tail_pos == block['pos']:
                            block['ready_to_attach'] = True
                        # Start following path when tail no longer overlaps
                        if block.get('ready_to_attach') and not block['attached'] and tail_pos != block['pos']:
                            block['attached'] = True
                            # Find the closest path index to the block's current position
                            min_idx = 0
                            block_x, block_y = block['pos']
                            min_dist = float('inf')
                            for idx, pos in enumerate(path):
                                # Use distance squared to avoid unnecessary sqrt operations
                                dist_sq = (pos[0] - block_x) ** 2 + (pos[1] - block_y) ** 2
                                if dist_sq < min_dist:
                                    min_dist = dist_sq
                                    min_idx = idx
                            block['path_index'] = min_idx
                    # Move attached blocks along the path at the same speed as the snake
                    blocks_to_remove = []
                    for block in blocks:
                        if block['attached'] and block['path_index'] is not None:
                            if block['path_index'] > 0:
                                block['pos'] = path[block['path_index']]
                                block['path_index'] -= 1  # Move at the same rate as the snake
                            else:
                                block['pos'] = path[0]
                        # Attach to snake if it overlaps with TAIL
                        if block['attached'] and tail_pos == block['pos']:
                            block['attached'] = False
                            block['hit'] = False
                            block['ready_to_attach'] = False
                            # No need to set block color here since we're appending to snake and the snake drawing logic handles coloring
                            snake.append(block['pos'])
                            score += 1
                            blocks_to_remove.append(block)
                            # Generate a new block in a random position (matrix-aligned)
                            forbidden = set(seg for seg in snake) | set(b['pos'] for b in blocks)
                            new_block = generate_single_block(forbidden=forbidden)
                            if new_block:
                                init_block(new_block)
                                blocks.append(new_block)
                    # Remove attached blocks from the list to prevent duplicates
                    for block in blocks_to_remove:
                        blocks.remove(block)
                # Clear screen
                display.fill(BLACK)
                # Draw blocks
                for block in blocks:
                    bx, by = block['pos']
                    draw_block(display, bx, by, block['color'])
                if not game_over:
                    # Draw snake (all segments, HEAD and TAIL colored differently)
                    for i, pos in enumerate(snake):
                        if i == 0:
                            draw_block(display, pos[0], pos[1], SNAKE_HEAD_COLOR)  # HEAD
                        elif i == len(snake) - 1 and len(snake) > 1:
                            # Calculate tail rotation based on direction from previous segment
                            # get_direction_angle now returns the correct angle for the tail to point away from the snake
                            tail_angle = get_direction_angle(snake[-1], snake[-2])
                            draw_block(display, pos[0], pos[1], SNAKE_TAIL_COLOR, rotation=tail_angle)  # TAIL
                        else:
                            draw_block(display, pos[0], pos[1], SNAKE_COLOR)
                else:
                    restart = show_game_over(display, score)
                    if restart:
                        break
                    else:
                        return
                # Draw score label in upper right corner
                draw_score_label(display, score)
                pygame.display.flip()
    except Exception as e:
        print(f"Game error: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pygame.quit()
        sys.exit()
