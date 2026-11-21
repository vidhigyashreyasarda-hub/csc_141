from pathlib import Path

names = []

while True:
    name = input("Enter your name (or quit): ")

    if name.lower() == 'quit':
        break

    names.append(name)

path = Path('guest_book.txt')
path.write_text('\n'.join(names) + '\n')