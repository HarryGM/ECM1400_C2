from components import *
import copy

def swap_player(current_player):
    if current_player == "Dark ":
        current_player = "Light"
    else:
        current_player = "Dark "
    return current_player

def all_legal_moves(board, player):
    legal_moves = []

    for y in range(len(board)):
        for x in range(len(board)):
            if legal_move(board, (x, y), player):
                legal_moves.append((x, y))

    return legal_moves

def change_outflanked_stones(board, move, current_player, direction):
    x = move[0]
    y = move[1]

    new_pos = (x + direction[0], y + direction[1])

    if board[new_pos[1]][new_pos[0]] != current_player:
        board[new_pos[1]][new_pos[0]] = current_player
        change_outflanked_stones(board, new_pos, current_player, direction)
    else:
        return board

def predict_move(game_board, player):
    legal_moves = all_legal_moves(game_board, player)
    if len(legal_moves) == 0:
        return None

    resulting_boards = []
    # Compute all resulting boards from all legal moves
    for move in legal_moves:
        board_tmp = copy.deepcopy(game_board)
        valid_directions = check_outflanks(board_tmp, move, player)[1]
        for direction in valid_directions:
            change_outflanked_stones(board_tmp, move, player, direction)
        resulting_boards.append(board_tmp)

    resulting_legal_moves_counts = []
    for board_state in resulting_boards:
        resulting_legal_moves_counts.append(len(all_legal_moves(board_state, swap_player(player))))

    # Find move which results in least possible number of moves for black
    move_index = resulting_legal_moves_counts.index(min(resulting_legal_moves_counts))
    return legal_moves[move_index]
