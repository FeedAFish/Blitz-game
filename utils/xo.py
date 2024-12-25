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
                x, y = self.mpos_to_ind(event.pos)
                if self.board[x + y * self.board_size] is None:
                    self.board[x + y * self.board_size] = self.player
                    self.player = -self.player
                    if self.check_win():
                        self.pause = True

    def mpos_to_ind(self, m_pos):
        x = m_pos[0] - self.x - self.grid_size // 2
        y = m_pos[1] - self.y - self.grid_size // 2
        return x // self.grid_size, y // self.grid_size

    def find_consecutive(self, lst, start_indices):  # Find consecutive stars
        count = 1
        for k in range(1, len(lst)):
            if lst[k] == lst[k - 1] and lst[k] != None:
                count += 1
                if count >= 5:
                    return lst[k]
            else:
                count = 1
        return

    def check_win(self):
        for i in range(self.board_size):  # Check row
            row = self.board[i * self.board_size : (i + 1) * self.board_size]
            row_indices = [(i, j) for j in range(self.board_size)]
            if self.find_consecutive(row, row_indices):
                return self.find_consecutive(row, row_indices)

        for j in range(self.board_size):  # Check column
            col = [self.board[i * self.board_size + j] for i in range(self.board_size)]
            col_indices = [(i, j) for i in range(self.board_size)]
            if self.find_consecutive(col, col_indices):
                return self.find_consecutive(col, col_indices)

        for start in range(-self.board_size + 1, self.board_size):  # Check diagonal
            diag = []
            diag_indices = []
            for i in range(self.board_size):
                j = i + start
                if 0 <= i < self.board_size and 0 <= j < self.board_size:
                    diag.append(self.board[i * self.board_size + j])
                    diag_indices.append((i, j))
            if self.find_consecutive(diag, diag_indices):
                return self.find_consecutive(diag, diag_indices)
        return
