
import pygame
from pygame.sprite import Sprite
from pathlib import Path


class Ship(Sprite):
    """Manage the player's ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image using an absolute path.
        # This works regardless of the working directory.
        image_path = (
            Path(__file__).resolve().parent
            / 'images'
            / 'ship.bmp'
        )

        self.image = pygame.image.load(str(image_path))

        # Resize the ship image.
        self.image = pygame.transform.scale(
            self.image, (100, 100)
        )

        self.rect = self.image.get_rect()

        # Start the ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store the ship's exact horizontal position.
        self.x = float(self.rect.x)

        # Movement flags.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on movement flags."""

        if self.moving_right:
            if self.rect.right < self.screen_rect.right:
                self.x += self.settings.ship_speed

        if self.moving_left:
            if self.rect.left > 0:
                self.x -= self.settings.ship_speed

        # Keep the ship within the screen boundaries.
        self.x = max(
            0,
            min(
                self.x,
                self.screen_rect.width - self.rect.width
            )
        )

        self.rect.x = int(self.x)

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship at the bottom of the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        # Reset movement flags.
        self.moving_right = False
        self.moving_left = False
