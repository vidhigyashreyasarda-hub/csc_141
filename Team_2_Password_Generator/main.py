
from generator import generate_password
from strength_checker import check_strength


def main():
    """Run the password generator application."""

    print("=" * 40)
    print("       TEAM 2 PASSWORD GENERATOR")
    print("=" * 40)

    while True:
        print("\nChoose a password mode:")
        print("1. Calm (Letters)")
        print("2. Balanced (Letters + Numbers)")
        print("3. Chaotic (Letters + Numbers + Symbols)")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        modes = {
            "1": "calm",
            "2": "balanced",
            "3": "chaotic"
        }

        if choice == "4":
            print("\nThank you for using Password Generator!")
            break

        if choice not in modes:
            print("Invalid choice. Please try again.")
            continue

        try:
            length = int(
                input("Enter password length (minimum 4): ")
            )

            mode = modes[choice]

            password = generate_password(length, mode)

            strength = check_strength(password)

            print("\n" + "-" * 40)
            print("Generated Password:", password)
            print("Mode:", mode.capitalize())
            print("Password Length:", len(password))
            print("Password Strength:", strength)
            print("-" * 40)

        except ValueError as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
