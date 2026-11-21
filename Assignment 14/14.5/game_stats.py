
from pathlib import Path


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings

        self.game_active = False

        # File to save the all-time high score.
        self.high_score_file = (
            Path(__file__).resolve().parent / "high_score.txt"
        )

        # Load the saved high score.
        self.high_score = self._load_high_score()

        self.reset_stats()

    def _load_high_score(self):
        """Read the all-time high score from a file."""
        try:
            contents = self.high_score_file.read_text(
                encoding="utf-8"
            )
            return int(contents.strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        """Save the high score permanently."""
        self.high_score_file.write_text(
            str(self.high_score),
            encoding="utf-8"
        )

    def reset_stats(self):
        """Reset statistics for a new game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
