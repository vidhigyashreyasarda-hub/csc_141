
import pygame
from pygame.sprite import Sprite
from pathlib import Path


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image using the correct file path.
        # This works regardless of the working directory.
        image_path = (
            Path(__file__).resolve().parent
            / 'images'
            / 'alien.bmp'
        )

        self.image = pygame.image.load(str(image_path))

        # Resize the alien image.
        self.image = pygame.transform.scale(
            self.image, (80, 80)
        )

        self.rect = self.image.get_rect()

        # Start each new alien near the top left.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if the alien is at the screen edge."""

        screen_rect = self.screen.get_rect()

        if (
            self.rect.right >= screen_rect.right
            or self.rect.left <= 0
        ):
            return True

        return False

    def update(self):
        """Move the alien right or left."""

        self.x += (
            self.settings.alien_speed
            * self.settings.fleet_direction
        )

        self.rect.x = int(self.x)
