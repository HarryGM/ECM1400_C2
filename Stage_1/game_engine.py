""" 
game_engine module:
module to run the game, using a simple game loop which implements many components functions 
and a number of helper functions defined in game_engine
"""

import re
from components import initialise_board, print_board, legal_move, check_outflanks

def cli_coords_input():
    """ 
    Takes a coordinate input in the form 'x, y',
    checks using regex if the input is valid,
    if so the input is returned in a format considering zero indexing
    """
    
    # iterate until valid move is inputted
    while True:
        move_coords = input("enter the coordinates of your move, format 'x, y': ")
        valid_coords = re.search("^[1-8], [1-8]$", move_coords)
        if valid_coords:
            break

    move_coords = move_coords.split(", ")
    # Adjust for 0 indexing
    return (int(move_coords[0]) - 1, int(move_coords[1]) - 1)

def swap_player(current_player):
    """ Takes a player, Dark or Light, and swaps them to the other player"""

    if current_player == "Dark ":
        current_player = "Light"
    else:
        current_player = "Dark "
    return current_player

def any_legal_moves(board, current_player):
    """ Checks if any moves on the board are legal  """

    move_available = False
    # Iterate over every board position
    for y in range(len(board)):
        for x in range(len(board)):
            if legal_move(board, (x, y), current_player):
                move_available = True
                break

    return move_available

def change_outflanked_stones(board, move, current_player, direction):
    """ Based on a direction flips all stones which are outflanked  """

    x = move[0]
    y = move[1]
    
    # Move one in the direction specified
    new_pos = (x + direction[0], y + direction[1])

    # Check if stone is the same as the current player to stop recursing
    if board[new_pos[1]][new_pos[0]] != current_player:
        board[new_pos[1]][new_pos[0]] = current_player
        change_outflanked_stones(board, new_pos, current_player, direction)

    return board

def simple_game_loop():
    """ 
    Whilst the game is not over,
    prompts player to enter moves,
    checks their legality,
    edits board states,
    outputs board states,
    outputs result when the game is over
    """

    print("Welcome to Othello\n")

    board = initialise_board()
    # print initial board
    print_board(board)
    # Set base values for important variables
    game_over = False
    move_counter = 60
    current_player = "Dark "

    while not game_over:
        # Check if the player can play a move,
        # and if the game is over based on whether the subsequent player can play a move
        if not any_legal_moves(board, current_player):
            current_player = swap_player(current_player)
        if not any_legal_moves(board, current_player):
            game_over = True
            break

        # Check if move counter has expired
        if move_counter == 0:
            game_over = True
            break

        # Prompt move
        print(f"{current_player} turn")
        move = cli_coords_input()
        # Check move legality and play move
        if legal_move(board, move, current_player):
            # Play move
            board[move[1]][move[0]] = current_player

            # Change outflanked stones
            valid_directions = check_outflanks(board, move, current_player)[1]
            for direction in valid_directions:
                change_outflanked_stones(board, move, current_player, direction)
            move_counter -= 1
            current_player = swap_player(current_player)

            # Output board to see effect of move
            print_board(board)

    print("Game over\n")
    # Initialise stone counts
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

if __name__ == "__main__":
    simple_game_loop()
