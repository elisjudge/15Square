import numpy as np
import config as c

class Board:
    def __init__(self, n_rows = c.N_ROWS, n_cols = c.N_COLS) -> None:
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_cells = self.n_rows * self.n_cols
        self.target = self.n_cells
        self.target_index = self.n_cells - 1
        self.cells = self.create_cells()
        self.row_complete = [False] * self.n_rows
        self.valid_moves = self.set_valid_moves()


    def create_cells(self):
        cells = np.array(np.zeros(self.n_cells))
        value = c.STARTING_VALUE
        for i in range(self.n_rows * self.n_cols):
                cells[i] = value
                value += 1
        return cells
    
    def update_row_status(self):
        for row_index in range(self.n_rows):
            if row_index == 0 or self.row_complete[row_index - 1]:
                start_index = row_index * self.n_cols
                end_index = start_index + self.n_cols
                row_values = self.cells[start_index:end_index]
                expected_values = np.arange(start_index + 1, end_index + 1)
                self.row_complete[row_index] = np.array_equal(row_values, expected_values)
            else:
                self.row_complete[row_index] = False

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

    def set_valid_moves(self):
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

    def __repr__(self) -> str:
        return str(self.cells.reshape((self.n_rows, self.n_cols)))