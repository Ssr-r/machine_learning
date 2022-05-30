from collections import defaultdict


class GameState:
    def __init__(self):
        self.board = [
            ["--", "--", "bN", "--", "--", "bN", "--", "--"],
            ["--", "--", "--", "bp", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "wp", "--", "--", "--", "--"],
            ["--", "--", "wN", "--", "--", "wN", "--", "--"]
        ]
        self.move_functions = {'p': self.get_pawn_moves, 'N': self.get_knight_moves}

        self.white_move = True
        self.move_log = []
        self.remain_moves = {}
        self.remain_pieces = {'w': [], 'b': []}
        self.color_map = {"w": True, "b": False}
        self.is_finished = False
        self.is_draw = False

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_move = not self.white_move  # swap players
        #  Pawn promotion

    def check_promotion(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if row == 0 and self.board[row][col][0] == "w" or row == 7 and self.board[row][col][0] == "b":
                    self.is_finished = True

    def check_draw(self, valid_moves):
        self.get_remain_moves(valid_moves)
        opp_color = "w" if self.white_move else "b"
        if len(self.remain_moves[opp_color]) == 0 and len(self.remain_pieces[opp_color]) >= 1 and not self.is_finished:
            self.is_draw = True

    def get_remain_moves(self, valid_moves):
        if not self.is_draw and not self.is_finished:
            self.remain_moves = {}
            for color in self.color_map.keys():
                remains = defaultdict(str)
                for move in valid_moves:
                    remains[move.get_chess_notation()] = move.get_rank()
                _color = "w" if self.white_move else "b"
                self.remain_moves[_color] = remains
                self.white_move = not self.white_move

    def get_remain_pieces(self):
        if not self.is_draw and not self.is_finished:
            self.remain_pieces = {'w': [], 'b': []}
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    if self.board[row][col] != "--" and self.board[row][col][0] == "w":
                        self.remain_pieces['w'].append(self.board[row][col])
                    elif self.board[row][col] != "--" and self.board[row][col][0] == "b":
                        self.remain_pieces['b'].append(self.board[row][col])
            if len(self.remain_pieces["w"]) == 0 or len(self.remain_pieces["b"]) == 0:
                self.is_finished = True

    def undo_move(self):
        if len(self.move_log) != 0:  # Make sure its not first move!
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_move = not self.white_move

    def get_valid_moves(self):
        moves = self.get_all_possible_moves()
        return moves

    def get_all_possible_moves(self):
        # All moves w/ considering checks
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]  # Returns w, b or -
                if (turn == "w" and self.white_move) or (turn == "b" and not self.white_move):
                    piece = self.board[row][col][1]  # Returns p or N
                    self.move_functions[piece](row, col, moves)
        return moves

    def get_pawn_moves(self, row, col, moves):
        if self.white_move:
            if self.board[row - 1][col] == "--":  # 1 square advanced
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == "--":
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0:  # Capture left
                if self.board[row - 1][col - 1][0] == "b":  # Enemy piece to capture
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
            if col + 1 <= 7:  # Capture right
                if self.board[row - 1][col + 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
        else:  # Black pawns
            if self.board[row + 1][col] == "--":  # 1 square advanced
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--":
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0:  # Capture left
                if self.board[row + 1][col - 1][0] == "w":  # Enemy piece to capture
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if col + 1 <= 7:  # Capture right
                if self.board[row + 1][col + 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def get_knight_moves(self, row, col, moves):
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, 2), (1, -2), (2, -1), (2, 1))
        ally_color = "w" if self.white_move else "b"
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))


class Move:
    # Map keys to vals -> h8 = top row, last col
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {value: key for key, value in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {value: key for key, value in files_to_cols.items()}

    def __init__(self, start_square, end_square, board):
        self.board = board
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_promotion = False
        if (self.piece_moved == "wp" and self.end_row == 0) or (self.piece_moved == "bp" and self.end_row == 7):
            self.is_promotion = True
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    # Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return (self.get_rank_file(self.start_row, self.start_col)
                + self.get_rank_file(self.end_row, self.end_col))

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def get_rank(self):
        return self.board[self.start_row][self.start_col]
