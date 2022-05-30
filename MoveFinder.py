import random
import numpy as np

piece_score = {"N": 3, "p": 10}
DEPTH = 2
CHECKMATE = 1000


def find_best_move(game_state, valid_moves):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    find_move_alpha(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if game_state.white_move else 0)
    return next_move


def find_move_alpha(game_state, valid_moves, depth, alpha, beta, turn_multipler):
    global next_move
    if depth == 0:
        return turn_multipler * score_board(game_state)

    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()
        score = - find_move_alpha(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multipler)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def find_random_move(valid_moves):
    return np.random.choice(valid_moves)


#  Positive for white wins, negatif is for black wins
def score_board(game_state):
    if game_state.is_finished:
        return -CHECKMATE if game_state.white_move else CHECKMATE

    score = 0
    for row in game_state.board:
        for square in row:
            if square[0] == "w":
                score += piece_score[square[1]]
            elif square[0] == "b":
                score += piece_score[square[1]]
    return score