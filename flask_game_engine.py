import os
import json

from flask import Flask, render_template, request, jsonify
from components import *
from othello_opponent import predict_move

# Define some useful functions from game_engine.py
def swap_player(current_player):
    if current_player == "Dark ":
        current_player = "Light"
    else:
        current_player = "Dark "
    return current_player

def change_outflanked_stones(board, move, current_player, direction):
    x = move[0]
    y = move[1]
    
    new_pos = (x + direction[0], y + direction[1])

    if board[new_pos[1]][new_pos[0]] != current_player:
        board[new_pos[1]][new_pos[0]] = current_player
        change_outflanked_stones(board, new_pos, current_player, direction)
    else:
        return board

def any_legal_moves(board, current_player):
    move_available = False
    for y in range(len(board)):
        for x in range(len(board)):
            if legal_move(board, (x, y), current_player):
                move_available = True
                break

    return move_available

def check_score(board):
    num_dark_stones = 0
    num_light_stones = 0

    for row in board:
        num_dark_stones += row.count("Dark ")
        num_light_stones += row.count("Light")

    if num_dark_stones > num_light_stones:
        winner = "Dark "
    elif num_light_stones >  num_dark_stones:
        winner = "Light"
    else:
        winner = "Draw"
    return winner, num_dark_stones, num_light_stones

board = initialise_board(4)

# Define data for response object
data = {
    "board" : board,
    "status" : None,
    "player" : "Dark ",
    "finished" : None,
    "move_count" : 60,
    "bot_move": None
}

app = Flask(__name__)

# Render template
@app.route("/")
def index():
    return render_template("index.html", game_board = board)

# Save route
@app.route("/save", methods = ["POST"])
def save():
    save_data = request.get_json()
    save_dir = "othello_saves"
    files_in_dir = 0

    save_data["player"] = data["player"]
    save_data["move_count"] = data["move_count"]

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for path in os.listdir(save_dir):
        # check if current path is a file
        if os.path.isfile(os.path.join(save_dir, path)):
            files_in_dir += 1
    try:
        with open(f"{save_dir}/save_{files_in_dir + 1}.json", "x") as f:
            try:
                json.dump(save_data, f)
                return "success"
            except:
                return "failed to write to the file"
    except:
        return "failed to open file"

# Load route
@app.route("/load", methods = ["POST"])
def load():
    load_data_loc = request.get_json()
    save_dir = "othello_saves"

    # retrieve save data
    with open(f"{save_dir}/{load_data_loc["file_name"]}", "r") as f:
        load_data = json.load(f)

    # Set variables for use in backend
    data["board"] = load_data["board"]
    data["player"] = load_data["player"]
    data["move_count"] = load_data["move_count"]

    # set response data to change board
    response_data = {
        "board": load_data["board"],
        "player": load_data["player"],
        "move_count": load_data["move_count"]
                     }

    return jsonify(response_data)

# Bot route
@app.route("/bot", methods = ["GET"])
def bot():
    if data["player"] == "Light":
        board = data["board"]
        data["finished"] = None
        current_player = data["player"]
        move_count = data["move_count"]
        x, y = predict_move(board, "Light")

        board[y][x] = "Light"
        valid_directions = check_outflanks(board, (x, y), "Light")[1]
        for direction in valid_directions:
            change_outflanked_stones(board, (x, y), "Light", direction)
        move_count -= 1

        # Check if the next player has any legal moves
        if not any_legal_moves(board, swap_player(current_player)):
            current_player = swap_player(current_player)
            # Check if the other player has any legal moves
            if not any_legal_moves(board, current_player):
                data["status"] = "game over"
                print("TEST")
                # Determine game over output
                winner, num_dark_stones, num_light_stones = check_score(board)
                if winner == "Draw":
                    data["finished"] = f"Draw, {num_dark_stones} each"
                else:
                    data["finished"] = f"{winner} won, Dark: {num_dark_stones}, Light: {num_light_stones}"

                current_player = "Dark "
                move_count = 60
                board = initialise_board(4)
    
        # Check if move count has expired
        if move_count == 0:
            data["status"] = "game over"

            # Determine game over output
            winner, num_dark_stones, num_light_stones = check_score(board)
            if winner == "Draw":
                data["finished"] = f"Draw, {num_dark_stones} each"
            else:
                data["finished"] = f"{winner} won, Dark: {num_dark_stones}, Light: {num_light_stones}"

            current_player = "Dark "
            move_count = 60
            board = initialise_board(4)

        data["board"] = board
        data["move_count"] = move_count
        data["player"] = "Dark "
        data["bot_move"] = (x, y)

        return jsonify(data)
    else:
        return "No legal moves"

# Move route
@app.route("/move", methods = ["GET"])
def move():
    x = int(request.args.get("x")) - 1
    y = int(request.args.get("y")) - 1
    current_player = data["player"]
    move_count = data["move_count"]
    board = data["board"]
    data["status"] = "success"
    data["finished"] = None

    if legal_move(board, (x, y), current_player):
        data["status"] = "success"
        board[y][x] = current_player

        # Change outflanked stones
        valid_directions = check_outflanks(board, (x, y), current_player)[1]
        for direction in valid_directions:
            change_outflanked_stones(board, (x, y), current_player, direction)

        move_count -= 1
        current_player = swap_player(current_player)
    else:
        data["status"] = "fail"
        data["message"] = "illegal move"

    # Check if the next player has any legal moves
    if not any_legal_moves(board, current_player):
        current_player = swap_player(current_player)
        # Check if the other player has any legal moves
        if not any_legal_moves(board, current_player):
            data["status"] = "game over"
            # Determine game over output
            winner, num_dark_stones, num_light_stones = check_score(board)
            if winner == "Draw":
                data["finished"] = f"Draw, {num_dark_stones} each"
            else:
                data["finished"] = f"{winner} won, Dark: {num_dark_stones}, Light: {num_light_stones}"

            current_player = "Dark "
            move_count = 60
            board = initialise_board(4)

    # Check if move count has expired
    if move_count == 0:
        data["status"] = "game over"

        # Determine game over output
        winner, num_dark_stones, num_light_stones = check_score(board)
        if winner == "Draw":
            data["finished"] = f"Draw, {num_dark_stones} each"
        else:
            data["finished"] = f"{winner} won, Dark: {num_dark_stones}, Light: {num_light_stones}"

        current_player = "Dark "
        move_count = 60
        board = initialise_board(4)

    data["board"] = board
    data["player"] = current_player
    data["move_count"] = move_count

    return jsonify(data)

if __name__ == "__main__":
    app.run()
