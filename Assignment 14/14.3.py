
import sys
import pygame


class TargetPractice:
    """A target practice game with increasing difficulty."""

    def __init__(self):
        pygame.init()

        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption("14-3 Challenging Target Practice")

        self.clock = pygame.time.Clock()
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 5
        self.ship_color = (30, 100, 200)
        self.ship = pygame.Rect(40, 370, 60, 60)
        self.moving_up = False
        self.moving_down = False

        # Target settings
        self.target_color = (200, 50, 50)
        self.initial_target_speed = 3
        self.target_speed = self.initial_target_speed
        self.speedup_scale = 1.15
        self.target_direction = 1

        self.target = pygame.Rect(
            self.screen_width - 60,
            325,
            40,
            150
        )

        # Bullet settings
        self.bullet_color = (40, 40, 40)
        self.bullet_speed = 8
        self.bullets = []

        # Game statistics
        self.hits = 0
        self.misses = 0
        self.misses_allowed = 3
        self.game_active = False

        # Fonts and Play button
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 36)

        self.play_button = pygame.Rect(0, 0, 200, 60)
        self.play_button.center = self.screen.get_rect().center

    def run_game(self):
        """Run the game."""
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
        """Reset the game to its original settings."""
        self.game_active = True

        self.hits = 0
        self.misses = 0
        self.bullets.clear()

        # Reset target speed for each new game.
        self.target_speed = self.initial_target_speed
        self.target_direction = 1

        self.ship.centery = self.screen_height // 2
        self.target.centery = self.screen_height // 2

        self.moving_up = False
        self.moving_down = False

    def _update_ship(self):
        """Move the ship vertically."""
        if self.moving_up:
            self.ship.y -= self.ship_speed

        if self.moving_down:
            self.ship.y += self.ship_speed

        self.ship.top = max(0, self.ship.top)
        self.ship.bottom = min(
            self.screen_height, self.ship.bottom
        )

    def _update_target(self):
        """Move the target and reverse at screen edges."""
        self.target.y += round(
            self.target_speed * self.target_direction
        )

        if self.target.bottom >= self.screen_height:
            self.target.bottom = self.screen_height
            self.target_direction = -1

        elif self.target.top <= 0:
            self.target.top = 0
            self.target_direction = 1

    def _fire_bullet(self):
        """Fire a bullet toward the target."""
        bullet = pygame.Rect(
            self.ship.right,
            self.ship.centery - 2,
            20,
            5
        )
        self.bullets.append(bullet)

    def _update_bullets(self):
        """Move bullets and detect hits and misses."""
        for bullet in self.bullets[:]:
            bullet.x += self.bullet_speed

            if bullet.colliderect(self.target):
                self.hits += 1
                self.bullets.remove(bullet)

                # Exercise 14-3:
                # Increase target speed after each hit.
                self.target_speed *= self.speedup_scale

            elif bullet.left >= self.screen_width:
                self.misses += 1
                self.bullets.remove(bullet)

                if self.misses >= self.misses_allowed:
                    self.game_active = False
                    self.moving_up = False
                    self.moving_down = False
                    break

    def _draw_ship(self):
        """Draw the ship pointing right."""
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
            "Play", True, (255, 255, 255)
        )

        text_rect = text.get_rect(
            center=self.play_button.center
        )
        self.screen.blit(text, text_rect)

    def _draw_score(self):
        """Display hits, misses, and target speed."""
        score_text = (
            f"Hits: {self.hits}    "
            f"Misses: {self.misses}/3    "
            f"Target Speed: {self.target_speed:.1f}"
        )

        score_image = self.small_font.render(
            score_text,
            True,
            (30, 30, 30)
        )
        self.screen.blit(score_image, (20, 20))

    def _update_screen(self):
        """Draw all game objects."""
        self.screen.fill(self.bg_color)

        self._draw_ship()

        pygame.draw.rect(
            self.screen,
            self.target_color,
            self.target
        )

        for bullet in self.bullets:
            pygame.draw.rect(
                self.screen,
                self.bullet_color,
                bullet
            )

        self._draw_score()

        if not self.game_active:
            self._draw_play_button()

        pygame.display.flip()


if __name__ == "__main__":
    game = TargetPractice()
    game.run_game()
