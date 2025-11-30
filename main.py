from components import *
from game_engine import *

board = initialise_board()
print(legal_move(board, (5, 4), "Dark"))
print(cli_coords_input())
