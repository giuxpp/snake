import pygame
import random
import sys

# === General Configuration Parameters ===
WIDTH, HEIGHT = 800, 600
SIDE = 30
STEP = SIDE  # All blocks move SIDE on every step
FPS = 15  # Increase FPS for smoother movement
SNAKE_MOVE_INTERVAL = 2  # Move the snake every 2 frames for classic speed
N_BLOCKS = 4
BLOCK_TOUCH_THRESHOLD = 0.5  # Fraction of overlap required to color the block (e.g., 0.5 for 50%)
COVERAGE_THRESHOLD = 1  # Fraction of block area that must be covered to count as a hit

# === Colors ===
RED = (255, 0, 0)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)

# === Shape Configuration Parameters ===
BLOCKS_COLOR = CYAN
SNAKE_COLOR = RED

# === Directions ===
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

SNAKE_HEAD = 0  # Index of the snake's head in the list
SNAKE_TAIL = -1  # Index of the snake's tail in the list

game_over = False  # Global variable to track game state
BLOCK_VELOCITY = STEP  # All blocks move at the same speed as the snake


# Generate random positions for blocks
def generate_blocks(n, forbidden=None):
    blocks = []
    cols = WIDTH // SIDE
    rows = HEIGHT // SIDE
    positions = set()
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
        positions.add(pos)
    return blocks

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

def draw_block(screen, x, y, color=SNAKE_COLOR):
    pygame.draw.rect(screen, color, (x, y, SIDE, SIDE))


draw_snake_init = draw_block

def show_game_over(screen, score):
    font = pygame.font.SysFont(None, 100)
    text = font.render(f"GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)
    font2 = pygame.font.SysFont(None, 60)
    score_text = font2.render(f"Score: {score}", True, (255, 255, 255))  # White color for score
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    screen.blit(score_text, score_rect)
    pygame.display.flip()
    # Wait for user to close the window or press ENTER to restart
    waiting = True
    restart = False
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    restart = True
                    waiting = False
        pygame.time.wait(50)
    return restart

def rect_overlap_fraction(rect1, rect2):
    # rect: (x, y, size, size)
    # Now: if the snake covers the center of the block, return 1, else 0
    x1, y1, s1, _ = rect1
    x2, y2, s2, _ = rect2
    center_x = x2 + s2 // 2
    center_y = y2 + s2 // 2
    if x1 <= center_x < x1 + s1 and y1 <= center_y < y1 + s1:
        return 1
    return 0

def area_coverage(snake_rect, block_rect):
    # Returns the fraction of the block's area covered by the snake
    sx, sy, sw, sh = snake_rect
    bx, by, bw, bh = block_rect
    x_overlap = max(0, min(sx + sw, bx + bw) - max(sx, bx))
    y_overlap = max(0, min(sy + sh, by + bh) - max(sy, by))
    overlap_area = x_overlap * y_overlap
    block_area = bw * bh
    if block_area == 0:
        return 0
    return overlap_area / block_area

def centers_separated_by_side(snake_pos, block_pos):
    sx, sy = snake_pos
    bx, by = block_pos
    snake_center = (sx + SIDE // 2, sy + SIDE // 2)
    block_center = (bx + SIDE // 2, by + SIDE // 2)
    dx = snake_center[0] - block_center[0]
    dy = snake_center[1] - block_center[1]
    distance = (dx ** 2 + dy ** 2) ** 0.5
    return distance >= SIDE


# === Snake Definitions ===
# The snake is a chain (list) of blocks. The first is the HEAD, the last is the TAIL.


def draw_score_label(screen, score):
    font = pygame.font.SysFont(None, 40)
    text = font.render(f"Score: {score}", True, (255, 255, 0))
    text_rect = text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(text, text_rect)

def main():
    global game_over
    while True:
        # Initialization
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Movement Example")
        clock = pygame.time.Clock()
        game_over = False
        # Initial snake: list of positions (classic movement)
        start_pos = ((WIDTH - SIDE) // 2 // SIDE * SIDE, (HEIGHT - SIDE) // 2 // SIDE * SIDE)
        snake = [start_pos]  # HEAD
        direction = RIGHT
        move_pending = False
        move_counter = 0
        # Store the path of the head
        path = [snake[0]]
        # Generate blocks, forbid initial snake position
        blocks = generate_blocks(N_BLOCKS, forbidden={start_pos})
        for block in blocks:
            block['hit'] = False
            block['moving'] = False
            block['move_dir'] = (0, 0)
            block['attached'] = False
            block['path_index'] = None
            block['start_path_index'] = None  # To track where to start following
        running = True
        score = 0  # Initialize score
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and not game_over:
                    if event.key == pygame.K_UP and direction != DOWN:
                        direction = UP
                        move_pending = True
                    elif event.key == pygame.K_DOWN and direction != UP:
                        direction = DOWN
                        move_pending = True
                    elif event.key == pygame.K_LEFT and direction != RIGHT:
                        direction = LEFT
                        move_pending = True
                    elif event.key == pygame.K_RIGHT and direction != LEFT:
                        direction = RIGHT
                        move_pending = True
            if not game_over and move_pending:
                move_counter += 1
                if move_counter >= SNAKE_MOVE_INTERVAL:
                    move_counter = 0
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
                    # Check collision with blocks (using area coverage)
                    head_rect = (hx, hy, SIDE, SIDE)
                    tail_rect = (snake[-1][0], snake[-1][1], SIDE, SIDE)
                    for block in blocks:
                        block_rect = (block['pos'][0], block['pos'][1], SIDE, SIDE)
                        # HIT: Head covers block
                        if not block['hit'] and area_coverage(head_rect, block_rect) >= COVERAGE_THRESHOLD:
                            block['color'] = SNAKE_COLOR
                            block['hit'] = True
                        # ATTACH: Tail covers block (after hit)
                        if block['hit'] and not block['attached'] and area_coverage(tail_rect, block_rect) >= COVERAGE_THRESHOLD:
                            block['ready_to_attach'] = True
                        # Start following path when tail no longer overlaps (0% coverage)
                        if block.get('ready_to_attach') and not block['attached'] and area_coverage(tail_rect, block_rect) == 0:
                            block['attached'] = True
                            # Find the closest path index to the block's current position
                            min_dist = float('inf')
                            min_idx = 0
                            for idx, pos in enumerate(path):
                                dist = ((pos[0] - block['pos'][0]) ** 2 + (pos[1] - block['pos'][1]) ** 2) ** 0.5
                                if dist < min_dist:
                                    min_dist = dist
                                    min_idx = idx
                            block['path_index'] = min_idx
                            block['start_path_index'] = min_idx
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
                        block_rect = (block['pos'][0], block['pos'][1], SIDE, SIDE)
                        overlap = area_coverage(tail_rect, block_rect)
                        if block['attached'] and overlap >= COVERAGE_THRESHOLD:
                            block['attached'] = False
                            block['hit'] = False
                            block['ready_to_attach'] = False
                            block['color'] = (100, 100, 255)  # TAIL color
                            snake.append(block['pos'])
                            score += 1
                            blocks_to_remove.append(block)
                            # Generate a new block in a random position (matrix-aligned)
                            forbidden = set([seg for seg in snake]) | set([b['pos'] for b in blocks])
                            new_block = generate_single_block(forbidden=forbidden)
                            if new_block:
                                # Initialize all required state keys for the new block
                                new_block['hit'] = False
                                new_block['moving'] = False
                                new_block['move_dir'] = (0, 0)
                                new_block['attached'] = False
                                new_block['path_index'] = None
                                new_block['start_path_index'] = None
                                new_block['ready_to_attach'] = False
                                blocks.append(new_block)
                    # Remove attached blocks from the list to prevent duplicates
                    for block in blocks_to_remove:
                        blocks.remove(block)
            # Clear screen
            screen.fill(BLACK)
            # Draw blocks
            for block in blocks:
                bx, by = block['pos']
                draw_block(screen, bx, by, block['color'])
            if not game_over:
                # Draw snake (all segments, HEAD and TAIL colored differently)
                for i, pos in enumerate(snake):
                    if i == 0:
                        draw_block(screen, pos[0], pos[1], (255, 100, 100))  # HEAD
                    elif i == len(snake) - 1:
                        draw_block(screen, pos[0], pos[1], (100, 100, 255))  # TAIL
                    else:
                        draw_block(screen, pos[0], pos[1], SNAKE_COLOR)
            else:
                restart = show_game_over(screen, score)
                if restart:
                    break
                else:
                    return
            # Draw score label in upper right corner
            draw_score_label(screen, score)
            pygame.display.flip()
        # If we reach here, the user pressed ENTER to restart


if __name__ == "__main__":
    main()
