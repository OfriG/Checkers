import pygame
from .constants import RED, WHITE, BLUE, GREEN, SQUARE_SIZE
from checkers.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.boost_used = {RED: False, WHITE: False}
        self.boost_just_used = {RED: False, WHITE: False}
        self.twice_used = {RED: False, WHITE: False}  # Whether the player has already used Twice
        self.twice_pending = {RED: False, WHITE: False}  # Whether there's a possibility for an extra turn now
        self.just_got_king = False
        self.winner_color = None
        self.board = Board()  # Ensure board is initialized
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        self.boost_used = {RED: False, WHITE: False}
        self.boost_just_used = {RED: False, WHITE: False}
        self.twice_used = {RED: False, WHITE: False}
        self.twice_pending = {RED: False, WHITE: False}
        self.just_got_king = False
        self.winner_color = None

    def winner(self):
        if self.board is None:
            return None
        w = self.board.winner()
        if w is not None:
            self.winner_color = w
        return w

    def reset(self):
        self._init()

    def select(self, row, col, use_boost=False, use_twice=False):
        if self.selected:
            result = self._move(row, col, use_boost, use_twice)
            if not result:
                self.selected = None
                self.select(row, col, use_boost, use_twice)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece is not None and piece.color == self.turn:
            self.selected = piece
            allow_boost = (not self.boost_used[self.turn] and use_boost)
            self.valid_moves = self.board.get_valid_moves(piece, allow_boost=allow_boost)
            return True
        return False

    def _move(self, row, col, use_boost=False, use_twice=False):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            was_king = self.selected.king
            is_boost_move = use_boost and not self.boost_used[self.turn] and abs(self.selected.row - row) == 2
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)

            # If this was a Boost move
            if is_boost_move:
                self.boost_used[self.turn] = True
                self.boost_just_used[self.turn] = True
            else:
                self.boost_just_used[self.turn] = False

            # If this was a Twice move
            if use_twice and not self.twice_used[self.turn] and skipped:  # Only if there was a capture
                self.twice_used[self.turn] = True
                self.twice_pending[self.turn] = True
                return True

            # If got crowned as king
            if not was_king and self.selected.king:
                self.just_got_king = True
            else:
                self.just_got_king = False

            # Change turn if not in Twice mode
            if not self.twice_pending[self.turn]:
                self.change_turn()
            else:
                self.twice_pending[self.turn] = False  # Cancel Twice after it's been used
        else:
            return False
        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            # בודק אם זה מהלך Boost רק אם יש חייל נבחר
            color = BLUE
            if self.selected:
                is_boost = abs(self.selected.row - row) == 2 and abs(self.selected.col - col) == 2
                color = GREEN if is_boost else BLUE
            pygame.draw.circle(self.win, color, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()