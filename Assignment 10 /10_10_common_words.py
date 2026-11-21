from pathlib import Path

filenames = ['book1.txt', 'book2.txt', 'book3.txt']

for filename in filenames:
    try:
        path = Path(filename)
        contents = path.read_text(encoding='utf-8')

    except FileNotFoundError:
        print(f"{filename} not found.")

    else:
        count1 = contents.lower().count('the')
        count2 = contents.lower().count('the ')

        print(f"{filename}:")
        print(f"'the' appears {count1} times.")
        print(f"'the ' appears {count2} times.")