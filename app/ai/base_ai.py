import random
from player import Player

class BaseAI(Player):
    def __init__(self) -> None:
        super().__init__()

    def select_move(self, **kwargs):
        valid_moves = [val for val in kwargs["valid_moves"].values() if val]
        return random.choice(valid_moves)
