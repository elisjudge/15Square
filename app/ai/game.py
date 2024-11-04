import numpy as np
import random

from board import Board

class Game:
    def __init__(self, player) -> None:
        self.board = Board()
        self.player = player
        self.winner = False
        self.target_index = None
        self.board_shuffled = False
        self.shuffle_board()
        self.set_target_index()
        self.valid_moves = self.get_valid_moves()
        self.n_moves = 0
        
    def simulate_click(self, i):
        if not self.winner:
            if i - self.board.n_rows >= 0 and self.board.cells[i - self.board.n_rows] == self.board.target:
                self.swap_cells(i, i - self.board.n_rows)
            elif i + self.board.n_rows < self.board.n_cells and self.board.cells[i + self.board.n_rows] == self.board.target:
                self.swap_cells(i, i + self.board.n_rows)
            elif i % self.board.n_cols != 0 and self.board.cells[i - 1] == self.board.target:
                self.swap_cells(i, i - 1)
            elif i % self.board.n_cols != self.board.n_cols - 1 and self.board.cells[i + 1] == self.board.target:
                self.swap_cells(i, i + 1)

    def shuffle_board(self):
        for _ in range(1000):
            selection = random.randint(0, self.board.n_cells - 1)
            self.simulate_click(selection)
        self.board_shuffled = True

    def swap_cells(self, i, j):
        temp = self.board.cells[i]
        self.board.cells[i] = self.board.cells[j]
        self.board.cells[j] = temp

        if self.board_shuffled:
            self.set_target_index()
            self.valid_moves = self.get_valid_moves()
            self.board.update_row_status()
            self.winner = all(self.board.row_complete)

    def set_target_index(self):
        self.target_index = int(np.nonzero(self.board.cells == 16)[0][0])
    
    def get_valid_moves(self):
        return {
            "slide_down": self.target_index - self.board.n_rows if self.target_index - self.board.n_rows >= 0 else None,
            "slide_up": self.target_index + self.board.n_rows if self.target_index + self.board.n_rows < self.board.n_cells else None,
            "slide_right": self.target_index - 1 if self.target_index % self.board.n_cols != 0 else None,
            "slide_left": self.target_index + 1 if self.target_index % self.board.n_cols != self.board.n_cols - 1 else None
        }