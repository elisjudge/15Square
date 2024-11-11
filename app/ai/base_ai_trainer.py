from ai import AIPlayer
from trainer import Trainer
from utils import timeit

import config as c
import numpy as np

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
            priority_cells = current_priority_values
            priority_cell = self.find_first_out_of_place(priority_cells, current_state)

            next_state = history[i + 1][0] if i + 1 < len(history) else final_state
            next_correct_rows = history[i + 1][2] if i + 1 < len(history) else current_correct_rows
            next_correct_positions = history[i + 1][3] if i + 1 < len(history) else current_correct_positions

            # positional_reward = len(next_correct_positions)
            row_completion_reward = sum(next_correct_rows) * 10
            target_reward = self.calculate_target_cell_reward(current_state, next_state, priority_cell)
            empty_cell_reward = self.calculate_empty_cell_reward(current_state, next_state, priority_cell)

            # reward = positional_reward + row_completion_reward + target_reward + empty_cell_reward
            reward =  row_completion_reward + target_reward + empty_cell_reward
            
            self.update_q_value(current_state, action, reward, next_state)

    def calculate_target_cell_reward(self, current_state, next_state, priority_cell):
        target_position = self.index_to_coordinates(priority_cell - 1)
        priority_cell_position_current, priority_cell_position_next = self.get_priority_coordinate(current_state, next_state, priority_cell)
        current_distance = self.compute_manhattan_distance(target_position, priority_cell_position_current)
        next_distance = self.compute_manhattan_distance(target_position, priority_cell_position_next)

        if next_distance < current_distance:
            return 10
        elif next_distance == current_distance:
            return 0
        else:
            return -5
    
    def calculate_empty_cell_reward(self, current_state, next_state, priority_cell):
        empty_cell_position_current, empty_cell_position_next = self.get_empty_coordinate(current_state, next_state)
        priority_cell_position_current, priority_cell_position_next = self.get_priority_coordinate(current_state, next_state, priority_cell)
        current_distance = self.compute_manhattan_distance(empty_cell_position_current, priority_cell_position_current)
        next_distance = self.compute_manhattan_distance(empty_cell_position_next, priority_cell_position_next)
        
        if next_distance < current_distance:
            return 0.5
        else:
            return 0
        
    def get_empty_coordinate(self, current_state, next_state):
        empty_cell_position_current = self.index_to_coordinates(
            np.where(current_state == (c.N_ROWS * c.N_COLS))[0][0])
        empty_cell_position_next = self.index_to_coordinates(
            np.where(next_state == (c.N_ROWS * c.N_COLS))[0][0])
        return empty_cell_position_current, empty_cell_position_next

    def get_priority_coordinate(self, current_state, next_state, priority_cell):
        priority_cell_position_current = self.index_to_coordinates(
            np.where(current_state == priority_cell)[0][0])
        priority_cell_position_next = self.index_to_coordinates(
            np.where(next_state == priority_cell)[0][0])
        return priority_cell_position_current, priority_cell_position_next

    def index_to_coordinates(self, index):
        return (index // c.N_COLS, index % c.N_COLS)
    
    def compute_manhattan_distance(self, coord1, coord2):
        return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    def find_first_out_of_place(self, priority_cells, current_state):
        for cell in priority_cells:
            expected_position = cell - 1
            if current_state[expected_position] != cell:
                return cell
        return None
    
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
        
        self.save_q_table()
            