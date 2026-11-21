
import unittest
import string

from generator import generate_password
from strength_checker import check_strength


class TestPasswordGenerator(unittest.TestCase):

    def test_password_length(self):
        password = generate_password(12, "balanced")
        self.assertEqual(len(password), 12)

    def test_calm_mode(self):
        password = generate_password(20, "calm")
        self.assertTrue(password.isalpha())

    def test_balanced_mode(self):
        password = generate_password(20, "balanced")
        self.assertTrue(password.isalnum())

    def test_chaotic_mode(self):
        password = generate_password(20, "chaotic")
        allowed = (
            string.ascii_letters
            + string.digits
            + string.punctuation
        )
        self.assertTrue(
            all(char in allowed for char in password)
        )

    def test_short_password(self):
        with self.assertRaises(ValueError):
            generate_password(3, "calm")

    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            generate_password(12, "unknown")

    def test_weak_password(self):
        self.assertEqual(check_strength("abc"), "Weak")

    def test_strong_password(self):
        self.assertEqual(
            check_strength("Abcd1234!xyz"),
            "Strong"
        )


if __name__ == "__main__":
    unittest.main()
