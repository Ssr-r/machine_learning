import pygame
import sys
import time

import MoveFinder
import _helper

WIDTH = HEIGHT = 600
DIM = 8
SQ_SIZE = HEIGHT // DIM
MAX_FPS = 15
ROUND_LIMIT = 32
IMAGES = {}


#  Will be called once for load images

def load_images():
    pieces = ['wp', 'bp', 'wN', 'bN']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(
            pygame.image.load(f"images/{piece}.png"),
            (SQ_SIZE, SQ_SIZE)
        )


# Main driver for input and updating
def main(round_limit=ROUND_LIMIT, train=False, player_one=False, player_two=False):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('white'))
    game_state = _helper.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False  # Flag var for when a move is made
    # load images need to called once before loop
    load_images()
    selected_square = ()  # Initial empty square (row, col)
    player_clicks = []  # Keep tracks of user clicks. [(two tuple)]
    RUN_FLAG = True
    game_over = False
    player_one = player_one  # If human plays white, true, AI plays white False
    player_two = player_two  # Same for above
    current_round = 0
    while RUN_FLAG:
        time.sleep(0.5)
        human_turn = (game_state.white_move and player_one) or (not game_state.white_move and player_two)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN_FLAG = False
                sys.exit()
            #  mouse handlers
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = pygame.mouse.get_pos()
                    row = location[1] // SQ_SIZE
                    col = location[0] // SQ_SIZE
                    if selected_square == (row, col):  # Click same square
                        selected_square = ()  # Deselect
                        player_clicks = []  # Empty clicks
                    else:
                        selected_square = (row, col)
                        player_clicks.append(selected_square)
                    if len(player_clicks) == 2:
                        move = _helper.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.make_move(valid_moves[i])
                                move_made = True
                                current_round += 1
                                #  print(move.get_chess_notation())
                                #  for i in game_state.board: print(i) # for print board
                                selected_square = ()  # Reset user clicks
                                player_clicks = []
                        if not move_made:
                            player_clicks = [selected_square]
            #  Key handlers
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:  # undo last move when pressed "z"
                    game_state.undo_move()
                    move_made = True
                    current_round -= 1
                if event.key == pygame.K_r:  # Reset board when pressed "r"
                    game_state = _helper.GameState()
                    valid_moves = game_state.get_valid_moves()
                    selected_square = ()
                    player_clicks = []
                    move_made = False
                    current_round = 0

        # AI move finder
        if not game_over and not human_turn:
            ai_move = MoveFinder.find_best_move(game_state, valid_moves)
            if ai_move is None:
                ai_move = MoveFinder.find_random_move(valid_moves)
            game_state.make_move(ai_move)
            move_made = True
            current_round += 1

        if move_made:
            valid_moves = game_state.get_valid_moves()
            game_state.get_remain_pieces()
            game_state.check_draw(valid_moves)
            game_state.check_promotion()
            move_made = False

        if game_state.is_finished:
            game_over = True
            if not game_state.white_move:
                print("Beyaz Kazandı")
                main()
            else:
                print("Siyah Kazandı")
                main()

        if game_state.is_draw or current_round >= ROUND_LIMIT:
            game_over = True
            print("Draw!")
            main()

        draw_game_state(screen, game_state, valid_moves, selected_square)
        clock.tick(MAX_FPS)
        pygame.display.flip()


#  Highlight possible moves for selected piece
def highlight_squared(screen, game_state, valid_moves, selected_square):
    if selected_square != ():
        row, col = selected_square
        if game_state.board[row][col][0] == ("w" if game_state.white_move else "b"):
            surface = pygame.Surface((SQ_SIZE, SQ_SIZE))
            surface.set_alpha(50)  # 0 for transparency, 255 for full opaque
            surface.fill(pygame.Color('blue'))
            screen.blit(surface, (col * SQ_SIZE, row * SQ_SIZE))
            surface.fill(pygame.Color('yellow'))
            _valid_moves = [move for move in valid_moves if move.start_row == row and move.start_col == col]
            for move in _valid_moves:
                screen.blit(surface, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))


def draw_game_state(screen, game_state, valid_moves, selected_square):
    draw_board(screen)
    highlight_squared(screen, game_state, valid_moves, selected_square)
    draw_pieces(screen, game_state.board)


# Draws current state of board
def draw_board(screen):
    colors = [pygame.Color('white'), pygame.Color('gray')]
    for row in range(DIM):
        for col in range(DIM):
            color = colors[((row + col) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(
                col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE
            ))


# Draws pi state of pieces to board
def draw_pieces(screen, board):
    for row in range(DIM):
        for col in range(DIM):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(
                    col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE
                ))


if __name__ == "__main__":
    main(player_one=False, player_two=False)
