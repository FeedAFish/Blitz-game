import numpy as np
import random
import pickle as pkl
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import Dense  # type: ignore
from tensorflow.keras.optimizers import Adam  # type: ignore


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

        self.memory = []
        # Learning parameters
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = 0.99
        self.min_exploration_rate = 0.1

        self.model = self.build_model()

    def build_model(self):
        model = Sequential(
            [
                Dense(128, input_dim=self.state_size, activation="relu"),
                Dense(128, activation="relu"),
                Dense(self.action_size, activation="linear"),
            ]
        )
        model.compile(optimizer=Adam(learning_rate=self.learning_rate), loss="mse")
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > 2000:
            self.memory.pop(0)

    def choose_action(self, state):
        if np.random.rand() <= self.exploration_rate:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state, verbose=0)
        best5 = np.argpartition(q_values[0], -5)[-5:]
        choice = [best5[-1]]
        choice.extend([i for i in best5[:-1] if q_values[0][i] > 6])
        return random.choice(choice)

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target -= self.discount_factor * np.amax(
                    self.model.predict(next_state, verbose=0)[0]
                )
            q_values = self.model.predict(state, verbose=0)
            q_values[0][action] = target
            self.model.fit(state, q_values, epochs=1, verbose=0)

    def update_epsilon(self):
        if self.exploration_rate > self.min_exploration_rate:
            self.exploration_rate *= self.exploration_decay

    def train(self, num_episodes=1000):
        for episode in range(num_episodes):
            self.current_player = 1
            total_reward = 0
            state = np.zeros((1, self.state_size))

            for _ in range(100):  # Limit each episode to 100 steps
                action = self.choose_action(state)
                n_state, reward, done = self.step(action, state)
                self.remember(state, action, reward, n_state, done)
                state = n_state
                total_reward += reward

                if done:
                    break

            self.replay(64)
            self.update_epsilon()
            if episode % 100 == 0:
                print(f"Episode {episode}: Total reward: {total_reward}")

    def step(self, action, state):
        if state[0][action] != 0:  # Invalid move
            return state, -1000, True

        # Apply move
        state[0][action] = self.current_player
        reward, done = self.check_win(state[0])
        self.current_player = 3 - self.current_player  # Switch player
        return state, reward, done

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
        state = np.array(board).reshape(1, self.state_size)
        action = self.choose_action(state)
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
