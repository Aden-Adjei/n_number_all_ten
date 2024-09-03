from all_ten_solver import solver
from all_ten import gen_puzzle
def run():
    game = input("Input the game you want to solve or the size "
            + "of the puzzle if you want the solution to a random game ")

    # creates random game
    if game.isnumeric():
        if int(game) < 3:
            print("there are no valid games of size less than 3")
            return
        game = gen_puzzle(int(game))

    # parses inputed game
    else:
        try:
            game = eval(game)

            # ensures that game is valid
            if not isinstance(game, (list, set, tuple)):
                raise SyntaxError
            if not all(isinstance(num, int) for num in game):
                raise SyntaxError
        except (SyntaxError, NameError):
            # reprompts user if input is invalid
            print(f"{game} is not a valid game. Please input a list, tuple, "
                  + "or set of the playable integers in the game\n")
            run()
            return

    # prints the solution
    print("")
    solution = solver(game)
    if solution is None:
        print(f"The game: {game}\nhas no solution")
    else:
        print(f"The solution to {game} is:\n{solution}", [eval(elem) for elem in solution] == [1,2,3,4,5,6,7,8,9,10])

run()
