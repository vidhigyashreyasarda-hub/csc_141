
import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Manage Alien Invasion game behavior."""

    def __init__(self):
        """Initialize the game and its resources."""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (
                self.settings.screen_width,
                self.settings.screen_height
            )
        )

        pygame.display.set_caption(
            "Alien Invasion - Exercise 14-5"
        )

        self.clock = pygame.time.Clock()

        # Create ship and game statistics.
        self.ship = Ship(self)
        self.stats = GameStats(self)

        # Create bullet and alien groups.
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Create scoreboard.
        self.sb = Scoreboard(self)

        # Create alien fleet.
        self._create_fleet()

        # Create difficulty buttons.
        self.difficulty_buttons = {}

        for difficulty in ("Easy", "Medium", "Hard"):
            self.difficulty_buttons[difficulty] = Button(
                self, difficulty
            )

        center_x = self.screen.get_rect().centerx
        center_y = self.screen.get_rect().centery

        positions = {
            "Easy": center_y - 100,
            "Medium": center_y,
            "Hard": center_y + 100
        }

        for difficulty, button in self.difficulty_buttons.items():
            button.rect.center = (
                center_x,
                positions[difficulty]
            )

            button.msg_image_rect.center = button.rect.center

    def run_game(self):
        """Start the main game loop."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _quit_game(self):
        """Save the all-time high score before exiting."""
        self.stats.save_high_score()
        pygame.quit()
        sys.exit()

    def _check_events(self):
        """Respond to keyboard and mouse events."""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self._quit_game()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_difficulty_buttons(event.pos)

    def _check_difficulty_buttons(self, mouse_pos):
        """Start the game with the selected difficulty."""
        if self.stats.game_active:
            return

        for difficulty, button in self.difficulty_buttons.items():
            if button.rect.collidepoint(mouse_pos):
                self.settings.difficulty = difficulty
                self._start_game()
                break

    def _start_game(self):
        """Reset game settings and start a new game."""

        # Reset difficulty-based speeds.
        self.settings.initialize_dynamic_settings()

        # Reset game statistics.
        # The saved high score is NOT reset.
        self.stats.reset_stats()
        self.stats.game_active = True

        # Reset scoreboard.
        self.sb.prep_score()
        self.sb.prep_high_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Clear existing bullets and aliens.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet.
        self._create_fleet()

        # Center the ship.
        self.ship.center_ship()
        self.ship.moving_right = False
        self.ship.moving_left = False

        # Hide mouse cursor.
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to key presses."""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_SPACE:
            if self.stats.game_active:
                self._fire_bullet()

        elif event.key == pygame.K_q:
            self._quit_game()

        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()

    def _check_keyup_events(self, event):
        """Respond to key releases."""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a bullet and add it to the group."""

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update bullet positions and remove old bullets."""

        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""

        collisions = pygame.sprite.groupcollide(
            self.bullets,
            self.aliens,
            True,
            True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += (
                    self.settings.alien_points * len(aliens)
                )

            self.sb.prep_score()
            self.sb.check_high_score()

            # Exercise 14-5:
            # Save the new high score immediately.
            if self.stats.score >= self.stats.high_score:
                self.stats.save_high_score()

        # Start a new level when all aliens are destroyed.
        if not self.aliens:
            self.bullets.empty()

            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Create a fleet of aliens."""

        alien = Alien(self)

        alien_width = alien.rect.width
        alien_height = alien.rect.height

        available_space_x = (
            self.settings.screen_width - 2 * alien_width
        )

        number_aliens_x = available_space_x // (
            2 * alien_width
        )

        ship_height = self.ship.rect.height

        available_space_y = (
            self.settings.screen_height
            - 3 * alien_height
            - ship_height
        )

        number_rows = available_space_y // (
            2 * alien_height
        )

        for row_number in range(int(number_rows)):
            for alien_number in range(int(number_aliens_x)):
                self._create_alien(
                    alien_number,
                    row_number
                )

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the fleet."""

        alien = Alien(self)

        alien_width = alien.rect.width

        alien.x = (
            alien_width
            + 2 * alien_width * alien_number
        )

        alien.rect.x = int(alien.x)

        alien.rect.y = (
            alien.rect.height
            + 2 * alien.rect.height * row_number
        )

        self.aliens.add(alien)

    def _update_aliens(self):
        """Update alien positions and check collisions."""

        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(
            self.ship,
            self.aliens
        ):
            self._ship_hit()
            return

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond when aliens reach screen edges."""

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Move the fleet down and reverse direction."""

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond when the ship is hit by an alien."""

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Remove existing aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet.
            self._create_fleet()

            # Center the ship.
            self.ship.center_ship()

            self.ship.moving_right = False
            self.ship.moving_left = False

            # Pause briefly after collision.
            sleep(0.5)

        else:
            self.stats.game_active = False

            self.ship.moving_right = False
            self.ship.moving_left = False

            # Save high score when game ends.
            self.stats.save_high_score()

            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check whether aliens reached the bottom."""

        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        """Draw everything on the screen."""

        self.screen.fill(self.settings.bg_color)

        # Draw ship.
        self.ship.blitme()

        # Draw bullets.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw aliens.
        self.aliens.draw(self.screen)

        # Display scoreboard.
        self.sb.show_score()

        # Display difficulty buttons when inactive.
        if not self.stats.game_active:
            for button in self.difficulty_buttons.values():
                button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
