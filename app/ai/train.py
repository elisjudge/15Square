from game import Game
from ai import AIPlayer

import numpy as np

class SimpleAITrainer:
    def __init__(self, move_limit, player:AIPlayer) -> None:
        self.move_limit = move_limit
        self.target = player

    def play_game(self):
        game = Game(player=self.target)
        history = []
        while not game.winner and game.n_moves < self.move_limit:
            current_state = game.board.cells
            current_move = game.player.select_move(state=current_state, valid_moves= game.valid_moves)
            history.append((np.copy(current_state), current_move))
            print(game.board)
            print()
            print(game.valid_moves)
            print()
            game.simulate_click(current_move)
            if game.winner:
                print("You Win")
                break
            game.n_moves += 1
        print(f"Final move count: {game.n_moves}")
        print(self.target.q_table)

