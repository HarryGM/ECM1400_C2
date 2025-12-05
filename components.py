def initialise_board(size = 8):
    board_state = []
    for y in range(size):
        row = []
        for x in range(size):
            # Fill central 4 points works for all board sizes where there are 4 central points
            # Middle top left point
            if x == (size // 2) - 1 and y == (size // 2) - 1:
                row.append("Light")
            # Middle top right point
            elif x == (size // 2) - 1 and y == (size // 2):
                row.append("Dark ")
            # Middle bottom left point
            elif x == (size // 2) and y == (size // 2) - 1:
                row.append("Dark ")
            # Middle bottom right point
            elif x == (size // 2) and y == (size // 2):
                row.append("Light")
            # Fill remaining points
            else:
                row.append("None ")
        board_state.append(row)
    return board_state    

def print_board(board):
    for row in board:
        for element in row:
            print(element, end = " ")
        print("\n")

def check_match_in_direction(board, position, direction, colour, opposing_colour):
    x = position[0]
    y = position[1]

    if board[y][x] == colour:
        return True

    # Check if moving one further and check if this takes you off the board, direction is less than -1 to account for case where stone is at the edge of the board 
    if x + direction[0] > len(board) - 1 or x + direction[0] < 0:
        return False
    if y + direction[1] > len(board) - 1 or y + direction[1] < 0:
        return False
    
    if board[y][x] == "None ":
        return False

    new_pos = (x + direction[0], y + direction[1])
    return check_match_in_direction(board, new_pos, direction, colour, opposing_colour)


def check_adjacent(board, position, direction, colour, opposing_colour):
    x = position[0]
    y = position[1]

    # Check if move takes you off the board
    if x + direction[0] > len(board) - 1 or x + direction[0] < 0:
        return False
    if y + direction[1] > len(board) - 1 or y + direction[1] < 0:
        return False

    # Check if next stone along this direction is opposing in colour
    if board[y + direction[1]][x + direction[0]] != opposing_colour:
        return False

    # Check if moving one further and check if this takes you off the board
    if x + (2 * direction[0]) > len(board) - 1 or x + (2 * direction[0]) < 0:
        return False
    if y + (2 * direction[1]) > len(board) - 1 or y + (2 * direction[1]) < 0:
        return False

    # Check for a match along the line
    new_pos = (x + (2 * direction[0]), y + (2 * direction[1])) 
    return check_match_in_direction(board, new_pos, direction, colour, opposing_colour)

def check_outflanks(board, position, colour):
    x = position[0]
    y = position[1]

    # Determine opposing colour
    if colour == "Light":
        opposing_colour = "Dark "
    else:
        opposing_colour = "Light"

    # Define directions of movement 
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
    valid_directions = []

    # Check each direction individually until a correct one is found
    for direction in directions:
        direction_supports_move = check_adjacent(board, position, direction, colour, opposing_colour)
        if direction_supports_move:
            # Return direction for later use in game_engine.py(changing outflanked stones)
            valid_directions.append(direction)

    if len(valid_directions) > 0:
        return True, valid_directions
    else:
        return False, None

def legal_move(board, position, colour):
    x = position[0]
    y = position[1]
    
    # Check position is unoccupied
    if board[y][x] != "None ":
        return False

    # Check if position outflanks
    return check_outflanks(board, position, colour)[0]
