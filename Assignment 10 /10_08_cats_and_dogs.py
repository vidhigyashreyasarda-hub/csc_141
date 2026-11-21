from pathlib import Path

filenames = ['cats.txt', 'dogs.txt']

for filename in filenames:
    try:
        path = Path(filename)
        contents = path.read_text()
        print(contents)

    except FileNotFoundError:
        print(f"Sorry, {filename} was not found.")