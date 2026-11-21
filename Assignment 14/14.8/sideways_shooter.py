
import sys
import random

import pygame


class SidewaysShooter:
    """A game where the player shoots aliens moving from right to left."""

    def __init__(self):
        pygame.init()

        self.width = 1200
        self.height = 800

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )
        pygame.display.set_caption(
            "14-8 Sideways Shooter"
        )

        self.clock = pygame.time.Clock()
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship = pygame.Rect(50, 370, 55, 60)
        self.ship_speed = 5
        self.moving_up = False
        self.moving_down = False

        # Bullet settings
        self.bullets = []
        self.bullet_speed = 9
        self.bullet_limit = 5

        # Alien settings
        self.aliens = []
        self.alien_width = 45
        self.alien_height = 45
        self.alien_speed = 2
        self.alien_spawn_interval = 1000
        self.last_spawn = 0

        # Game statistics
        self.score = 0
        self.level = 1
        self.lives = 3
        self.game_active = False

        # Fonts
        self.font = pygame.font.SysFont(None, 45)
        self.small_font = pygame.font.SysFont(None, 32)

        # Play button
        self.play_button = pygame.Rect(
            0, 0, 200, 65
        )
        self.play_button.center = (
            self.width // 2,
            self.height // 2
        )

    def run_game(self):
        """Run the game loop."""
        while True:
            self._check_events()

            if self.game_active:
                self._update_ship()
                self._update_bullets()
                self._update_aliens()
                self._spawn_aliens()

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

                elif event.key == pygame.K_p:
                    if not self.game_active:
                        self._start_game()

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
        """Reset the game and start playing."""
        self.score = 0
        self.level = 1
        self.lives = 3

        self.alien_speed = 2
        self.alien_spawn_interval = 1000

        self.bullets.clear()
        self.aliens.clear()

        self.ship.centery = self.height // 2

        self.moving_up = False
        self.moving_down = False

        self.last_spawn = pygame.time.get_ticks()
        self.game_active = True

    def _update_ship(self):
        """Move the ship up and down."""
        if self.moving_up:
            self.ship.y -= self.ship_speed

        if self.moving_down:
            self.ship.y += self.ship_speed

        self.ship.top = max(
            0, self.ship.top
        )

        self.ship.bottom = min(
            self.height, self.ship.bottom
        )

    def _fire_bullet(self):
        """Fire a bullet to the right."""
        if len(self.bullets) < self.bullet_limit:
            bullet = pygame.Rect(
                self.ship.right,
                self.ship.centery - 3,
                22,
                6
            )

            self.bullets.append(bullet)

    def _update_bullets(self):
        """Move bullets and check collisions."""
        for bullet in self.bullets[:]:
            bullet.x += self.bullet_speed

            if bullet.left >= self.width:
                self.bullets.remove(bullet)
                continue

            for alien in self.aliens[:]:
                if bullet.colliderect(alien):
                    self.aliens.remove(alien)
                    self.bullets.remove(bullet)

                    self.score += 50
                    self._check_level()

                    break

    def _spawn_aliens(self):
        """Create aliens at the right side of the screen."""
        current_time = pygame.time.get_ticks()

        if (
            current_time - self.last_spawn
            >= self.alien_spawn_interval
        ):
            alien_y = random.randint(
                20,
                self.height - self.alien_height - 20
            )

            alien = pygame.Rect(
                self.width,
                alien_y,
                self.alien_width,
                self.alien_height
            )

            self.aliens.append(alien)
            self.last_spawn = current_time

    def _update_aliens(self):
        """Move aliens toward the ship."""
        for alien in self.aliens[:]:
            alien.x -= self.alien_speed

            if alien.colliderect(self.ship):
                self._lose_life()
                return

            elif alien.right < 0:
                self.aliens.remove(alien)
                self._lose_life()
                return

    def _lose_life(self):
        """Respond when an alien reaches or hits the ship."""
        self.lives -= 1

        self.aliens.clear()
        self.bullets.clear()

        self.ship.centery = self.height // 2
        self.moving_up = False
        self.moving_down = False

        self.last_spawn = pygame.time.get_ticks()

        if self.lives <= 0:
            self.game_active = False

    def _check_level(self):
        """Increase difficulty as score increases."""
        new_level = self.score // 500 + 1

        if new_level > self.level:
            self.level = new_level
            self._increase_speed()

    def _increase_speed(self):
        """Make aliens faster each level."""
        self.alien_speed *= 1.15

        self.alien_spawn_interval = max(
            300,
            int(self.alien_spawn_interval * 0.9)
        )

    def _draw_ship(self):
        """Draw a triangular ship facing right."""
        points = [
            (self.ship.left, self.ship.top),
            (self.ship.right, self.ship.centery),
            (self.ship.left, self.ship.bottom)
        ]

        pygame.draw.polygon(
            self.screen,
            (30, 100, 220),
            points
        )

    def _draw_aliens(self):
        """Draw aliens."""
        for alien in self.aliens:
            pygame.draw.ellipse(
                self.screen,
                (200, 50, 50),
                alien
            )

            # Alien eyes
            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                (alien.x + 14, alien.y + 15),
                5
            )

            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                (alien.x + 31, alien.y + 15),
                5
            )

    def _draw_bullets(self):
        """Draw bullets."""
        for bullet in self.bullets:
            pygame.draw.rect(
                self.screen,
                (40, 40, 40),
                bullet
            )

    def _draw_scoreboard(self):
        """Display score, level, and remaining lives."""
        score_text = (
            f"Score: {self.score}     "
            f"Level: {self.level}     "
            f"Lives: {self.lives}"
        )

        image = self.small_font.render(
            score_text,
            True,
            (30, 30, 30)
        )

        self.screen.blit(image, (20, 20))

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

    def _update_screen(self):
        """Draw the game screen."""
        self.screen.fill(self.bg_color)

        self._draw_ship()
        self._draw_aliens()
        self._draw_bullets()
        self._draw_scoreboard()

        if not self.game_active:
            self._draw_play_button()

            if self.lives <= 0:
                game_over = self.font.render(
                    "Game Over!",
                    True,
                    (200, 50, 50)
                )

                game_over_rect = game_over.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 - 90
                    )
                )

                self.screen.blit(
                    game_over,
                    game_over_rect
                )

        pygame.display.flip()


if __name__ == "__main__":
    game = SidewaysShooter()
    game.run_game()
