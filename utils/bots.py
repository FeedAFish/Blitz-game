import random
import pickle as pkl


class TicTacToeBot:
    def __init__(
        self, player=1, learning_rate=0.2, discount_factor=0.9, exploration_rate=1.0
    ):
        # Initialize Q-table with zeros for all possible states and actions
        self.q_table = {}
        self.player = player

        # Learning parameters
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = 0.9999
        self.min_exploration_rate = 0.001

    def get_state_hash(self, board):
        return tuple(board)

    def get_moves(self, board):
        return [i for i in range(9) if not board[i]]

    def choose_action(
        self,
        board,
    ):
        valid_moves = self.get_moves(board)
        # Exploration
        if random.random() < self.exploration_rate:
            return random.choice(valid_moves)

        # Exploitation
        state_key = self.get_state_hash(board)
        if state_key not in self.q_table:
            return random.choice(valid_moves)

        if state_key == tuple([None] * 9):
            return random.choice(valid_moves)

        return self.check_best(board, valid_moves)

    def check_best(self, board, valid_moves):
        next_board = board.copy()
        max_value = -100

        for move in valid_moves:
            next_board[move] = self.player

            if tuple(next_board) not in self.q_table:
                value = 0
            else:
                value = self.q_table.get(tuple(next_board)) * self.player

            if value > max_value:
                max_value = value
                bests = [move]
            elif value == max_value:
                bests.append(move)

            next_board[move] = None

        return random.choice(bests)

    def check_win(self, board):
        winning_combinations = [
            (0, 1, 2),  # Row 1
            (3, 4, 5),  # Row 2
            (6, 7, 8),  # Row 3
            (0, 3, 6),  # Col 1
            (1, 4, 7),  # Col 2
            (2, 5, 8),  # Col 3
            (0, 4, 8),  # Dia 1
            (2, 4, 6),  # Dia 2
        ]

        for combo in winning_combinations:
            a, b, c = combo
            if board[a] == board[b] == board[c] and board[a] is not None:
                return board[a]

        if all(cell is not None for cell in board):
            return 0

        return None

    def feed_reward(self, reward):
        for state in reversed(self.states_record):
            if self.q_table.get(state) is None:
                self.q_table[state] = 0
            self.q_table[state] += self.learning_rate * (
                self.discount_factor * reward - self.q_table[state]
            )
            reward = self.q_table[state]

    def train(self, num_episodes=10000):
        for episode in range(num_episodes):
            board = [None] * 9
            self.player = 1
            self.states_record = [self.get_state_hash(board)]
            while True:
                action = self.choose_action(board)
                board[action] = self.player
                self.states_record.append(self.get_state_hash(board))
                if self.check_win(board) != None:
                    self.feed_reward(self.check_win(board))
                    break
                self.player = -self.player
            self.exploration_rate = max(
                self.min_exploration_rate,
                self.exploration_rate * self.exploration_decay,
            )

    def play(self, board, player):
        self.player = player
        action = self.choose_action(board)
        board[action] = self.player
        return board

    def save(self, path="bot_ttt.pkl"):
        with open(path, "wb") as file:
            pkl.dump(self, file)

    @staticmethod
    def load(path):
        with open(path, "rb") as file:
            instance = pkl.load(file)
        return instance
