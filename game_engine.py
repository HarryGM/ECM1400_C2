import re
from components import *

def cli_coords_input():
    while True:
        move_coords = input("enter the coordinates of your move, format 'x, y': ")
        valid_coords = re.search("^[1-8], [1-8]$", move_coords)
        if valid_coords:
            break

    move_coords = move_coords.split(", ")
    # Adjust for 0 indexing
    return (int(move_coords[0]) - 1, int(move_coords[1]) - 1)

def swap_player(current_player):
    if current_player == "Dark ":
        current_player = "Light"
    else:
        current_player = "Dark "
    return current_player

def any_legal_moves(board, current_player):
    move_available = False
    for y in range(len(board)):
        for x in range(len(board)):
            if legal_move(board, (x, y), current_player):
                move_available = True
                break
        else:
            continue
        break

    return move_available

def change_outflanked_stones(board, move, current_player, direction):
    x = move[0]
    y = move[1]

    new_pos = (x + direction[0], y + direction[1])

    if (board[new_pos[1]][new_pos[0]] != current_player):
        board[new_pos[1]][new_pos[0]] = current_player
        change_outflanked_stones(board, new_pos, current_player, direction)
    else:
        return board

def simple_game_loop():
    print("Welcome to Othello\n")

    board = initialise_board()
    game_over = False
    move_counter = 60
    current_player = "Dark "

    while not game_over:
        if not any_legal_moves(board, current_player):
            current_player = swap_player(current_player)
        if not any_legal_moves(board, current_player):
            game_over = True
            break

        if move_counter == 0:
            game_over = True
            break

        print(f"{current_player} turn")
        move = cli_coords_input()
        if legal_move(board, move, current_player):
            # Play move
            board[move[1]][move[0]] = current_player

            # Change outflanked stones
            direction = check_outflanks(board, move, current_player)[1]
            change_outflanked_stones(board, move, current_player, direction)
            move_counter -= 1
            current_player = swap_player(current_player)
            
            # Output board to see effect of move
            print_board(board)

    print("Game over\n")
    # initialise stone counts
    num_dark_stones = 0
    num_light_stones = 0

    for row in board:
        num_dark_stones += row.count("Dark ")
        num_light_stones += row.count("Light")
                

    if num_dark_stones > num_light_stones:
        print(f"Winner is Dark, Dark: {num_dark_stones}, Light: {num_light_stones}")
    elif num_light_stones > num_dark_stones: 
        print(f"Winner is Light, Dark: {num_dark_stones}, Light: {num_light_stones}")
    else:
        print(f"Draw, Dark: {num_dark_stones}, Light: {num_light_stones}")





