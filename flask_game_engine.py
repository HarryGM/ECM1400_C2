from flask import Flask, render_template, request, jsonify
from components import *

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

    if (board[new_pos[1]][new_pos[0]] != current_player):
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
        else:
            continue
        break

    return move_available

board = initialise_board(4)

# Define data for response object
data = {
    "board" : None,
    "status" : None,
    "player" : "Dark ",
    "finished" : None,
    "move_count" : 60
}

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", game_board = board)

@app.route("/move", methods = ["GET"])
def move():
    x = int(request.args.get("x")) - 1
    y = int(request.args.get("y")) - 1
    current_player = data["player"]
    move_count = data["move_count"]
    data["status"] = "success"

    if not any_legal_moves(board, current_player):
        data["player"] = current_player
        data["status"] = "fail"
        data["message"] = f"No legal moves for {current_player}"
        current_player = swap_player(current_player)
        if not any_legal_moves(board, current_player):
            data["finished"] = "Game is over"
            data["player"] = "Dark "
            data["board"] = initialise_board()
            return jsonify(data)

    if legal_move(board, (x, y), current_player):
        data["status"] = "success"
        board[y][x] = current_player

        # Change outflanked stones
        valid_directions = check_outflanks(board, (x, y), current_player)[1]
        print(valid_directions)
        for direction in valid_directions:
            change_outflanked_stones(board, (x, y), current_player, direction)

        move_count -= 1
        current_player = swap_player(current_player)
    else:
        data["status"] = "fail"
        data["message"] = "illegal move"

    data["board"] = board
    data["player"] = current_player
    data["move_count"] = move_count

    return jsonify(data)


if __name__ == "__main__":
    app.run()
