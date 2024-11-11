from player import Player
import numpy as np
import random

from functools import reduce

class AIPlayer(Player):
    def __init__(self, learning_rate = 0.1, discount_factor = 0.9, epsilon = 0.9) -> None:
        super().__init__()
        self.lr = learning_rate
        self.df = discount_factor
        self.e = epsilon
        self.q_table = {}
        self.n_exploration = 0
        self.n_moves = 0

    def select_move(self, **kwargs):
        valid_moves = [val for val in kwargs["valid_moves"].values() if val]
        hashed_state = self.hash_state(kwargs["state"])
        self.n_moves += 1

        if np.random.rand() < self.e:
            self.n_exploration += 1
            return random.choice(valid_moves)
        else: 
            if hashed_state in self.q_table:
                q_values = self.q_table[hashed_state]
                max_q_action = max(q_values, key=q_values.get)
                return eval(max_q_action)
            else:
                self.n_exploration += 1
                return random.choice(valid_moves)

    def hash_state(self, state, base=16):
        return reduce(lambda acc, tile: acc * base + int(tile), state, 0)
        # return tuple(int(x) if x.is_integer() else float(x) for x in state)
    
    def update_q_value(self, hashed_state, action, reward, hashed_next_state):
        if hashed_state not in self.q_table:
            self.q_table[hashed_state] = {}
        if hashed_next_state not in self.q_table:
            self.q_table[hashed_next_state] = {}
        
        old_q = self.q_table[hashed_state].get(str(action), 0)
        max_next_q = max(self.q_table[hashed_next_state].values(), default = 0)
        new_q = old_q + self.lr * (reward + self.df * max_next_q - old_q)
        self.q_table[hashed_state][str(action)] = new_q
        return abs(new_q - old_q)

class RandomMovingAI(Player):
    def __init__(self) -> None:
        super().__init__()

    def select_move(self, **kwargs):
        valid_moves = [val for val in kwargs["valid_moves"].values() if val]
        return random.choice(valid_moves)

        