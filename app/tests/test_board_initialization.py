import unittest
import ai

class TestBoardInitialization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n Running Board Initialization Tests... \n")
    
    def setUp(self):
        pass

    def test_1(self):
        board = ai.Board()
        

if __name__ == "__main__":
    unittest.main()