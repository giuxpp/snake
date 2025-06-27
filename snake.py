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

def draw_block(screen, x, y, color=SNAKE_COLOR):
    pygame.draw.rect(screen, color, (x, y, SIDE, SIDE))

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

def main():
    global game_over
    while True:
        # Initialization
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Classic - Demo - By Giuxpp")
        clock = pygame.time.Clock()
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
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and not game_over:
                    if event.key == pygame.K_UP and direction != DOWN:
                        direction = UP
                    elif event.key == pygame.K_DOWN and direction != UP:
                        direction = DOWN
                    elif event.key == pygame.K_LEFT and direction != RIGHT:
                        direction = LEFT
                    elif event.key == pygame.K_RIGHT and direction != LEFT:
                        direction = RIGHT
            if not game_over:
                move_counter += 1
                if move_counter > SNAKE_MOVE_INTERVAL:
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
                            block['color'] = (100, 100, 255)  # TAIL color
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
