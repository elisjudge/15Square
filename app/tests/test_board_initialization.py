import unittest
import ai

class TestBoardInitialization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n Running Board Initialization Tests... \n")
    
    def setUp(self):
        self.test_board = ai.Board()
        self.default_n_rows = 4
        self.default_n_columns = 4
        self.default_n_cells = self.default_n_rows * self.default_n_columns

    def test_1_initialization_properties(self):
        self.assertTrue(hasattr(self.test_board, "n_rows"), "GameBoard should have property 'n_rows'.")
        self.assertTrue(hasattr(self.test_board, "n_cols"), "GameBoard should have property 'n_cols'.")
        self.assertTrue(hasattr(self.test_board, "n_cells"), "GameBoard should have property 'n_cells'.")
        self.assertTrue(hasattr(self.test_board, "target_index"), "GameBoard should have property 'target_index'.")
        ### ADD MORE ATTRIBUTES

    def test_2_initialization_methods(self):
        pass

    def test_3_initialization_default_dimensions(self):
        self.assertEqual(self.test_board.n_rows, self.default_n_rows, f"Default rows should equal {self.default_n_rows}")
        self.assertEqual(self.test_board.n_cols, self.default_n_columns, f"Default columns should equal {self.default_n_columns}")
        self.assertEqual(self.test_board.n_cells, self.default_n_cells, f"Default number of cells on {self.default_n_rows}x{self.default_n_columns} board should be {self.default_n_cells}")
    
    def test_4_initialization_custom_dimensions(self):
        custom_n_rows = 5
        custom_n_cols = 6
        custom_n_cells = custom_n_rows * custom_n_cols
        
        test_board = ai.Board(n_rows=custom_n_rows, n_cols=custom_n_cols)
        self.assertEqual(test_board.n_rows, custom_n_rows, f"Default rows should equal {custom_n_rows}")
        self.assertEqual(test_board.n_cols, custom_n_cols, f"Default columns should equal {custom_n_cols}")
        self.assertEqual(test_board.n_cells, custom_n_cells, f"Default number of cells on {custom_n_rows}x{custom_n_cols} board should be {custom_n_cells}")

        



        

if __name__ == "__main__":
    unittest.main()