import config as c
import numpy as np
import random

from board import Board

class Game:
    def __init__(self, player, seed=None) -> None:
        self.board = Board()
        self.player = player
        self.winner = False
        self.target_index = self.set_target_index()
        self.valid_moves = self.get_valid_moves()
        self.board_shuffled = False
        self.shuffle_board(seed=seed)
        self.n_moves = 0
        self.priority_conditions = self.board.set_priority_conditions()
        
    def simulate_click(self, selection):
        if not self.winner:
            self.swap_cells(self.target_index, selection)

    def shuffle_board(self, seed=None):
        if seed is not None:
            random.seed(seed) 
        
        for _ in range(c.N_SHUFFLES):
            valid_move_indices = [move for move in self.valid_moves.values()]
            selection = random.choice(valid_move_indices)
            self.simulate_click(selection)

        if seed is not None:
            random.seed()
        
        self.board_shuffled = True

    def swap_cells(self, empty_cell, selection):
        self.board.cells[empty_cell], self.board.cells[selection] = self.board.cells[selection], self.board.cells[empty_cell]
        self.target_index = selection
        self.valid_moves = self.get_valid_moves()

        if self.board_shuffled:
            self.board.update_row_status()
            self.winner = all(self.board.row_complete)

    def set_target_index(self):
        return int(np.nonzero(self.board.cells == self.board.n_cells)[0][0])
    
    def get_valid_moves(self):
        return self.board.valid_moves.get(self.target_index)