from pathlib import Path
import json

def get_stored_username():
    path = Path('username.json')

    if path.exists():
        contents = path.read_text()
        return json.loads(contents)

    return None


def get_new_username():
    username = input("What is your name? ")

    path = Path('username.json')
    contents = json.dumps(username)
    path.write_text(contents)

    return username


def greet_user():
    username = get_stored_username()

    if username:
        correct = input(f"Are you {username}? (yes/no): ")

        if correct.lower() == 'yes':
            print(f"Welcome back, {username}!")
        else:
            username = get_new_username()
            print(f"We'll remember you, {username}!")

    else:
        username = get_new_username()
        print(f"We'll remember you, {username}!")


greet_user()