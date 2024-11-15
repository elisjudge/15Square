from . import _config as c
import numpy as np

class Board:
    def __init__(self, n_rows = c.N_ROWS, n_cols = c.N_COLS, seed=None) -> None:
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_cells = self.n_rows * self.n_cols
        self.target = self.n_cells
        self.target_index = self.n_cells - 1
        self.cells = self.generate_random_cells(seed)
        self.row_complete = [False] * self.n_rows
        self.valid_moves = self.set_valid_moves()

    def create_cells(self):
        starting_val = c.STARTING_VALUE
        cells = np.append(np.arange(starting_val, self.n_cells), None)
        return cells

    def generate_random_cells(self, seed):
        cells = self.create_cells()
        self.shuffle_cells(cells, seed)
        self.make_solvable(cells)
        return cells

    def get_e_row_number(self, cells):
        e = np.where(cells == None)[0][0]
        e_row = e // self.n_rows + 1
        return e_row    

    def make_solvable(self, cells):
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

    
    @staticmethod                    
    def count_inversions(cells):
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
