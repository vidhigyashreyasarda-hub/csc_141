
import secrets

from modes import get_characters


def generate_password(length, mode):
    """Generate a random password."""

    if length < 4:
        raise ValueError(
            "Password must be at least 4 characters long."
        )

    characters = get_characters(mode)

    password = ""

    for i in range(length):
        password += secrets.choice(characters)

    return password
