import pygame
import random

# Global textures
BLOCK_TEXTURE = None
SNAKE_TEXTURE = None
SNAKE_HEAD_TEXTURE = None
SNAKE_TAIL_TEXTURE = None
BG_TEXTURE_LEVEL_1 = None  # Background texture
BG_TEXTURE_LEVEL_2 = None  # Background texture
BG_TEXTURE_LEVEL_3 = None  # Background texture

# === Texture Generation Functions ===
def create_gradient_dot_texture(color, size=30, dot_size=4):
    """
    Create a gradient texture with dots overlay.

    Args:
        color (tuple): Base color for the gradient (R, G, B).
        size (int): Size of the texture (width and height).
        dot_size (int): Size of the dots overlay.

    Returns:
        pygame.Surface: Generated texture with gradient and dots.
    """
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

    return texture

def create_serpent_long_thong_head_texture(color, size=30):
    """
    Create a special serpent head texture with scales, eyes, and a long tongue.

    Args:
        color (tuple): Base color for the head (R, G, B).
        size (int): Size of the texture (width and height).

    Returns:
        pygame.Surface: Generated texture for the serpent head.
    """
    texture = pygame.Surface((size, size), pygame.SRCALPHA)
    texture.fill((0, 0, 0, 0))  # Transparent background

    # Define trapezoid points
    top_width = size // 2
    height = size

    top_left = ((size - top_width) // 2, 0)
    top_right = ((size + top_width) // 2, 0)
    bottom_left = (0, height)
    bottom_right = (size, height)

    points = [top_left, top_right, bottom_right, bottom_left]

    # Draw trapezoid body
    pygame.draw.polygon(texture, color, points)

    # Add eyes (two glowing circles)
    eye_color = (255, 255, 0)  # Bright yellow eyes
    eye_size = size // 6
    eye_pos_left = (size // 4, size // 3)
    eye_pos_right = (3 * size // 4, size // 3)

    # Draw eye outlines (slightly larger)
    pygame.draw.circle(texture, (0, 0, 0), eye_pos_left, eye_size)
    pygame.draw.circle(texture, (0, 0, 0), eye_pos_right, eye_size)
    # Draw the actual eyes (smaller)
    pygame.draw.circle(texture, eye_color, eye_pos_left, eye_size - 1)
    pygame.draw.circle(texture, eye_color, eye_pos_right, eye_size - 1)
    # Add eye pupils (black)
    pygame.draw.circle(texture, (0, 0, 0), eye_pos_left, eye_size // 2)
    pygame.draw.circle(texture, (0, 0, 0), eye_pos_right, eye_size // 2)

    # Modify red tongue to be 3x larger
    tongue_color = (255, 0, 0)  # Bright red
    tongue_width = (size // 10) * 3
    tongue_height = (size // 6) * 3

    tongue_points = [
        (size // 2 - tongue_width, size - tongue_height),  # Left bottom
        (size // 2, size - tongue_height // 2),            # Middle peak
        (size // 2 + tongue_width, size - tongue_height),  # Right bottom
        (size // 2, size - tongue_height * 1.5)           # Top center
    ]

    pygame.draw.polygon(texture, tongue_color, tongue_points)

    return texture

def create_serpent_short_thong_head_texture(color, size=30):
    """
    Create a special serpent head texture with scales, eyes, and a short tongue.

    Args:
        color (tuple): Base color for the head (R, G, B).
        size (int): Size of the texture (width and height).

    Returns:
        pygame.Surface: Generated texture for the serpent head.
    """
    texture = pygame.Surface((size, size), pygame.SRCALPHA)
    texture.fill((0, 0, 0, 0))  # Transparent background

    # Define trapezoid points
    top_width = size // 2
    height = size

    top_left = ((size - top_width) // 2, 0)
    top_right = ((size + top_width) // 2, 0)
    bottom_left = (0, height)
    bottom_right = (size, height)

    points = [top_left, top_right, bottom_right, bottom_left]

    # Draw trapezoid body
    pygame.draw.polygon(texture, color, points)

    # Add eyes (two glowing circles)
    eye_color = (255, 255, 0)  # Bright yellow eyes
    eye_size = size // 6
    eye_pos_left = (size // 4, size // 3)
    eye_pos_right = (3 * size // 4, size // 3)

    # Draw eye outlines (slightly larger)
    pygame.draw.circle(texture, (0, 0, 0), eye_pos_left, eye_size)
    pygame.draw.circle(texture, (0, 0, 0), eye_pos_right, eye_size)
    # Draw the actual eyes (smaller)
    pygame.draw.circle(texture, eye_color, eye_pos_left, eye_size - 1)
    pygame.draw.circle(texture, eye_color, eye_pos_right, eye_size - 1)
    # Add eye pupils (black)
    pygame.draw.circle(texture, (0, 0, 0), eye_pos_left, eye_size // 2)
    pygame.draw.circle(texture, (0, 0, 0), eye_pos_right, eye_size // 2)

    # Add red tongue ("M" shape)
    tongue_color = (255, 0, 0)  # Bright red
    tongue_width = size // 10
    tongue_height = size // 6

    tongue_points = [
        (size // 2 - tongue_width, size - tongue_height),  # Left bottom
        (size // 2, size - tongue_height // 2),            # Middle peak
        (size // 2 + tongue_width, size - tongue_height),  # Right bottom
        (size // 2, size - tongue_height * 1.5)           # Top center
    ]

    pygame.draw.polygon(texture, tongue_color, tongue_points)

    return texture


def create_serpent_head_texture_closed_eyes(color, size=30):
    """
    Create a special serpent head texture with scales and closed eyes.

    Args:
        color (tuple): Base color for the head (R, G, B).
        size (int): Size of the texture (width and height).

    Returns:
        pygame.Surface: Generated texture for the serpent head with closed eyes.
    """
    texture = pygame.Surface((size, size), pygame.SRCALPHA)
    texture.fill(color)  # Base color

    # Create darker shade for details
    darker = (max(0, int(color[0] * 0.6)),
             max(0, int(color[1] * 0.6)),
             max(0, int(color[2] * 0.6)))

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

    # Add closed eyes (two horizontal lines)
    eye_color = (0, 0, 0)  # Black for closed eyes
    eye_size = size // 6
    eye_pos_left = (size // 4, size // 3)
    eye_pos_right = (3 * size // 4, size // 3)

    # Draw closed eyes as horizontal lines
    pygame.draw.line(texture, eye_color, (eye_pos_left[0] - eye_size//2, eye_pos_left[1]),
                     (eye_pos_left[0] + eye_size//2, eye_pos_left[1]), 2)
    pygame.draw.line(texture, eye_color, (eye_pos_right[0] - eye_size//2, eye_pos_right[1]),
                     (eye_pos_right[0] + eye_size//2, eye_pos_right[1]), 2)

    return texture

def create_snake_tail_texture(color, size=30):
    """
    Create a special snake tail texture with a tapered, forked end.

    Args:
        color (tuple): Base color for the tail (R, G, B).
        size (int): Size of the texture (width and height).

    Returns:
        pygame.Surface: Generated texture for the snake tail.
    """
    texture = pygame.Surface((size, size), pygame.SRCALPHA)

    # Create darker shade for details
    darker = (max(0, int(color[0] * 0.7)),
             max(0, int(color[1] * 0.7)),
             max(0, int(color[2] * 0.7)))

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

def create_dirt_texture_level_1(size=30):
    """
    Create a grainy blue dirt texture for the background.

    Args:
        size (int): Size of the texture (width and height).

    Returns:
        pygame.Surface: Generated texture for the dirt background.
    """
    # Base blue color
    base_color = (70, 130, 180)  # Steel blue
    texture = pygame.Surface((size, size), pygame.SRCALPHA)

    # Create variations of blue for the grainy effect
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

def create_dirt_texture_level_2(size=30):
    """
    Create a grainy brown dirt texture for the background.

    Args:
        size (int): Size of the texture (width and height).

    Returns:
        pygame.Surface: Generated texture for the dirt background.
    """
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

def create_dirt_texture_level_3(size=30):
    """
    Create a grainy red dirt texture for the background.

    Args:
        size (int): Size of the texture (width and height).

    Returns:
        pygame.Surface: Generated texture for the dirt background.
    """
    # Base red color
    base_color = (178, 34, 34)  # Firebrick red
    texture = pygame.Surface((size, size), pygame.SRCALPHA)

    # Create variations of red for the grainy effect
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

# Updated create_hen_texture to remove current eyes and beak, add a new big beak at the bottom, and place two big eyes in the center.
def create_hen_texture(size=30):
    """
    Create a texture resembling a hen with a circular figure, eyes, and a bigger beak.

    Args:
        size (int): Size of the texture (width and height).

    Returns:
        pygame.Surface: Generated texture for the hen block.
    """
    texture = pygame.Surface((size, size), pygame.SRCALPHA)

    # Draw hen body (circle)
    body_color = (255, 200, 0)  # Yellow-orange for body
    pygame.draw.circle(texture, body_color, (size // 2, size // 2), size // 2)

    # Draw bigger beak (larger triangle at the bottom)
    beak_color = (255, 100, 0)  # Red-orange for beak
    beak_points = [
        (size // 2, size - size // 6),  # Bottom point (lower)
        (size // 2 - size // 4, size - size // 3),  # Left point (wider)
        (size // 2 + size // 4, size - size // 3)   # Right point (wider)
    ]
    pygame.draw.polygon(texture, beak_color, beak_points)

    # Draw small eyes (centered circles)
    eye_size = size // 10

    # Calculate eye positions
    eye_pos_left = (size // 2 - size // 5, size // 3)
    eye_pos_right = (size // 2 + size // 5, size // 3)

    # Draw eye outlines (slightly larger)
    pygame.draw.circle(texture, (0, 0, 0), eye_pos_left, eye_size)
    pygame.draw.circle(texture, (0, 0, 0), eye_pos_right, eye_size)
    # Draw the actual eyes (smaller)
    pygame.draw.circle(texture, (255, 255, 255), eye_pos_left, eye_size - 2)
    pygame.draw.circle(texture, (255, 255, 255), eye_pos_right, eye_size - 2)
    # Add eye pupils (black)
    pygame.draw.circle(texture, (0, 0, 0), eye_pos_left, eye_size // 3)
    pygame.draw.circle(texture, (0, 0, 0), eye_pos_right, eye_size // 3)

    return texture
