
import sys
import pygame


class TargetPractice:
    """A game where the player shoots at a moving target."""

    def __init__(self):
        pygame.init()

        self.screen_width = 1200
        self.screen_height = 800

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )

        pygame.display.set_caption("14-2 Target Practice")

        self.clock = pygame.time.Clock()

        # Colors
        self.bg_color = (230, 230, 230)
        self.ship_color = (30, 100, 200)
        self.target_color = (200, 50, 50)
        self.bullet_color = (40, 40, 40)

        # Ship settings
        self.ship_width = 60
        self.ship_height = 60
        self.ship_speed = 5

        self.ship = pygame.Rect(
            40,
            self.screen_height // 2,
            self.ship_width,
            self.ship_height
        )

        self.moving_up = False
        self.moving_down = False

        # Target settings
        self.target_width = 40
        self.target_height = 150
        self.target_speed = 3
        self.target_direction = 1

        self.target = pygame.Rect(
            self.screen_width - 60,
            self.screen_height // 2 - 75,
            self.target_width,
            self.target_height
        )

        # Bullet settings
        self.bullet_width = 20
        self.bullet_height = 5
        self.bullet_speed = 8
        self.bullets = []

        # Game statistics
        self.misses = 0
        self.misses_allowed = 3
        self.hits = 0
        self.game_active = False

        # Play button
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 36)

        self.play_button = pygame.Rect(
            0, 0, 200, 60
        )
        self.play_button.center = (
            self.screen_width // 2,
            self.screen_height // 2
        )

    def run_game(self):
        """Start the main game loop."""
        while True:
            self._check_events()

            if self.game_active:
                self._update_ship()
                self._update_target()
                self._update_bullets()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keyboard and mouse events."""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    self.moving_up = True

                elif event.key == pygame.K_DOWN:
                    self.moving_down = True

                elif event.key == pygame.K_SPACE:
                    if self.game_active:
                        self._fire_bullet()

                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_UP:
                    self.moving_up = False

                elif event.key == pygame.K_DOWN:
                    self.moving_down = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_active:
                    if self.play_button.collidepoint(event.pos):
                        self._start_game()

    def _start_game(self):
        """Start a new game and reset statistics."""
        self.game_active = True

        self.misses = 0
        self.hits = 0

        self.bullets.clear()

        self.ship.centery = self.screen_height // 2
        self.target.centery = self.screen_height // 2

        self.target_direction = 1

        self.moving_up = False
        self.moving_down = False

    def _update_ship(self):
        """Move the ship up and down."""
        if self.moving_up and self.ship.top > 0:
            self.ship.y -= self.ship_speed

        if (
            self.moving_down
            and self.ship.bottom < self.screen_height
        ):
            self.ship.y += self.ship_speed

    def _update_target(self):
        """Move the target up and down."""
        self.target.y += (
            self.target_speed * self.target_direction
        )

        if self.target.bottom >= self.screen_height:
            self.target.bottom = self.screen_height
            self.target_direction = -1

        elif self.target.top <= 0:
            self.target.top = 0
            self.target_direction = 1

    def _fire_bullet(self):
        """Create a bullet from the ship."""
        bullet = pygame.Rect(
            self.ship.right,
            self.ship.centery - self.bullet_height // 2,
            self.bullet_width,
            self.bullet_height
        )

        self.bullets.append(bullet)

    def _update_bullets(self):
        """Move bullets and check hits and misses."""
        for bullet in self.bullets[:]:

            bullet.x += self.bullet_speed

            # Check whether the bullet hits the target.
            if bullet.colliderect(self.target):
                self.hits += 1
                self.bullets.remove(bullet)

            # Check whether the bullet misses.
            elif bullet.left >= self.screen_width:
                self.misses += 1
                self.bullets.remove(bullet)

                # End the game after three misses.
                if self.misses >= self.misses_allowed:
                    self.game_active = False
                    self.moving_up = False
                    self.moving_down = False
                    break

    def _draw_ship(self):
        """Draw a ship pointing toward the target."""
        points = [
            (self.ship.left, self.ship.top),
            (self.ship.right, self.ship.centery),
            (self.ship.left, self.ship.bottom)
        ]

        pygame.draw.polygon(
            self.screen,
            self.ship_color,
            points
        )

    def _draw_play_button(self):
        """Draw the Play button."""
        pygame.draw.rect(
            self.screen,
            (0, 150, 0),
            self.play_button
        )

        text = self.font.render(
            "Play",
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(
            center=self.play_button.center
        )

        self.screen.blit(text, text_rect)

    def _draw_score(self):
        """Display hits and misses."""
        score_text = (
            f"Hits: {self.hits}    "
            f"Misses: {self.misses}/3"
        )

        score_image = self.small_font.render(
            score_text,
            True,
            (30, 30, 30)
        )

        self.screen.blit(score_image, (20, 20))

    def _update_screen(self):
        """Draw the game screen."""
        self.screen.fill(self.bg_color)

        # Draw the ship.
        self._draw_ship()

        # Draw the moving target.
        pygame.draw.rect(
            self.screen,
            self.target_color,
            self.target
        )

        # Draw bullets.
        for bullet in self.bullets:
            pygame.draw.rect(
                self.screen,
                self.bullet_color,
                bullet
            )

        # Display score.
        self._draw_score()

        # Display Play button when game is inactive.
        if not self.game_active:
            self._draw_play_button()

        pygame.display.flip()


if __name__ == "__main__":
    game = TargetPractice()
    game.run_game()
