import numpy as np

STARTING_VALUE = 1

class Board:
    def __init__(self, N_ROWS = 4, N_COLS = 4) -> None:
        self.n_rows = N_ROWS
        self.n_cols = N_COLS
        self.n_cells = self.n_rows * self.n_cols
        self.target = self.n_cells
        self.target_index = self.n_cells - 1
        self.cells = self.create_cells()
        self.row_complete = [False] * self.n_rows

    def create_cells(self):
        cells = np.array(np.zeros(self.n_cells))
        value = STARTING_VALUE
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

    def __repr__(self) -> str:
        return str(self.cells.reshape((self.n_rows, self.n_cols)))
    
    