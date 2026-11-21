
import string


def get_characters(mode):
    """Return allowed characters for a password mode."""

    if mode == "calm":
        return string.ascii_letters

    elif mode == "balanced":
        return string.ascii_letters + string.digits

    elif mode == "chaotic":
        return (
            string.ascii_letters
            + string.digits
            + string.punctuation
        )

    else:
        raise ValueError("Invalid password mode.")
