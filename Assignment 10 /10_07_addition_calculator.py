while True:
    try:
        num1 = input("Enter first number (or q): ")

        if num1.lower() == 'q':
            break

        num2 = input("Enter second number (or q): ")

        if num2.lower() == 'q':
            break

        total = int(num1) + int(num2)
        print("Sum:", total)

    except ValueError:
        print("Please enter numbers only.")