
import sys
import random
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from alien_bullet import AlienBullet
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Manage the Alien Invasion game."""

    def __init__(self):
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (
                self.settings.screen_width,
                self.settings.screen_height
            )
        )

        pygame.display.set_caption(
            "Alien Invasion - Exercise 14-7"
        )

        self.clock = pygame.time.Clock()

        self.ship = Ship(self)
        self.stats = GameStats(self)

        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.sb = Scoreboard(self)

        self._create_fleet()

        # Difficulty buttons
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

        # Exercise 14-7: Shield settings
        self.shield_active = False
        self.shield_start_time = 0
        self.shields_left = self.settings.shield_limit

        # Alien firing timer
        self.last_alien_shot = pygame.time.get_ticks()

        self.info_font = pygame.font.SysFont(None, 30)

    def run_game(self):
        """Start the main game loop."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

                if self.stats.game_active:
                    self._update_alien_bullets()
                    self._alien_fire()
                    self._update_shield()

            self._update_screen()
            self.clock.tick(60)

    def _quit_game(self):
        """Save high score before quitting."""
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
        """Start the game at the chosen difficulty."""
        if self.stats.game_active:
            return

        for difficulty, button in self.difficulty_buttons.items():
            if button.rect.collidepoint(mouse_pos):
                self.settings.difficulty = difficulty
                self._start_game()
                break

    def _start_game(self):
        """Reset settings and start a new game."""
        self.settings.initialize_dynamic_settings()

        self.stats.reset_stats()
        self.stats.game_active = True

        self.sb.prep_images()

        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()

        self._create_fleet()

        self.ship.center_ship()
        self.ship.moving_right = False
        self.ship.moving_left = False

        # Reset shields for a new game.
        self.shield_active = False
        self.shields_left = self.settings.shield_limit

        self.last_alien_shot = pygame.time.get_ticks()

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

        elif event.key == pygame.K_s:
            if self.stats.game_active:
                self._activate_shield()

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
        """Fire a bullet from the player's ship."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update player bullets."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullets hitting aliens."""
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

            if self.stats.score >= self.stats.high_score:
                self.stats.save_high_score()

        if not self.aliens:
            self._start_new_level()

    def _start_new_level(self):
        """Prepare the next level."""
        self.bullets.empty()
        self.alien_bullets.empty()

        self._create_fleet()
        self.settings.increase_speed()

        self.stats.level += 1
        self.sb.prep_level()

        self.last_alien_shot = pygame.time.get_ticks()

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
        """Create and position one alien."""
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
        """Update aliens and check collisions."""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(
            self.ship,
            self.aliens
        ):
            if not self.shield_active:
                self._ship_hit()
                return

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Check whether aliens reached the edges."""
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
        """Respond to the ship being hit."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            self.ship.moving_right = False
            self.ship.moving_left = False

            self.shield_active = False
            self.last_alien_shot = pygame.time.get_ticks()

            sleep(0.5)

        else:
            self.stats.game_active = False

            self.ship.moving_right = False
            self.ship.moving_left = False

            self.stats.save_high_score()
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check whether aliens reached the bottom."""
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    # -----------------------------------------
    # Exercise 14-7: Alien shooting
    # -----------------------------------------

    def _alien_fire(self):
        """Allow an alien to fire at regular intervals."""
        current_time = pygame.time.get_ticks()

        if (
            current_time - self.last_alien_shot
            >= self.settings.alien_fire_interval
        ):
            if self.aliens:
                shooting_alien = random.choice(
                    self.aliens.sprites()
                )

                new_bullet = AlienBullet(
                    self,
                    shooting_alien
                )

                self.alien_bullets.add(new_bullet)

            self.last_alien_shot = current_time

    def _update_alien_bullets(self):
        """Move alien bullets and check for hits."""
        self.alien_bullets.update()

        for bullet in self.alien_bullets.copy():

            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)

            elif bullet.rect.colliderect(self.ship.rect):
                self.alien_bullets.remove(bullet)

                if not self.shield_active:
                    self._ship_hit()
                    break

    # -----------------------------------------
    # Exercise 14-7: Protective shields
    # -----------------------------------------

    def _activate_shield(self):
        """Activate a temporary protective shield."""
        if self.shield_active:
            return

        if self.shields_left > 0:
            self.shield_active = True
            self.shields_left -= 1

            self.shield_start_time = (
                pygame.time.get_ticks()
            )

    def _update_shield(self):
        """Deactivate the shield after its duration."""
        if self.shield_active:
            current_time = pygame.time.get_ticks()

            elapsed = (
                current_time - self.shield_start_time
            )

            if elapsed >= self.settings.shield_duration:
                self.shield_active = False

    def _draw_shield(self):
        """Draw a blue protective ring around the ship."""
        if self.shield_active:
            center = self.ship.rect.center

            radius = max(
                self.ship.rect.width,
                self.ship.rect.height
            ) // 2 + 15

            pygame.draw.circle(
                self.screen,
                (0, 150, 255),
                center,
                radius,
                4
            )

    def _draw_shield_info(self):
        """Display remaining shields."""
        text = f"Shields: {self.shields_left}  (Press S)"

        image = self.info_font.render(
            text,
            True,
            (20, 80, 160)
        )

        self.screen.blit(image, (20, 70))

    def _update_screen(self):
        """Draw everything on the screen."""
        self.screen.fill(self.settings.bg_color)

        self.ship.blitme()
        self._draw_shield()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.sb.show_score()
        self._draw_shield_info()

        if not self.stats.game_active:
            for button in self.difficulty_buttons.values():
                button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
