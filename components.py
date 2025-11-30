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

