import pygame
from utils.textures import create_gradient_dot_texture, create_hen_texture, create_apple_texture, create_rabbit_texture
from config import SIDE
from config import game_config

# === Classes ===
class Block:
    def __init__(self, pos, color=None):
        """
        Initialize a block with position and optional color.
        Args:
            pos (tuple): Position of the block (x, y).
            color (tuple, optional): Color of the block (R, G, B). Defaults to None.
        Attributes:
            hit (bool): Whether the block has been hit.
            attached (bool): Whether the block is attached to the snake.
            path_index (int): Index in the snake's path.
            ready_to_attach (bool): Whether the block is ready to attach.
            texture (pygame.Surface): Texture of the block.
        """
        self.pos = pos
        self._color = color
        self.hit = False
        self.attached = False
        self.path_index = None
        self.ready_to_attach = False
        self.texture = None

    @property
    def color(self):
        """
        Get the color of the block.
        Returns:
            tuple: Color of the block (R, G, B).
        """
        return self._color if self._color is not None else (220, 220, 60)  # Default block color

    def update_texture(self):
        """
        Update the block's texture based on its color.
        Returns:
            None
        """
        if not self.texture:
            self.texture = create_gradient_dot_texture(self.color)

    def draw(self, display):
        """
        Draw the block on the display.
        Args:
            display (pygame.Surface): The game display surface.
        Returns:
            None
        """
        if not self.texture:
            self.update_texture()
            if not self.texture:  # Fallback to a default texture
                self.texture = pygame.Surface((SIDE, SIDE))
                self.texture.fill(self.color)
        x, y = self.pos
        display.blit(self.texture, (x, y))

class HenBlock(Block):
    def __init__(self, pos):
        super().__init__(pos, (220, 220, 60))  # Default block color

    def update_texture(self):
        """
        Override update_texture in HenBlock to use create_hen_texture.
        """
        if not self.texture:
            level = game_config.get("level", 1)
            if level == "medium":
                self.texture = create_hen_texture(SIDE)
            elif level == "hard":
                self.texture = create_rabbit_texture(SIDE)
            else:
                self.texture = create_apple_texture(SIDE)

class AppleBlock(Block):
    def __init__(self, pos):
        super().__init__(pos, (220, 60, 60))  # Default block color

    def update_texture(self):
        """
        Override update_texture in AppleBlock to use create_apple_texture.
        """
        if not self.texture:
            self.texture = create_apple_texture(SIDE)

class RabbitBlock(Block):
    def __init__(self, pos):
        super().__init__(pos, (60, 220, 60))  # Default block color

    def update_texture(self):
        """
        Override update_texture in RabbitBlock to use create_rabbit_texture.
        """
        if not self.texture:
            self.texture = create_rabbit_texture(SIDE)