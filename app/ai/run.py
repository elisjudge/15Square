import sys
import argparse 

import cProfile
import pstats  # Optional, for organizing profiling output
from io import StringIO

from ai._game import Game
from ai._human import HumanPlayer
from ai._ai import AIPlayer
from ai._base_ai_trainer import BaseAITrainer

import logging
from logger import setup_logging

setup_logging()
logger = logging.getLogger("app")

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
            game = Game(player=HumanPlayer(), seed=10)
            while True:
                selection = game.player.select_move(state=game.board, valid_moves=game.valid_moves)
                game.simulate_click(selection)
                if game.winner:
                    print("You Win")
                    break
                game.n_moves += 1
            print(f"Final move count: {game.n_moves}")

        if self.args.type == "simple_ai":
            player = AIPlayer()
            trainer = BaseAITrainer(player=player, seed=4)

            profile = cProfile.Profile()
            profile.enable()
            trainer.train_ai()
            profile.disable()
            
            # Print profile stats
            stream = StringIO()
            ps = pstats.Stats(profile, stream=stream).sort_stats('cumulative')
            ps.print_stats(20)  # Show top 20 entries
            print(stream.getvalue())
            
        return self.args


def main():
    logger.debug("This is a debug message.")
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