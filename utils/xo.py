from utils import elements
from utils import bots

import pygame


class GameXO(elements.Board):
    def __init__(self, x, y, image_path=None):
        super().__init__(x, y, image_path)
        self.mode = 1
        self.player = 1
        self.silent = False

        self.sizing_board()
        self.hover_rect = self.rect.inflate(-self.grid_size - 1, -self.grid_size - 1)

        # Load resources
        self.load_bot()
        self.load_image()
        self.load_sound()
        self.init_board()

    def load_bot(self):  # Load bot
        pass

    def switch_mode(self):  # Switch PVE and PVP mode
        self.mode = 1 if self.mode == 0 else 0

    def switch_player(self):  # Switch player turn
        self.player = -self.player

    def sizing_board(self):  # Sizing board
        self.grid_size = 20
        self.board_size = 400 // self.grid_size + 1
        self.width = self.height = self.grid_size * (self.board_size - 1)
        self.hover_rect = self.rect.inflate(
            (420 - self.width) // 2, (420 - self.height) // 2
        )

    def load_sound(self):  # Load sound
        self.move_sound = pygame.mixer.Sound("data/sound/error.mp3")
        self.set_sound(0.5)

    def set_sound(self, sound):  # Set sound volume
        self.move_sound.set_volume(sound)

    def change_sound(self):
        self.silent = not self.silent
        self.set_sound(0 if self.silent else 0.5)

    def load_image(self):  # Load image
        def load_n_scale(image_path, size):
            return pygame.transform.scale(
                pygame.image.load(image_path).convert_alpha(), size
            )

        self.image_list = [
            load_n_scale(
                "./data/img/XO_X.png", (self.grid_size - 6, self.grid_size - 6)
            ),
            load_n_scale(
                "./data/img/XO_O.png", (self.grid_size - 6, self.grid_size - 6)
            ),
        ]

    def init_board(self):
        self.board = [None for _ in range(self.board_size**2)]
        self.pause = False
        self.turn = 1

    def draw(self, surface):  # Draw board
        super().draw(surface)
        self.draw_grid(surface)  # Draw grid
        self.draw_elements(surface)  # Draw elements
        self.draw_result(surface)  # Draw result

    def draw_grid(self, surface):
        for i in range(self.board_size):
            pygame.draw.line(
                surface,
                (128, 128, 128),
                (self.x + self.grid_size // 2, self.y + i * self.grid_size),
                (
                    self.x + self.grid_size // 2 + self.width,
                    self.y + i * self.grid_size,
                ),
                1,
            )
            pygame.draw.line(
                surface,
                (128, 128, 128),
                (self.x + i * self.grid_size, self.y + self.grid_size // 2),
                (
                    self.x + i * self.grid_size,
                    self.y + self.grid_size // 2 + self.width,
                ),
                1,
            )

    def draw_elements(self, surface):
        for i, element in enumerate(self.board):
            if element:
                x, y = i % self.board_size, i // self.board_size
                surface.blit(
                    self.image_list[(element + 1) // 2],
                    (
                        self.x + self.grid_size + x * self.grid_size - 7,
                        self.y + self.grid_size + y * self.grid_size - 7,
                    ),
                )

    def draw_result(self, surface):
        pass

    def on_click(self, event):
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and not self.pause
        ):
            if self.hover_rect.collidepoint(event.pos):
                x, y = self.mouse_position_to_indices(event.pos)
                if self.board[x + y * self.board_size] is None:
                    self.board[x + y * self.board_size] = self.turn
                    self.turn = -self.turn
                    if self.check_win():
                        self.pause = True

    def mouse_position_to_indices(
        self, mouse_position
    ):  # Convert mouse position to grid indices.
        x, y = mouse_position
        x -= self.x + self.grid_size // 2
        y -= self.y + self.grid_size // 2

        return x // self.grid_size, y // self.grid_size

    def find_consecutive_xo(self, lst):
        count = 1
        for index, star in enumerate(lst[1:], start=1):
            if star == lst[index - 1] and star is not None:
                count += 1
                if count >= 5:
                    return star
            else:
                count = 1
        return None

    def check_win(self):
        for i in range(self.board_size):  # Check rows
            row = self.board[i * self.board_size : (i + 1) * self.board_size]
            if self.find_consecutive_xo(row):
                return self.find_consecutive_xo(row)

        for i in range(self.board_size):  # Check columns
            col = [self.board[i + j * self.board_size] for j in range(self.board_size)]
            if self.find_consecutive_xo(col):
                return self.find_consecutive_xo(col)

        for start in range(-self.board_size + 1, self.board_size):  # Check diagonal
            diagonal = [
                self.board[i * self.board_size + i + start]
                for i in range(self.board_size)
                if 0 <= i + start < self.board_size
            ]
            if self.find_consecutive_xo(diagonal):
                return self.find_consecutive_xo(diagonal)

        for start in range(
            -self.board_size + 1, self.board_size
        ):  # Check anti-diagonal
            diagonal = [
                self.board[i * self.board_size + start - i]
                for i in range(self.board_size)
                if 0 <= start - i < self.board_size
            ]
            if self.find_consecutive_xo(diagonal):
                return self.find_consecutive_xo(diagonal)

        return None
