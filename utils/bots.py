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
            return -0.1

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
                if self.check_win(board):
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


class XOBot:
    def __init__(
        self,
        learning_rate=0.2,
        discount_factor=0.9,
        exploration_rate=1.0,
        board_size=20,
    ):
        self.q_table = {}
        self.board_size = board_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = 0.9999
        self.min_exploration_rate = 0.1

    def get_state_hash(self, board):  # Hash state
        return tuple(board)

    def get_available_moves(self, board) -> list[int]:  # Get all available moves
        return [i for i in range(len(board)) if board[i] is None]

    def choose_action(self, board, player=1):
        valid_moves = self.get_available_moves(board)
        if random.random() < self.exploration_rate or tuple(board) not in self.q_table:
            return random.choice(valid_moves)
        return self.check_best(board, valid_moves, player=player)

    def check_best(
        self, board, valid_moves, variety=3, player=1
    ):  # Random choice the first highest 'variety' moves if value > 0 else choose the highest value
        best_moves = {}
        for move in valid_moves:
            next_board = board.copy()
            next_board[move] = player
            value = self.q_table.get(tuple(next_board), 0.0) * player
            if value not in best_moves:
                best_moves[value] = [move]
            else:
                best_moves[value].append(move)

        bests = []
        count = 0
        for value in sorted(best_moves, reverse=True):
            count += 1
            if value > 0 or len(bests) == 0:
                bests.extend(best_moves[value])
                if count >= variety:
                    break

        return random.choice(bests)

    def check_win(self, board):
        for i in range(self.board_size):  # Check rows
            row = board[i * self.board_size : (i + 1) * self.board_size]
            if self.find_consecutive_xo(row):
                return self.find_consecutive_xo(row)

        for i in range(self.board_size):  # Check columns
            col = [board[i + j * self.board_size] for j in range(self.board_size)]
            if self.find_consecutive_xo(col):
                return self.find_consecutive_xo(col)

        for start in range(-self.board_size + 1, self.board_size):  # Check diagonal
            diagonal = [
                board[i * self.board_size + i + start]
                for i in range(self.board_size)
                if 0 <= i + start < self.board_size
            ]
            if self.find_consecutive_xo(diagonal):
                return self.find_consecutive_xo(diagonal)

        for start in range(
            -self.board_size + 1, self.board_size
        ):  # Check anti-diagonal
            diagonal = [
                board[i * self.board_size + start - i]
                for i in range(self.board_size)
                if 0 <= start - i < self.board_size
            ]
            if self.find_consecutive_xo(diagonal):
                return self.find_consecutive_xo(diagonal)
        if all(cell is not None for cell in board):
            return -0.1

        return None

    def find_consecutive_xo(self, lst):
        count = 1
        prev = None
        for star in lst:
            if star == prev:
                count += 1
                if count >= 5:
                    return star
            else:
                count = 1
            prev = star
        return None

    def train(self, num_episodes=10000):
        for espisode in range(num_episodes):
            if espisode % 500 == 0:
                print(f"Episode {espisode}: ")
            board = [None] * self.board_size**2
            player = 1
            states = [self.get_state_hash(board)]
            while True:
                action = self.choose_action(board, player)
                board[action] = player
                states.append(self.get_state_hash(board))
                result = self.check_win(board)
                if result:
                    self.feed_reward(result, states)
                    break
                player = -player
            self.exploration_rate = max(
                self.min_exploration_rate,
                self.exploration_rate * self.exploration_decay,
            )

    def feed_reward(self, reward, states):
        for state in reversed(states):
            if state not in self.q_table:
                self.q_table[state] = 0
            self.q_table[state] += self.learning_rate * (
                self.discount_factor * reward - self.q_table[state]
            )
            reward = self.q_table[state]

    def play(self, board, player):
        action = self.choose_action(board, player)
        board[action] = player
        return board

    def save(self, path="bot_ttt.pkl"):
        with open(path, "wb") as file:
            pkl.dump(self, file)

    @staticmethod
    def load(path):
        with open(path, "rb") as file:
            instance = pkl.load(file)
        return instance
