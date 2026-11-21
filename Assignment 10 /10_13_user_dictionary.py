from pathlib import Path
import json

username = input("Enter your name: ")
age = input("Enter your age: ")
city = input("Enter your city: ")

user = {
    'username': username,
    'age': age,
    'city': city
}

path = Path('user.json')
contents = json.dumps(user)
path.write_text(contents)

contents = path.read_text()
user_info = json.loads(contents)

print(f"Name: {user_info['username']}")
print(f"Age: {user_info['age']}")
print(f"City: {user_info['city']}")