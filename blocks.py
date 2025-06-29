import pygame
from textures import create_gradient_dot_texture

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
        return self._color if self._color is not None else (220, 220, 60)  # Default block color

    def update_texture(self):
        """Update the block's texture based on its color"""
        if not self.texture:
            self.texture = create_gradient_dot_texture(self.color)

    def draw(self, display):
        """Draw the block on the display"""
        if not self.texture:
            self.update_texture()
        x, y = self.pos
        display.blit(self.texture, (x, y))

    def handle_collision(self):
        """Handle collision with snake. Returns score increase."""
        return 0

class RegularBlock(Block):
    def __init__(self, pos):
        super().__init__(pos, (220, 220, 60))  # Default block color

    def handle_collision(self, snake=None):
        """Regular blocks add 1 to score and make the snake grow"""
        return 1
