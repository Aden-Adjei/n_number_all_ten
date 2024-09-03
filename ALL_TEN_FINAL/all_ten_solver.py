"""
Contains code for the solver to All Ten
"""
ALL_TEN = set(range(1,11))
def solver(game):
    """
    given a game represented as a set of numbers
    that can be used to make all ten,
    and a start_state represented as a set
    of already found numbers, returns a solution
    as a dictionary mapping found numbers to expressions
    """
    to_find = ALL_TEN.copy()
    sols = [None]*10
    epsilon = 10**(-6)

    def all_ten_helper(nums):
        """
        Recursively computes numbers that can be made
        to see if all nums from 1 to 10 can be made
        """
        # checks if found number needed to be found
        if len(nums) == 1:
            if int(nums[0][0]) in to_find \
            and abs(int(nums[0][0]) - nums[0][0]) <= epsilon:
                to_find.remove(int(nums[0][0]))
                sols[int(nums[0][0]) - 1] = nums[0][2]
            return

        # tries all possible arithmetic operations
        # between every pair of numbers in the game
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):

                before = nums[:i]
                at_i = nums[i][0]
                at_j = nums[j][0]
                between = nums[i+1:j]
                after = nums[j+1:]
                # parentheses rules for addition and subtraction
                # (puts more parenthesis than necessary, but few
                # enough to maintain readability)
                i_parenths = ("-" in nums[i][2]) or ("+" in nums[i][2])
                j_parenths = ("-" in nums[j][2]) or ("+" in nums[j][2])

                # tries adding two numbers
                expr_1 = f"{nums[i][2]}+{nums[j][2]}"
                all_ten_helper([(at_i + at_j, False, expr_1)]+
                                before + between + after)

                # tries subtracting two numbers (in both directions)
                expr_1 = f"{nums[i][2]}-({nums[j][2]})" if j_parenths\
                    else f"{nums[i][2]}-{nums[j][2]}"
                expr_2 = f"{nums[j][2]}-({nums[i][2]})" if i_parenths\
                    else f"{nums[j][2]}-{nums[i][2]}"
                all_ten_helper([(at_i - at_j, False, expr_1)]+
                                before + between + after)
                all_ten_helper([(at_j - at_i, False, expr_2)]+
                                before + between + after)

                # multiplication/division parentheses rules
                j_parenths = ("-" in nums[j][2]) or ("+" in nums[j][2])\
                            or ("*" in nums[j][2]) or ("/" in nums[j][2])

                # tries multiplying two numbers
                expr_1 = f"({nums[i][2]})*({nums[j][2]})" if i_parenths and j_parenths\
                    else f"({nums[i][2]})*{nums[j][2]}" if i_parenths\
                    else f"{nums[i][2]}*({nums[j][2]})" if j_parenths\
                    else f"{nums[i][2]}*{nums[j][2]}"
                all_ten_helper([(at_i * at_j, False, expr_1)]+
                                before + between + after)

                # tries dividing two numbers
                expr_1 = f"({nums[i][2]})/({nums[j][2]})" if i_parenths and j_parenths\
                    else f"({nums[i][2]})/{nums[j][2]}" if i_parenths\
                    else f"{nums[i][2]}/({nums[j][2]})" if j_parenths\
                    else f"{nums[i][2]}/{nums[j][2]}"

                # division parentheses rules in other direction
                i_parenths = ("-" in nums[i][2]) or ("+" in nums[i][2])\
                            or ("*" in nums[i][2]) or ("/" in nums[i][2])
                j_parenths = ("-" in nums[j][2]) or ("+" in nums[j][2])

                expr_2 = f"({nums[j][2]})/({nums[i][2]})" if i_parenths and j_parenths\
                    else f"({nums[j][2]})/{nums[i][2]}" if j_parenths\
                    else f"{nums[j][2]}/({nums[i][2]})" if i_parenths\
                    else f"{nums[j][2]}/{nums[i][2]}"
                if at_i != 0 and at_j != 0:
                    all_ten_helper([(at_i / at_j, False, expr_1)]+
                                    before + between + after)
                    all_ten_helper([(at_j / at_i, False, expr_2)]+
                                    before + between + after)
                elif at_i == 0 and at_j != 0:
                    all_ten_helper([(at_i / at_j, False, expr_1)]+
                                    before + between + after)
                elif at_i != 0 and at_j == 0:
                    all_ten_helper([(at_j / at_i, False, expr_2)]+
                                    before + between + after)

                # tries concatenating two numbers
                if nums[i][1] and nums[j][1]:
                    all_ten_helper([(int(str(at_i) + str(at_j)), True, nums[i][2]+nums[j][2])]
                                    + before + between + after)
                    all_ten_helper([(int(str(at_j) + str(at_i)), True, nums[j][2]+nums[i][2])]
                                    + before + between + after)

                # stops search if all ten numbers are found
                if not to_find:
                    raise IndexError
        return

    # finds and returns the solutions
    try:
        all_ten_helper([(num,True,str(num)) for num in game])
    except IndexError:
        return sols
    return None
