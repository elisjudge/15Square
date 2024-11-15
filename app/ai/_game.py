from ._board import Board

class Game:
    def __init__(self, player, seed=None, strict=False) -> None:
        self.board = Board(seed=seed, strict=strict)
        self.player = player
        self.winner = False
        self.valid_moves = self.get_valid_moves()
        self.n_moves = 0
        self.priority_conditions = self.board.set_priority_conditions()
        
    def simulate_click(self, selection):
        self.swap_cells(self.board.target_index, selection)

    def swap_cells(self, empty_cell, selection):
        self.board.update_cells(empty_cell, selection)         
        self.valid_moves = self.get_valid_moves()
        self.winner = all(self.board.row_complete)

    def get_valid_moves(self):
        return self.board.valid_moves.get(self.board.target_index)