from flask import Flask, render_template

app = Flask(__name__)
@app.route("/<game_board>")
def index(game_board):
    return render_template("index.html", game_board = game_board)

if __name__ == "__main__":
    app.run()
