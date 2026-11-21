
import pygame
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    """A bullet fired downward by an alien."""

    def __init__(self, ai_game, alien):
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.color = self.settings.alien_bullet_color

        self.rect = pygame.Rect(
            0,
            0,
            self.settings.alien_bullet_width,
            self.settings.alien_bullet_height
        )

        self.rect.midtop = alien.rect.midbottom
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet downward."""
        self.y += self.settings.alien_bullet_speed
        self.rect.y = int(self.y)

    def draw_bullet(self):
        """Draw the alien bullet."""
        pygame.draw.rect(
            self.screen,
            self.color,
            self.rect
        )
