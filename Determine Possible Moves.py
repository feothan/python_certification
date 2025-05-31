def determine_possible_moves(piece, posx, posy):
    gridx, gridy = 6, 6
    possibilities = []

    # Generate the possible moves
    for each in range(piece + 1):
        possibilities.append((posx + each, posy + (piece - each)))
        possibilities.append((posx + each, posy - (piece - each)))
        possibilities.append((posx - each, posy + (piece - each)))
        possibilities.append((posx - each, posy - (piece - each)))

    # Remove duplicates
    unique_possibilities = list(set(possibilities))

    # Filter valid positions
    valid_positions = []
    for each in unique_possibilities:
        if 0 <= each[0] < gridx and 0 <= each[1] < gridy:
            valid_positions.append(each)
    return valid_positions

moves = determine_possible_moves(4, 5, 5)

print(moves)

