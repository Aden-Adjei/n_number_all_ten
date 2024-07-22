from all_ten import game
def start():
    n = input("How many numbers would you like to play with? (standard is 4) ")

    # creates standard 4 integer game
    if n.lower() == "standard":
        n = 4

    # creates n integer game
    elif n.isnumeric():
        n = int(n)

        # prompts user if input is invalid
        if n < 3:
            print("You must input an integer greater than 2")
            start()
            return
    # prompts user if input is invalid
    else:
        print(f"{n} is not a number\n")
        start()
        return

    # separates game text and runs game
    print("\n\n")
    game(n)

start()
