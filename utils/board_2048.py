from utils import elements

import random
import pygame


class Board_2048(elements.Board):
    def __init__(self, x, y, image_path=None):
        super().__init__(x, y, image_path)
        self.board_size = 4
        self.grid_size = 100
        self.width = self.grid_size * self.board_size
        self.x = 100
        self.y = 100
        self.load_color()
        self.load_image_and_font("data/img/2048_bg.png", "data/img/box_2048.png")
        self.init_board()

    # Initialize the board
    def init_board(self):  # Initialize the board
        self.pause = True
        self.end = False
        self.score = 0
        self.board = [0 for _ in range((self.board_size) ** 2)]
        for _ in range(2):
            self.add_new_element()
        self.score = 0
        self.pause = False

    def load_image_and_font(self, bg_path, box_path):  # Load image for the board
        try:
            self.bg = pygame.transform.scale(
                pygame.image.load(bg_path).convert_alpha(),
                (self.width, self.width),
            )
            self.box = pygame.transform.scale(
                pygame.image.load(box_path).convert_alpha(),
                (self.grid_size, self.grid_size),
            )
        except pygame.error:
            print("Cannot load image:", bg_path, box_path)
            self.bg = pygame.Surface((self.width, self.width))

        try:
            self.font = pygame.font.Font("data/font/LovelyKids-gxly4.ttf", 25)
        except:
            self.font = pygame.font.Font(None, 25)

    def load_color(self):
        self.color = [
            (255, 255, 255),  # White
            (128, 128, 128),  # Gray
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 165, 0),  # Orange
            (255, 255, 0),  # Yellow
            (128, 0, 128),  # Purple
            (255, 192, 203),  # Pink
            (165, 42, 42),  # Brown
            (0, 0, 0),  # Black
            (255, 0, 0),  # Red
            (0, 255, 255),  # Cyan
            (255, 0, 255),  # Magenta
            (0, 128, 128),  # Teal
            (237, 197, 63),  # Gold
        ]

    # Draw the board
    def draw(self, surface):  # Draw the board
        super().draw(surface)
        self.draw_grid(surface)
        self.draw_elements(surface)
        self.draw_result(surface)

    def draw_grid(self, surface):  # Draw grid for the board
        pygame.draw.rect(surface, (0, 0, 0), self.rect.inflate(-7, -7), border_radius=3)
        surface.blit(self.bg, (self.x, self.y))
        board = pygame.Surface((self.width, self.width), pygame.SRCALPHA)
        pygame.draw.rect(
            board,
            (119, 110, 101, 200),
            board.get_rect(),
        )
        surface.blit(board, (self.x, self.y))
        for i in range(self.board_size - 1):
            pygame.draw.line(
                surface,
                (0, 0, 0),
                (self.x, self.y + (i + 1) * self.grid_size),
                (
                    self.x + self.width,
                    self.y + (i + 1) * self.grid_size,
                ),
                1,
            )
            pygame.draw.line(
                surface,
                (0, 0, 0),
                (self.x + (i + 1) * self.grid_size, self.y),
                (
                    self.x + (i + 1) * self.grid_size,
                    self.y + self.width,
                ),
            )

    def draw_elements(self, surface):  # Draw elements on board
        for num, i in enumerate(self.board):
            if i:
                self.draw_one_element(surface, num, i)

    def draw_one_element(self, surface, pos, value):  # Draw one element on board
        x = pos % self.board_size
        y = pos // self.board_size
        pygame.draw.circle(
            surface,
            self.color[value - 1],
            (
                self.x + x * self.grid_size + self.grid_size // 2,
                self.y + y * self.grid_size + self.grid_size // 2,
            ),
            self.grid_size // 2,
        )
        surface.blit(
            self.box,
            (self.x + x * self.grid_size, self.y + y * self.grid_size),
        )
        text = self.font.render(str(2**value), True, (0, 0, 0))
        text = pygame.transform.rotate(text, -10)
        text_rect = text.get_rect(
            center=(
                self.x + x * self.grid_size + self.grid_size // 3,
                self.y + y * self.grid_size + 2 * self.grid_size // 3,
            )
        )
        surface.blit(
            text,
            text_rect,
        )

    def draw_result(self, surface):  # Draw the result
        text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = (700, 100)
        surface.blit(text, rect)
        if self.end:
            text = self.font.render("Game Over", True, (0, 0, 0))
            rect = text.get_rect()
            rect.center = (700, 140)
            surface.blit(text, rect)

    # Game Mechanics
    def on_key_down(self, event):  # Key down event
        if self.pause or self.end:
            return

        if event.key == pygame.K_UP:
            self.board = self.move(0)
        elif event.key == pygame.K_DOWN:
            self.board = self.move(1)
        elif event.key == pygame.K_LEFT:
            self.board = self.move(2)
        elif event.key == pygame.K_RIGHT:
            self.board = self.move(3)

    def add_new_element(self):
        available = [i for i in range(self.board_size**2) if not self.board[i]]
        if not available:
            self.end = True
        rand = random.choice([1, 1, 1, 2])

        self.board[random.choice(available)] = rand
        self.score += 2**rand

    def move(self, direction):
        if self.pause or self.end:
            return
        if direction == 0:
            return self.move_up()
        elif direction == 1:
            return self.move_down()
        elif direction == 2:
            return self.move_left()
        elif direction == 3:
            return self.move_right()

    def list_move(self, lst):  # Move value by list
        col = [i for i in lst]
        for j in range(self.board_size):
            if not col[j]:
                for k in range(j + 1, self.board_size):
                    if col[k]:
                        col[j], col[k] = col[k], col[j]
                        break
            if col[j]:
                for k in range(j + 1, self.board_size):
                    if col[k]:
                        if col[k] == col[j]:
                            col[j] += 1
                            col[k] = 0
                            self.score += 2 ** (col[j])
                        break
        return col

    def move_up(self):  # Move up
        board = self.board.copy()
        for i in range(self.board_size):

            lst = [self.board[j] for j in range(i, self.board_size**2, self.board_size)]
            lst = self.list_move(lst)

            for j in range(i, self.board_size**2, self.board_size):
                board[j] = lst[j // self.board_size]
        return board

    def move_down(self):  # Move down
        board = self.board.copy()
        for i in range(self.board_size):
            lst = [self.board[j] for j in range(i, self.board_size**2, self.board_size)]
            lst = lst[::-1]
            lst = self.list_move(lst)
            for j in range(i, self.board_size**2, self.board_size):
                board[j] = lst[3 - j // self.board_size]
        return board

    def move_left(self):  # Move left
        board = self.board.copy()
        for i in range(self.board_size):
            lst = [
                self.board[j]
                for j in range(i * self.board_size, (i + 1) * self.board_size)
            ]
            lst = self.list_move(lst)

            for j in range(i * self.board_size, (i + 1) * self.board_size):
                board[j] = lst[j % self.board_size]
        return board

    def move_right(self):  # Move right
        board = self.board.copy()
        for i in range(self.board_size):
            lst = [
                self.board[j]
                for j in range(
                    (i + 1) * self.board_size - 1, i * self.board_size - 1, -1
                )
            ]
            lst = self.list_move(lst)

            for j in range((i + 1) * self.board_size - 1, i * self.board_size - 1, -1):
                board[j] = lst[3 - j % self.board_size]
        return board

    def check_end(self):  # Check win
        for i in range(4):
            if self.move(i) != self.board:
                return False
        pygame.mixer.Sound("data/sound/loss.mp3").play()
        return True

    # Event handle
    def on_click(self, event):
        if event.type == pygame.KEYDOWN:
            self.o_board = self.board.copy()
            self.on_key_down(event)
            if self.board != self.o_board:
                self.add_new_element()
                if self.check_end():
                    self.end = True

    def to_pause(self):
        self.pause = not self.pause
