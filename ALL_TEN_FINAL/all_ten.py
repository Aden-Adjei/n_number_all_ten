"""
Impluments and runs the all ten game
"""
from datetime import datetime
import random
from collections import Counter
from all_ten_solver import solver, ALL_TEN

def rules(n):
    """
    Prints the rules for the game with n numbers
    """
    print(f"Use all {n} numbers in the state once each to make 1 through 10 using "
          + "addition(+), subtraction(-), multiplication(*), and division(/)\n"
          + f"You can type all {n} numbers in one expression and press enter, "
          + "or you can turn any expression into a new number in the state by "
          + "pressing enter. Decimals are allowed (for repeating decimals, use "
          + "as many or more digits than appear in the state). Negatives will be "
          + f"made positive when evaluated. Only The original {n} numbers can be "
          + f"combined into multi-digit numbers. All {n} numbers must be used.\n"
          + "Enjoy!")


def can_make_ten(puzzle):
    """
    determins if puzzle is solvable
    """
    solution = solver(puzzle)
    return solution is not None


def gen_puzzle(n):
    """
    Generates an n number tuple that can make
    all numbers from zero to 10 using addition,
    subbtraction, multiplication, division, and
    concatenations
    """
    # no viable puzzles with less than 3 numbers
    if n < 3:
        return None
    # only one viable puzzle with exactly 3 numbers
    if n == 3:
        return (1,2,4)

    # generates a random puzzle with n numbers
    # then makes sure that it is solvable until
    # it finds a viable puzzle
    viable = False
    while not viable:
        puzzle = tuple(random.randint(1,9) for _ in range(n))
        viable = can_make_ten(puzzle)

    return puzzle


def parse_input(start_state, state, exp, edit_count):
    """
    given an expression, the start state, and the current state,
    determines the next state and the value found or zero if none is found
    """
    counts = Counter(state)
    edit_counts = Counter(state[edit_count:])
    nums = []
    cur_num = ""
    # finds all the nubmers in the expression
    for char in exp:
        if char in "()*+/- ":
            if cur_num:
                nums.append(cur_num)
                cur_num = ""
            continue

        if char in "1234567890.":
            cur_num += char

        else:
            print(f"'{exp}' is not a valid expression")
            return state, 0
    if cur_num:
        nums.append(cur_num)

    # checks that each number can be made in the current state
    for num in nums:
        if num == ".":
            print(f"'{exp}' is not a valid expression")
            return state, 0

        # deals with floats
        if "." in num:
            num_float = float(num)
            if num_float in counts and counts[num_float] > 0:
                counts[num_float] -= 1
            else:
                print(f"'{num_float}' used too many times")
                return state, 0

        # deals with integers
        else:
            num_int = int(num)
            if num_int in counts and counts[num_int] > 0:
                counts[num_int] -= 1

            # checks if the number is made by combining to
            # numbers in the state
            elif len(num) > 1:
                con_counts = Counter(num)
                for n, count in con_counts.items():
                    # only considers numbers that haven't been edited
                    if int(n) in edit_counts:
                        if edit_counts[int(n)] < count:
                            print(f"'{num_int}' used too many times")
                            return state, 0
                        counts[int(n)] -= count
                    else:
                        print("Only numbers from the original puzzle can be combined")
                        return state, 0
            else:
                print(f"'{num_int}' used too many times")
                return state, 0

    # evaluates the input expression
    try:
        state = [abs(eval(exp)),]
    except (SyntaxError, NameError):
        print(f"'{exp}' is not a valid expression")
        return state, 0

    # generates the new state
    for num, count in counts.items():
        state.extend([num]*count)

    # checks if a new number in all ten as been found
    if len(state) == 1:
        if state[0] in ALL_TEN:
            return start_state, state[0]
        print(state[0], "is not a number from 1-10")
        return start_state, 0

    # return the edited state
    return state, 0


def game(n):
    """
    Runs a game of all_ten with n starting numbers
    """
    start_state = gen_puzzle(n)
    prev_state = start_state
    state = start_state
    found = set()
    start = datetime.now()
    edit_count = 0

    # prints rules and runs game loop
    rules(n)
    while found != ALL_TEN:
        if set(state) == set(start_state):
            edit_count = 0

        print("*"*10)
        print("found:", found)
        print("state:", state)
        print("*"*10)
        exp = input()

        # checks that something is input
        if not exp:
            continue

        # refresh command
        if exp == "r":
            state = start_state
            continue

        # quit command
        if exp == "q":
            print("Quitting...")
            return

        # updates game state
        prev_state = state
        state, find = parse_input(start_state, state, exp, edit_count)
        if set(state) != set(prev_state):
            edit_count += 1
        else:
            state = prev_state
        if find:
            found.add(find)

    print("You win, Time:", datetime.now() - start)
