def make_branches(char1, char2, number_of_rows = 12):
    char = char1
    for row in range(number_of_rows):
        width = (row * 2) + 1
        buffer = ((number_of_rows * 2) + 1 - width) // 2
        print((buffer * " ") + (width * char))
        if char == char1:
            char = char2
        else:
            char = char1

def make_trunk(char, number_of_rows = 4, width = 5, size_of_branches = 12):
    for row in range(number_of_rows):
        branch_width = (size_of_branches * 2) + 1
        buffer = (branch_width - width) // 2
        print((buffer * " ") + (width * char))

def make_christmas_tree(branch_char_1, branch_char_2, trunk_char = 5, number_of_rows = 12, number_of_trunk_rows = 4, trunk_width = 5):
    make_branches(branch_char_1, branch_char_2, number_of_rows)
    make_trunk(trunk_char, number_of_trunk_rows, trunk_width, number_of_rows)

make_christmas_tree('*', '%', '*', 12, 4, 5)
make_christmas_tree('V', 'W', 'o', 16, 3, 10)
