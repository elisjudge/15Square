from ai import AIPlayer
from trainer import Trainer
from utils import timeit

import config as c

class BaseAITrainer(Trainer):
    def __init__(self, player: AIPlayer, move_limit=c.MOVE_LIMIT, n_episodes=c.N_EPISODES, batch_size=c.BATCH_SIZE, seed=None) -> None:
        super().__init__(player, move_limit, n_episodes, batch_size, seed)

    def back_propagate_reward(self, final_state, history):
        """Standard backward propagation, updating Q-table immediately."""
        reward = 100 
        for i in range(len(history) - 1, -1, -1):
            current_state, action, current_correct_rows, current_correct_positions, current_priority_values = history[i]
            next_state = history[i + 1][0] if i + 1 < len(history) else final_state
            self.update_q_value(current_state, action, reward, next_state)
    
    def forward_propagate_reward(self, final_state, history):
        """Standard forward propagation, updating Q-table immediately."""
        for i in range(len(history)):
            current_state, action, current_correct_rows, current_correct_positions, current_priority_values = history[i]
            target_cells = current_priority_values

            next_state = history[i + 1][0] if i + 1 < len(history) else final_state
            next_correct_rows = history[i + 1][2] if i + 1 < len(history) else current_correct_rows
            next_correct_positions = history[i + 1][3] if i + 1 < len(history) else current_correct_positions

            positional_reward = len(next_correct_positions)
            row_completion_reward = sum(next_correct_rows) * 10

            target_reward = 0  # Placeholder for specific target tile reward logic
            
            empty_cell_reward = 0  # Placeholder for distance-based reward logic


            reward = positional_reward + row_completion_reward + target_reward + empty_cell_reward
            self.update_q_value(current_state, action, reward, next_state)


    
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
            