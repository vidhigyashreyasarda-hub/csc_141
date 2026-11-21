import pygame.font


class Button:
    """A class to create a button for the game."""

    def __init__(self, ai_game, msg):
        """Initialize button attributes."""

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set button dimensions and properties.
        self.width = 200
        self.height = 50

        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)

        self.font = pygame.font.SysFont(None, 48)

        # Create the button rectangle.
        self.rect = pygame.Rect(
            0, 0, self.width, self.height
        )

        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn the message into a rendered image."""

        self.msg_image = self.font.render(
            msg, True, self.text_color,
            self.button_color
        )

        self.msg_image_rect = self.msg_image.get_rect()

        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw the button on the screen."""

        self.screen.fill(self.button_color, self.rect)

        self.screen.blit(
            self.msg_image,
            self.msg_image_rect
        )