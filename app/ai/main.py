import sys
import argparse 
import numpy as np

from game import Game
from human import HumanPlayer
from ai import AIPlayer

MOVE_LIMIT = 5

class CmdLineParser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description='15 Puzzle')
        self.parser.add_argument(
            "--type",
            choices=['human', 'simple_ai'],
            help= "Select the player who will be playing ('human', 'simple_ai')")
        
    def get_args(self):
        return self.parser.parse_args()

    def do_args(self):
        self.args = self.get_args()
        if self.args.type == 'human':
            game = Game(player=HumanPlayer())
            while True:
                selection = game.player.select_move(state=game.board, valid_moves=game.valid_moves)
                game.simulate_click(selection)
                if game.winner:
                    print("You Win")
                    break
                game.n_moves += 1
            print(f"Final move count: {game.n_moves}")

        if self.args.type == "simple_ai":
            move_limit = MOVE_LIMIT
            player = AIPlayer()
            game = Game(player=player)
            game_history= []

            while not game.winner and game.n_moves < move_limit:
                current_state = game.board.cells
                current_move = game.player.select_move(state=current_state, valid_moves= game.valid_moves)
                game_history.append((np.copy(current_state), current_move))
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

            print(game_history)
            print(player.q_table)
        return self.args


def main():
    arg_parser = CmdLineParser()
    try: 
        args = arg_parser.do_args()
        if not args:
            raise Exception('You must enter a valid argument')
    except Exception as e:
        print(f"Error occured: {e}")
        sys.exit(1)
    sys.exit(0)    

if __name__ == "__main__":
    main()