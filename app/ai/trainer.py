from ai import AIPlayer
from game import Game

import config as c
import json
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
            current_correct_rows = game.board.row_complete
            history.append((np.copy(current_state), current_move, current_correct_rows, current_correct_positions))
            game.simulate_click(current_move)
            game.n_moves += 1
            if game.winner:
                break
            
        return game.winner, game.board.cells, history
    
    def evaluate_correct_positions(self, state):
        return {i for i, value in enumerate(state) if value == i + 1}
    
    def back_propagate_reward(self, final_state, history):
        """Standard backward propagation, updating Q-table immediately."""
        pass

    
    def forward_propagate_reward(self, final_state, history):
        """Standard forward propagation, updating Q-table immediately."""
        pass

    def hash_state(self, state):
        return tuple(map(int, state))
    
    def save_q_table(self, filename="ai_q.json"):
        """Save the Q-table to a file with tuple keys converted to strings for JSON compatibility."""
        q_table_serializable = {str(key): value for key, value in self.target.q_table.items()}
        with open(filename, "w") as f:
            json.dump(q_table_serializable, f, indent=4)

    def load_q_table(self, filename="ai_q.json"):
        """Load the Q-table from a file, converting string keys back to tuples."""
        with open(filename, "r") as f:
            q_table_data = json.load(f)
        self.target.q_table = {eval(key): value for key, value in q_table_data.items()}
    
    def train_ai(self):
        pass

    def update_q_value(self, current_state, action, reward, next_state):
        self.target.update_q_value(
                hashed_state=self.target.hash_state(current_state),
                action=str(action),
                reward=reward,
                hashed_next_state=self.target.hash_state(next_state)
            )
