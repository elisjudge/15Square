from . import _config as c
from ._board import Board

import numpy as np
import random


class Game:
    def __init__(self, player, seed=None) -> None:
        self.board = Board(seed=seed)
        self.player = player
        self.winner = False
        self.target_index = self.set_target_index()
        self.valid_moves = self.get_valid_moves()
        self.n_moves = 0
        self.priority_conditions = self.board.set_priority_conditions()
        
    def simulate_click(self, selection):
        self.swap_cells(self.target_index, selection)

    def swap_cells(self, empty_cell, selection):
        self.board.cells[empty_cell], self.board.cells[selection] = self.board.cells[selection], self.board.cells[empty_cell]
        self.target_index = selection
        self.valid_moves = self.get_valid_moves()
        self.board.update_row_status()
        self.winner = all(self.board.row_complete)

    def set_target_index(self):
        return np.where(self.board.cells == None)[0][0]
    
    def get_valid_moves(self):
        return self.board.valid_moves.get(self.target_index)