import pygame
from utils.textures import create_gradient_dot_texture, create_hen_texture, create_apple_texture, create_rabbit_texture
from config import SIDE

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

    def handle_collision(self):
        """
        Handle collision with the snake.
        Returns:
            int: Score increase from the collision.
        """
        return 0

class HenBlock(Block):
    def __init__(self, pos):
        """
        Initialize a HenBlock with position.
        Args:
            pos (tuple): Position of the block (x, y).
        Returns:
            None
        """
        super().__init__(pos, (220, 220, 60))  # Default block color

    def update_texture(self):
        """
        Override update_texture in HenBlock to use create_hen_texture.
        Returns:
            None
        """
        if not self.texture:
            self.texture = create_rabbit_texture(SIDE)

    def handle_collision(self, snake=None):
        """
        Handle collision with the snake.
        Args:
            snake (object, optional): The snake object. Defaults to None.
        Returns:
            int: Score increase from the collision.
        """
        return 1
