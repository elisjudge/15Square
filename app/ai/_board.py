from . import _config as c
from ._utils import strict_cell_validation
import numpy as np

class Board:
    def __init__(self, n_rows = c.N_ROWS, n_cols = c.N_COLS, seed=None, strict=False) -> None:
        self._strict = strict
        self._n_rows = n_rows
        self._n_cols = n_cols
        self._n_cells = self._n_rows * self._n_cols
        self._cells = self.generate_random_cells(seed)
        self._target_index = self.set_target_index()
        self._row_complete = [False] * self._n_rows
        self._valid_moves = self.set_valid_moves()

    def generate_random_cells(self, seed):
        """ Intializes the board for the game """
        cells = np.append(np.arange(c.STARTING_VALUE, self.n_cells), None)
        self.shuffle_cells(cells, seed)
        self.make_solvable(cells)
        return cells

    def get_e_row_number(self, cells):
        """ Returns row number that contains the empty cell """
        e = np.where(cells == None)[0][0]
        e_row = e // self.n_rows + 1
        return e_row    

    def make_solvable(self, cells):
        """ Guarantees randomly shuffled board can be solved """
        inversions = self.count_inversions(cells)
        e_row = self.get_e_row_number(cells)
        solvability = inversions + e_row
        
        if solvability % 2 != 0:
            for i in range(len(cells) - 1):
                if cells[i] is not None and cells[i + 1] is not None:
                    cells[i], cells[i + 1] = cells[i + 1], cells[i]
                    break

    def set_priority_conditions(self):
        """Create a dictionary mapping row completion states to target cells."""
        priority_conditions = {}
    
        for idx in range(self.n_rows + 1):
            row_complete = [False] * self.n_rows
            if idx > 0:
                for row in range(0, idx):
                    row_complete[row] = True

            priority_conditions[tuple(row_complete)] =  []

        for i, condition in enumerate(priority_conditions):
            if i == 0:
                start_value = i * self.n_rows + 1
                end_value = i * self.n_rows + self.n_cols + 1
                target_values = [val for val in range(start_value, end_value)]
            
            elif i == self.n_rows:
                target_values = None

            elif i > 0:
                start_value = (i - 1) * self.n_rows + 1
                if i == self.n_rows - 1:
                    end_value = i * self.n_rows + self.n_cols
                else:
                    end_value = i * self.n_rows + self.n_cols + 1

                target_values = [val for val in range(start_value, end_value)]

            priority_conditions[condition] = target_values
            
        return priority_conditions
    
    def set_target_index(self):
        """Calculate and validate the position of the empty cell."""
        try:
            target_idx = np.where(self.cells == None)[0][0]
            if not (0 <= target_idx < self.n_cells):
                raise ValueError("Target index must be within the bounds of the board.")
            return target_idx
        except IndexError:
            raise Exception("Empty cell is missing from the array")

    def set_valid_moves(self):
        """ Builds the dictionary of valid moves in the game """
        valid_moves = {}
        for board_idx in range(self.n_cells):
            moves = {
                "slide_down": board_idx - self.n_rows if board_idx - self.n_rows >= 0 else None,
                "slide_up": board_idx + self.n_rows if board_idx + self.n_rows < self.n_cells else None,
                "slide_right": board_idx - 1 if board_idx % self.n_cols != 0 else None,
                "slide_left": board_idx + 1 if board_idx % self.n_cols != self.n_cols - 1 else None
            }
            valid_moves[board_idx] = {direction: move for direction, move in moves.items() if move is not None}
        return valid_moves
    
    @strict_cell_validation
    def update_cells(self, empty_cell, selection):
        """
        Swap two cells on the board.
        Validation is applied if strict mode is enabled.
        """
        self._cells[empty_cell], self._cells[selection] = self._cells[selection], self._cells[empty_cell]

        # Refresh the board state
        self._target_index = self.set_target_index()
        self.update_row_status()
    
    def update_row_status(self):
        """Recalculate which rows are complete."""
        for row_index in range(self.n_rows):
            if row_index == 0 or self.row_complete[row_index - 1]:
                start_index = row_index * self.n_cols
                end_index = start_index + self.n_cols
                row_values = self.cells[start_index:end_index]
                expected_values = np.arange(start_index + 1, end_index + 1)
                self.row_complete[row_index] = np.array_equal(row_values, expected_values)
            else:
                self.row_complete[row_index] = False
    
    @property
    def cells(self):
        """The current game board state"""
        return self._cells
    
    @property
    def n_cells(self):
        """Total cells on the board"""
        return self._n_cells
    
    @property
    def n_cols(self):
        """Number of columns on the board."""
        return self._n_cols
    
    @property
    def n_rows(self):
        """Number of rows on the board."""
        return self._n_rows
    
    @property
    def row_complete(self):
        """List indicating whether each row is complete"""
        return self._row_complete
    
    @property
    def strict(self):
        """ Determines whether strict validation of cell swap occurs """
        return self._strict
    
    @property
    def target_index(self):
        """Position of the the empty cell in array"""
        return self._target_index
    
    @property
    def valid_moves(self):
        """Dictionary of valid moves for the current board state."""
        return self._valid_moves
    
    @staticmethod                    
    def count_inversions(cells):
        """ Helper function to determine whether board is solvable or not """
        inversions = 0
        for i in range(len(cells)):
            if cells[i] is None:
                continue  # Skip the empty cell
            for j in range(i + 1, len(cells)):
                if cells[j] is not None and cells[i] > cells[j]:
                    inversions += 1
        return inversions
    
    @staticmethod    
    def shuffle_cells(cells, seed):
        """ Shuffles board base on seeding """
        if seed is not None:
            np.random.seed(seed) 

        np.random.shuffle(cells)

        if seed is not None:
            # Reset seed after shuffle if seed
            np.random.seed(None)
    
    def __repr__(self) -> str:
        reshaped = self.cells.reshape((self.n_rows, self.n_cols))

        # Using fixed width of 4 for each cell, ensuring alignment
        board_str = "\n".join(
            " ".join(f"{str(cell) if cell is not None else ' ':>4}" for cell in row)
            for row in reshaped
        )
        return board_str