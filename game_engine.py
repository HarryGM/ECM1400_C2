import re
from components import *

def cli_coords_input():
    while True:
        move_coords = input("enter the coordinates of your move, format 'x, y': ")
        valid_coords = re.search("^[1-8], [1-8]$", move_coords)
        if valid_coords:
            break

    move_coords = move_coords.split(", ")
    return (int(move_coords[0]), int(move_coords[1]))

def swap_player(current_player):
    if current_player == "Dark":
        current_player = "Light"
    else:
        current_player = "Dark"
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

def simple_game_loop():
    print("Welcome to Othello\n")

    board = initialise_board()
    move_counter = 60
    current_player = "Dark"

    while True:
        if not any_legal_moves(board, current_player):
            current_player = swap_player(current_player)
        if not any_legal_moves(board, current_player):
            break

        print(f"{current_player} turn")
        move = cli_coords_input()





