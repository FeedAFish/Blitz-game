import numpy as np
import random
import pickle as pkl
import torch
import torch.nn as nn
import torch.optim as optim


class XO_Bot:
    def __init__(
        self,
        board_size,
        learning_rate=0.2,
        discount_factor=0.9,
        exploration_rate=1.0,
    ):
        self.board_size = board_size
        self.state_size = self.board_size * self.board_size
        self.action_size = self.state_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.memory = []
        # Learning parameters
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = 0.99
        self.min_exploration_rate = 0.1

        self.model = self.build_model().to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def build_model(self):
        model = nn.Sequential(
            nn.Linear(self.state_size, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, self.action_size),
        )
        return model

    def predict(self, board):
        state = torch.FloatTensor(board).to(self.device)
        with torch.no_grad():
            return self.model(state).cpu().numpy()

    def fit(self, board, q_values):
        self.optimizer.zero_grad()
        outputs = self.predict(board)
        self.criterion(outputs, q_values).backward()
        self.optimizer.step()

    def remember(self, board, action, reward, next_board, done):
        self.memory.append((board, action, reward, next_board, done))
        if len(self.memory) > 2000:
            self.memory.pop(0)

    def choose_action(self, board):

        if np.random.rand() <= self.exploration_rate:
            return random.randrange(self.action_size)
        q_values = self.predict(board)
        best5 = np.argpartition(q_values, -5)[-5:]
        choice = [best5[-1]]
        choice.extend([i for i in best5[:-1] if q_values[i] > 0])
        return random.choice(choice)

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for board, action, reward, n_board, done in minibatch:
            target = reward
            if not done:
                target -= self.discount_factor * np.amax(self.predict(n_board))
            q_values = self.predict(board)
            q_values[0][action] = target
            self.fit(board, q_values, epochs=1, verbose=0)

    def update_exp_rate(self):
        if self.exploration_rate > self.min_exploration_rate:
            self.exploration_rate *= self.exploration_decay

    def train(self, num_episodes=1000):
        for episode in range(num_episodes):
            self.current_player = 1
            total_reward = 0
            board = [0] * self.state_size

            for _ in range(100):  # Limit each episode to 100 steps
                action = self.choose_action(board)
                n_board, reward, done = self.step(action, board)
                self.remember(board, action, reward, n_board, done)
                board = n_board
                total_reward += reward

                if done:
                    break

            self.replay(64)
            self.update_exp_rate()
            if episode % 10 == 0:
                print(f"Episode {episode}: Total reward: {total_reward}")

    def step(self, action, board):
        if board[action] != 0:  # Invalid move
            return board, -1000, True

        # Apply move
        board[action] = self.current_player
        reward, done = self.check_win(board)
        self.current_player = 3 - self.current_player  # Switch player
        return board, reward, done

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

    def check_win(self, board):
        for i in range(self.board_size):  # Check rows
            row = board[i * self.board_size : (i + 1) * self.board_size]
            if self.find_consecutive_xo(row):
                return 100, True

        for i in range(self.board_size):  # Check columns
            col = [board[i + j * self.board_size] for j in range(self.board_size)]
            if self.find_consecutive_xo(col):
                return 100, True

        for start in range(-self.board_size + 1, self.board_size):  # Check diagonal
            diagonal = [
                board[i * self.board_size + i + start]
                for i in range(self.board_size)
                if 0 <= i + start < self.board_size
            ]
            if self.find_consecutive_xo(diagonal):
                return 100, True

        for start in range(
            -self.board_size + 1, self.board_size
        ):  # Check anti-diagonal
            diagonal = [
                board[i * self.board_size + start - i]
                for i in range(self.board_size)
                if 0 <= start - i < self.board_size
            ]
            if self.find_consecutive_xo(diagonal):
                return 100, True
        if all(cell is not None for cell in board):
            return 0, True

        return 1, False

    def play(self, board, player):
        action = self.choose_action(board)
        board[action] = player
        return board

    def save(self, path="bot_xo.mdl"):
        with open(f"{path}", "wb") as file:
            torch.save(self, file)
        print(f"Bot saved successfully to {path}.")

    @staticmethod
    def load(path):
        # Load the attributes
        with open(f"{path}", "rb") as file:
            instance = torch.load(file, weights_only=False)

        print(f"Bot loaded successfully from {path}.")
        return instance
