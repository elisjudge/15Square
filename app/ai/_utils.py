import time
import functools

def timeit(func):
    """Decorator to measure the execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"Starting '{func.__name__}'...")
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"'{func.__name__}' completed in {elapsed_time:.2f} seconds.")
        
        return result
    return wrapper

def strict_cell_validation(func):
    """Decorator to perform strict validation of cell updates"""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if getattr(self, 'strict', True):
            empty_cell, selection = args[:2] 
            if not (0 <= empty_cell < self.n_cells):
                raise ValueError(f"Invalid empty_cell index: {empty_cell}. Must be between 0 and {self.n_cells - 1}.")
            if not (0 <= selection < self.n_cells):
                raise ValueError(f"Invalid selection index: {selection}. Must be between 0 and {self.n_cells - 1}.")
            if self._cells[empty_cell] is not None:
                raise ValueError(f"Cell at index {empty_cell} is not empty. It contains {self._cells[empty_cell]}.")
            valid_moves = self.valid_moves.get(empty_cell, {})
            if selection not in valid_moves.values():
                raise ValueError(f"Selection {selection} is not a valid move for empty_cell at index {empty_cell}.")

        return func(self, *args, **kwargs)
    return wrapper