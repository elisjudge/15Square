import numpy as np
import random

N_ROWS = 4
N_COLS = 4

class Game():
    def __init__(self) -> None:
        self.board = self.initialize_board()
        self.winning_tiles = self.board.copy()
        self.winner = False
        self.shuffle()

    def __repr__(self) -> str:
        pass

    def initialize_board(self):
        board = np.array(np.zeros(N_COLS*N_ROWS))
        value = 1
        for i in range(N_ROWS * N_COLS):
                board[i] = value
                value += 1
        return board
    
    def click(self, i):
        if not self.winner:
            if i - N_ROWS >= 0 and self.board[i - 4] == 16:
                self.swap(i, i - 4)
            elif i + N_ROWS < 16 and self.board[i + 4] == 16:
                self.swap(i, i + 4)
            elif i % N_COLS != 0 and self.board[i - 1] == 16:
                self.swap(i, i - 1)
            elif i % N_COLS != 3 and self.board[i + 1] == 16:
                self.swap(i, i + 1)

    def shuffle(self):
        for _ in range(1000):
            selection = random.randint(0, 15)
            self.click(selection)

    def swap(self, i, j):
        temp = self.board[i]
        self.board[i] = self.board[j]
        self.board[j] = temp

game = Game()