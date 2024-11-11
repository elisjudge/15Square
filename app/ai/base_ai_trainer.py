from ai import AIPlayer
from trainer import Trainer
from utils import timeit

import config as c

class BaseAITrainer(Trainer):
    def __init__(self, player: AIPlayer, move_limit=c.MOVE_LIMIT, n_episodes=c.N_EPISODES, batch_size=c.BATCH_SIZE, seed=None) -> None:
        super().__init__(player, move_limit, n_episodes, batch_size, seed)
    
    @timeit
    def train_ai(self):
        first_win_game = None
        
        for i in range(self.n_games):
            winner, final_state, history = self.play_game()
            if winner:
                self.back_propagate_reward(winner, final_state, history)

                if first_win_game is None:
                    first_win_game = i  
                    break
            else:
                self.forward_propagate_reward(final_state, history)

        if first_win_game is not None:
            print(f"Games played prior to first win: {first_win_game}")
            