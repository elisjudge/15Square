import numpy as np
import random

class Game():
    def __init__(self, N_ROWS = 4, N_COLS = 4) -> None:
        self.n_rows = N_ROWS
        self.n_cols = N_COLS
        self.n_cells = self.n_rows * self.n_cols
        self.target = self.n_cells
        self.target_index = self.n_cells - 1
        self.board = self.initialize_board()
        self.winning_tiles = self.board.copy()
        self.winner = False
        self.shuffle()
        self.find_target_index()
        self.valid_moves = self.get_valid_moves()

    def __repr__(self) -> str:
        pass

    def initialize_board(self):
        board = np.array(np.zeros(self.n_cells))
        value = 1
        for i in range(self.n_rows * self.n_cols):
                board[i] = value
                value += 1
        return board
    
    def click(self, i):
        if not self.winner:
            if i - self.n_rows >= 0 and self.board[i - self.n_rows] == self.target:
                self.swap(i, i - self.n_rows)
            elif i + self.n_rows < self.n_cells and self.board[i + self.n_rows] == self.target:
                self.swap(i, i + self.n_rows)
            elif i % self.n_cols != 0 and self.board[i - 1] == self.target:
                self.swap(i, i - 1)
            elif i % self.n_cols != self.n_cols - 1 and self.board[i + 1] == self.target:
                self.swap(i, i + 1)

    def shuffle(self):
        for _ in range(1000):
            selection = random.randint(0, self.n_cells - 1)
            self.click(selection)

    def swap(self, i, j):
        temp = self.board[i]
        self.board[i] = self.board[j]
        self.board[j] = temp

    def find_target_index(self):
        self.target_index = int(np.nonzero(self.board == 16)[0][0])
    
    def get_valid_moves(self):
        return {
            "up": self.target_index - self.n_rows if self.target_index - self.n_rows >= 0 else None,
            "down": self.target_index + self.n_rows if self.target_index + self.n_rows < self.n_cells else None,
            "left": self.target_index - 1 if self.target_index % self.n_cols != 0 else None,
            "right": self.target_index + 1 if self.target_index % self.n_cols != self.n_cols - 1 else None
        }

game = Game()
print(game.board)
game.find_target_index()
print(game.target_index)
print(game.valid_moves)