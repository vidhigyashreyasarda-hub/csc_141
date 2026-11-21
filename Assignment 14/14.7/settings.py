
class Settings:
    """Store settings for Alien Invasion."""

    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        # Player bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # Exercise 14-7: Alien bullets
        self.alien_bullet_width = 5
        self.alien_bullet_height = 18
        self.alien_bullet_color = (220, 40, 40)
        self.alien_fire_interval = 900

        # Exercise 14-7: Shields
        self.shield_duration = 3000
        self.shield_limit = 3

        # Difficulty settings
        self.difficulty = "Medium"
        self.score_scale = 1.5
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize speeds based on difficulty."""
        if self.difficulty == "Easy":
            self.ship_speed = 5.0
            self.bullet_speed = 7.0
            self.alien_speed = 0.8
            self.alien_bullet_speed = 3.0
            self.speedup_scale = 1.05

        elif self.difficulty == "Medium":
            self.ship_speed = 4.0
            self.bullet_speed = 6.0
            self.alien_speed = 1.5
            self.alien_bullet_speed = 4.0
            self.speedup_scale = 1.1

        else:
            self.ship_speed = 3.5
            self.bullet_speed = 5.0
            self.alien_speed = 2.5
            self.alien_bullet_speed = 5.0
            self.speedup_scale = 1.2

        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """Increase game difficulty after each level."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_bullet_speed *= self.speedup_scale

        self.alien_points = int(
            self.alien_points * self.score_scale
        )
