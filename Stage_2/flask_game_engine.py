""" 
flask_game_engine module:
Sets up a flask server and handles all necessary boilerplate,
defines a number of useful functions for engine purposes,
handles all flask routes, managing routes for saving, loading and moves,
runs game functionallity based on data from frontend
"""

import os
import json

from flask import Flask, render_template, request, jsonify
from components import initialise_board, legal_move, check_outflanks


# Define some useful functions from game_engine.py
def swap_player(current_player):
    """ Takes a player, Dark or Light, and swaps them to the other player """

    if current_player == "Dark ":
        current_player = "Light"
    else:
        current_player = "Dark "
    return current_player

def change_outflanked_stones(game_board,player_move, current_player, direction):
    """ Based on a direction flips all stones which are outflanked  """

    x = player_move[0]
    y = player_move[1]

    # Move one in specified direction
    new_pos = (x + direction[0], y + direction[1])

    # Check if stone is the same as the current player to stop recursing
    if game_board[new_pos[1]][new_pos[0]] != current_player:
        game_board[new_pos[1]][new_pos[0]] = current_player
        change_outflanked_stones(game_board, new_pos, current_player, direction)

    return game_board

def any_legal_moves(game_board, current_player):
    """ Checks if any moves on the board are legal """

    move_available = False
    # Iterate over every board position
    for y in range(len(game_board)):
        for x in range(len(game_board)):
            if legal_move(game_board, (x, y), current_player):
                move_available = True
                break

    return move_available

def check_score(game_board):
    """ determine the score of the game based on a board state """

    num_dark_stones = 0
    num_light_stones = 0

    # Count number of each colour on the board
    for row in game_board:
        num_dark_stones += row.count("Dark ")
        num_light_stones += row.count("Light")

    # Determine winner
    if num_dark_stones > num_light_stones:
        winner = "Dark "
    elif num_light_stones >  num_dark_stones:
        winner = "Light"
    else:
        winner = "Draw"
    return winner, num_dark_stones, num_light_stones

# Initialise the starting board
board = initialise_board()

# Define data for response object
data = {
    "board" : board,
    "status" : None,
    "player" : "Dark ",
    "finished" : None,
    "move_count" : 60
}

app = Flask(__name__)

@app.route("/")
def index():
    """ Root endpoint, render template on page load """

    return render_template("index.html", game_board = board)

@app.route("/save", methods = ["POST"])
def save():
    """ 
    Save endpoint, 
    get save data,
    check if save directory exists if not create it,
    save data to a json file in save directory
    """

    # Get save data
    save_data = request.get_json()
    save_dir = "othello_saves"
    files_in_dir = 0

    # Add additional data to save data
    save_data["player"] = data["player"]
    save_data["move_count"] = data["move_count"]

    # Make save directiry if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Find number of files in save directory
    for path in os.listdir(save_dir):
        # check if current path is a file
        if os.path.isfile(os.path.join(save_dir, path)):
            files_in_dir += 1

    # Create and write to file
    try:
        with open(f"{save_dir}/save_{files_in_dir + 1}.json", "x", encoding = "utf-8") as f:
            try:
                json.dump(save_data, f)
                return "success"
            except (IOError, OSError):
                return "failed to write to the file"
    except (FileNotFoundError, PermissionError, OSError):
        return "failed to open file"

@app.route("/load", methods = ["POST"])
def load():
    """ 
    Load endpoint,
    get save file name from frontend,
    read save file,
    change relevant variables,
    respond with response data
    """

    load_data_loc = request.get_json()
    save_dir = "othello_saves"

    # Retrieve save data
    try:
        with open(f"{save_dir}/{load_data_loc["file_name"]}", "r", encoding = "utf-8") as f:
            load_data = json.load(f)
    except (FileNotFoundError, PermissionError, OSError):
        return "failed to open file"

    # Set variables for use in backend
    data["board"] = load_data["board"]
    data["player"] = load_data["player"]
    data["move_count"] = load_data["move_count"]

    # Set response data to change board
    response_data = {
        "board": load_data["board"],
        "player": load_data["player"],
        "move_count": load_data["move_count"]
        }

    return jsonify(response_data)

@app.route("/move", methods = ["GET"])
def move():
    """ Move endpoint, handles response to move data from frontend """

    x = int(request.args.get("x")) - 1
    y = int(request.args.get("y")) - 1
    current_player = data["player"]
    move_count = data["move_count"]
    game_board = data["board"]
    data["status"] = "success"

    if legal_move(game_board, (x, y), current_player):
        data["status"] = "success"
        # Play move
        game_board[y][x] = current_player

        # Change outflanked stones
        valid_directions = check_outflanks(game_board, (x, y), current_player)[1]
        for direction in valid_directions:
            change_outflanked_stones(game_board, (x, y), current_player, direction)

        move_count -= 1
        current_player = swap_player(current_player)
    else:
        data["status"] = "fail"
        data["message"] = "illegal move"

    # Check if the next player has any legal moves
    if not any_legal_moves(game_board, current_player):
        current_player = swap_player(current_player)
        # Check if the other player has any legal moves
        if not any_legal_moves(game_board, current_player):
            data["status"] = "game over"

            # Determine game over output
            winner, num_dark_stones, num_light_stones = check_score(board)
            if winner == "Draw":
                data["finished"] = f"Draw, {num_dark_stones} each"
            else:
                data["finished"] = f"{winner} won, Dark:{num_dark_stones}, Light:{num_light_stones}"

            current_player = "Dark "
            move_count = 60
            game_board = initialise_board()

    # Check if move count has expired
    if move_count == 0:
        data["status"] = "game over"

        # Determine game over output
        winner, num_dark_stones, num_light_stones = check_score(game_board)
        if winner == "Draw":
            data["finished"] = f"Draw, {num_dark_stones} each"
        else:
            data["finished"] = f"{winner} won, Dark: {num_dark_stones}, Light: {num_light_stones}"

        current_player = "Dark "
        move_count = 60
        game_board = initialise_board()

    data["board"] = game_board
    data["player"] = current_player
    data["move_count"] = move_count

    return jsonify(data)

if __name__ == "__main__":
    app.run()
