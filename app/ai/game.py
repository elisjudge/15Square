import numpy as np
import random

from board import Board
from base_ai import BaseAI

class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.player = BaseAI()
        self.winner = False
        self.target_index = None
        self.board_shuffled = False
        self.shuffle_board()
        self.set_target_index()
        self.valid_moves = self.get_valid_moves()
        
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

game = Game()
print("Initial Game State")
print(game.board)
print(game.target_index)
print(game.valid_moves)
print(game.board.row_complete)
print(game.winner)
print()
print("Player Makes Random Selection")
current_move = game.player.select_move(valid_moves = game.valid_moves)
print(current_move)
game.simulate_click(current_move)

print("New Game State")
print(game.board)
print(game.target_index)
print(game.valid_moves)
print(game.board.row_complete)
print(game.winner)
print()

