from game import Game
from ai import AIPlayer
from utils import timeit

import numpy as np

N_EPISODES = 10000
EPOCH_LENGTH = 1000
MOVE_LIMIT = 1000

class SimpleAITrainer:
    def __init__(self, player:AIPlayer, move_limit = MOVE_LIMIT, n_episodes = N_EPISODES, epoch_length = EPOCH_LENGTH) -> None:
        self.target = player
        self.move_limit = move_limit
        self.n_games = n_episodes
        self.epoch_length = epoch_length

    def play_game(self):
        game = Game(player=self.target)
        history = []
        while not game.winner and game.n_moves < self.move_limit:
            current_state = game.board.cells
            current_move = game.player.select_move(state=current_state, valid_moves= game.valid_moves)
            current_correct_positions = self.evaluate_correct_positions(current_state)
            history.append((np.copy(current_state), current_move, current_correct_positions))
            game.simulate_click(current_move)
            if game.winner:
                break
            game.n_moves += 1
        return game.winner, game.board.cells, history
    
    def evaluate_correct_positions(self, state):
        return {i for i, value in enumerate(state) if value == i + 1}
    
    def back_propagate_reward(self, winner, final_state, history):
        reward = 10 if winner else -10
        for i in range(len(history) - 1, -1, -1):
            current_state, action, current_correct_positions = history[i]
            next_state = history[i + 1][0] if i + 1 < len(history) else final_state
            self.target.update_q_value(
                hashed_state=self.target.hash_state(current_state),
                action=str(action),
                reward=reward,
                hashed_next_state=self.target.hash_state(next_state)
            )
    
    def forward_propagate_reward(self, winner, final_state, history):
        end_reward = 10 if winner else -10
        
        for i in range(len(history)):
            current_state, action, current_correct_positions = history[i]
            next_state = history[i + 1][0] if i + 1 < len(history) else final_state
            final_state_correct_positions = self.evaluate_correct_positions(final_state)
            next_correct_positions = history[i + 1][2] if i + 1 < len(history) else final_state_correct_positions

            intermediate_reward = len(next_correct_positions)

            if i != len(history) - 1:
                reward = intermediate_reward
            else:
                reward = end_reward + intermediate_reward

            self.target.update_q_value(
                hashed_state=self.target.hash_state(current_state),
                action=str(action),
                reward=reward,
                hashed_next_state=self.target.hash_state(next_state)
            )

    @timeit
    def train_ai(self, propagation_type):
        wins = 0
        losses = 0
        first_win_game = None
        first_win_recorded = False
        
        for i in range(self.n_games):
            winner, final_state, history = self.play_game()
            if winner:
                wins += 1
                if not first_win_recorded:
                    first_win_game = i  
                    first_win_recorded = True
            else:
                losses += 1 
            
            if propagation_type == "backward":
                self.back_propagate_reward(winner, final_state, history)
            elif propagation_type == "forward":
                self.forward_propagate_reward(winner, final_state, history)

        print(f"Wins: {wins}, Losses: {losses}")
        if first_win_recorded:
            print(f"Games played prior to first win: {first_win_game}")

            
            






            


        

