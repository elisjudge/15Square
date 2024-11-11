from ai import AIPlayer
from functools import reduce
from game import Game

import config as c
import numpy as np

class Trainer:
    def __init__(self, player:AIPlayer, move_limit = c.MOVE_LIMIT, n_episodes = c.N_EPISODES, batch_size = c.BATCH_SIZE, seed= None) -> None:
        self.target = player
        self.move_limit = move_limit
        self.n_games = n_episodes
        self.batch_size = batch_size
        self.game_seed = seed

    def play_game(self):
        game = Game(player=self.target, seed=self.game_seed)
        history = []

        for _ in range(self.move_limit):
            current_state = game.board.cells
            current_move = game.player.select_move(state=current_state, valid_moves= game.valid_moves)
            current_correct_positions = self.evaluate_correct_positions(current_state)
            history.append((np.copy(current_state), current_move, current_correct_positions))
            game.simulate_click(current_move)
            game.n_moves += 1
            if game.winner:
                break
            
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

    def hash_state(self, state, base=c.HASH_BASE):
        return reduce(lambda acc, tile: acc * base + int(tile), state, 0)

    def train_ai(self):
        pass