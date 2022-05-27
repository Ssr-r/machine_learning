from pickle import FALSE
from sqlite3 import Row
import chess
import pygame, sys
import _helper



WIDTH = HEIGHT = 600
DIM = 8
SQ_SIZE = HEIGHT // DIM
MAX_FPS = 15
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
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pygame.Color('white'))
    game_state = _helper.GameState()
    valid_moves = game_state.get_valid_moves()
    #  for i in valid_moves: print(i.get_chess_notation())
    move_made = False # Flag var for when a move is made

    # load images need to called once before loop
    load_images()

    selected_square = () # Inıtal empty square (row, col)
    player_clicks = [] # Keep tracks of user clicks. [(two tuple)]
    RUN_FLAG = True
    while RUN_FLAG:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN_FLAG = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                row = location[1] // SQ_SIZE
                col = location[0] // SQ_SIZE
                if selected_square == (row, col): # Click same square
                    selected_square = () # Deselect
                    player_clicks = [] # Empty clicks
                else:
                    selected_square = (row, col)
                    player_clicks.append(selected_square)
                if len(player_clicks) == 2:
                    move = _helper.Move(player_clicks[0], player_clicks[1], game_state.board)
                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            game_state.make_move(valid_moves[i])
                            print("Değiştik!")
                            move_made = True
                            #  for i in game_state.board: print(i) # for print board
                            selected_square = () # Reset user clicks
                            player_clicks = []
                    if not move_made:
                        player_clicks = [selected_square]
            #  Key handlers
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z: # undo last move when pressed "z"
                    game_state.undo_move()
                    move_made = True
            if move_made:
                valid_moves = game_state.get_valid_moves()
                move_made = False
        draw_game_state(screen, game_state)
        pygame.display.flip()

def draw_game_state(screen, game_state):
    draw_board(screen),
    draw_pieces(screen, game_state.board)


# Draws current state of board
def draw_board(screen):
    colors = [pygame.Color('white'), pygame.Color('gray')]
    for row in range(DIM):
        for col in range(DIM):
            color = colors[((row+col) % 2)]
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
    main()