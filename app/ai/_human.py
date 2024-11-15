from ._player import Player

class HumanPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def select_move(self, **kwargs):
        print(kwargs["state"])
        print()
        print(kwargs["valid_moves"])
        print()
        selection = int(input("Enter index you wish to move: "))
        return selection