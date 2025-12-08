""" 
tests.py module:
contains unit tests for project
"""

from components import *
from flask_game_engine import *
from othello_opponent import *

def tests() -> None:
    """ unit tests """

    # Test initialise_board
    assert initialise_board() == [["None ", "None ", "None ", "None ", "None ", "None ", "None ", "None "], 
                                 ["None ", "None ", "None ", "None ", "None ", "None ", "None ", "None "], 
                                 ["None ", "None ", "None ", "None ", "None ", "None ", "None ", "None "], 
                                 ["None ", "None ", "None ", "Light", "Dark ", "None ", "None ", "None "],
                                 ["None ", "None ", "None ", "Dark ", "Light", "None ", "None ", "None "],
                                 ["None ", "None ", "None ", "None ", "None ", "None ", "None ", "None "],
                                 ["None ", "None ", "None ", "None ", "None ", "None ", "None ", "None "],
                                 ["None ", "None ", "None ", "None ", "None ", "None ", "None ", "None "]]

    assert initialise_board(4) == [["None ", "None ", "None ", "None "],
                                   ["None ", "Light", "Dark ", "None "],
                                   ["None ", "Dark ", "Light", "None "],
                                   ["None ", "None ", "None ", "None "],]

    # Skipping print_board as it has no return value

    # Test legal_move:
    assert legal_move(initialise_board(), (2, 3), "Dark ") == True
    assert legal_move(initialise_board(), (0, 0), "Dark") == False
    assert legal_move(initialise_board(4), (3, 1), "Light") == True

    # Test check_outflanks
    assert check_outflanks(initialise_board(), (2, 3), "Dark ") == (True, [(1, 0)])
    assert check_outflanks(initialise_board(), (2, 4), "Light") == (True, [(1, 0)])
    assert check_outflanks(initialise_board(4), (0, 3), "Dark") == (False, None)

    # Test check_adjacent
    assert check_adjacent(initialise_board(), (2, 3) , (1, 0), "Dark ", "Light") == True
    assert check_adjacent(initialise_board(4), (1, 3) , (0, -1), "Light", "Dark ") == True
    assert check_adjacent(initialise_board(), (0, 0), (-1,-1), "Dark ", "Light") == False 
    assert check_adjacent(initialise_board(), (0, 0), (1, 0), "Dark ", "Light") == False

    # Test check_match_in_direction
    assert check_match_in_direction(initialise_board(), (3, 3) , (1, 0), "Dark ", "Light") == True
    assert check_match_in_direction(initialise_board(4), (1, 2) , (0, -1), "Light", "Dark ") == True
    assert check_match_in_direction(initialise_board(4), (2, 3) , (1, 0), "Light", "Dark ") == False

    # Test swap_player
    assert swap_player("Light") == "Dark "
    assert swap_player("Dark ") == "Light"

    # Skipping change_outflanked_stones as return value is unused

    # Test any_legal_moves
    assert any_legal_moves(initialise_board(), "Light") == True
    assert any_legal_moves(initialise_board(), "Dark ") == True
    assert any_legal_moves(initialise_board(2), "Dark ") == False

    # Test check_score
    assert check_score(initialise_board()) == ("Draw", 2, 2)
    assert check_score([["None ", "None ", "None ", "None "],
                        ["None ", "Dark ", "Dark ", "None "],
                        ["None ", "None ", "Light", "Dark "],
                        ["None ", "None ", "None ", "None "]]) == ("Dark ", 3, 1)

    # Test all_legal_moves
    for move in all_legal_moves(initialise_board(), "Dark "):
        assert move in [(3, 2), (2, 3), (4, 5), (5, 4)]

    # Test predict_move
    assert predict_move(initialise_board(), "Light") == (4, 2)
    assert predict_move(initialise_board(), "Dark ") == (3, 2)

if __name__ == "__main__":
    try:
        tests()
    except AssertionError as message:
        print("Assertion Error: ")
        print(message)

