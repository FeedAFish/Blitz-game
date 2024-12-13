import pygame
import sys
from utils import bots


class Element:
    def __init__(self):
        pass

    def is_hover(self, mouse_pos):
        pass

    def on_click(self, event):
        pass

    def draw(self, surface):
        pass


class Button(Element):
    def __init__(
        self,
        x,
        y,
        image_path=None,
        text="",
        font_path="./font/LovelyKids-gxly4.ttf",
        action=None,
    ):
        # Load the image and font
        try:
            self.original_image = pygame.image.load(image_path).convert_alpha()
        except:
            pygame.quit()
            sys.exit()
        self.font = pygame.font.Font(font_path if font_path else None, 35)
        self.action = action if action else lambda: None

        # Resize image if it's too large (optional)
        max_width = 160
        if self.original_image.get_width() > max_width:
            aspect_ratio = (
                self.original_image.get_height() / self.original_image.get_width()
            )
            new_height = int(max_width * aspect_ratio)
            self.original_image = pygame.transform.scale(
                self.original_image, (max_width, new_height)
            )

        # Create a rect and hover_rect
        self.rect = self.original_image.get_rect(center=(x, y))
        self.hover_rect = self.rect.inflate(-5, -5)

        # Render text
        self.text_surface = self.font.render(text, True, (0, 0, 0))

        # Rotation variables
        self.angle = 0
        self.hover = False

    def draw(self, surface):
        # Blit the base image
        if self.hover:
            # Update angle with oscillation
            self.angle = 10

            # Rotate the image
            rotated_image = pygame.transform.rotate(self.original_image, self.angle)
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            surface.blit(rotated_image, rotated_rect)

        else:
            # Reset angle when not hovering
            self.angle = 0
            # Draw the original image and text when not hovering
            surface.blit(self.original_image, self.rect)

        # Center the text on the button
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        surface.blit(self.text_surface, text_rect)

    # Check if is hovered
    def is_hover(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
        return self.hover

    # Action on click
    def on_click(self, event):
        if self.hover_rect.collidepoint(event.pos):
            self.action()


class Board(Element):
    def __init__(self, x, y, image_path=None):
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(90, 90, 420, 420)
        self.image = (
            pygame.image.load(image_path).convert_alpha() if image_path else None
        )

    def draw(self, surface):
        # Draw outliner
        pygame.draw.rect(
            surface, (110, 44, 0), self.rect.inflate(6, 6), border_radius=3
        )

        # Draw inside
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, (255, 255, 255), self.rect, border_radius=3)


class Board_TTT(Board):
    def __init__(self, x, y, image_path=None):
        super().__init__(x, y, image_path)
        self.mode = 1
        self.player = -1
        self.hover_rect = self.rect.inflate(-5, -5)
        self.bot_rl = bots.TicTacToeBot.load("test_1.pkl")
        self.init_board()
        self.load_image()

    # Reinitiate the board
    def init_board(self):
        self.pause = True
        self.board = [None] * 9
        self.turn = 1
        if self.mode and self.player == -1:
            self.bot_play()
        self.pause = False

    # Load image for Tic Tac Toe
    def load_image(self):
        self.list_image = [
            pygame.image.load("img/banana.png").convert_alpha(),
            pygame.image.load("img/grape.png").convert_alpha(),
        ]
        self.list_result = [
            pygame.image.load("img/banana_w.png").convert_alpha(),
            pygame.image.load("img/draw.png").convert_alpha(),
            pygame.image.load("img/grape_w.png").convert_alpha(),
        ]

    def draw(self, surface):
        super().draw(surface)
        self.draw_grid(surface)
        self.draw_tic_tac_toe(surface)
        self.draw_result(surface)

    def draw_grid(self, surface):
        pygame.draw.line(
            surface, (0, 0, 0), (self.x + 140, self.y), (self.x + 140, self.y + 420), 5
        )
        pygame.draw.line(
            surface, (0, 0, 0), (self.x + 280, self.y), (self.x + 280, self.y + 420), 5
        )
        pygame.draw.line(
            surface, (0, 0, 0), (self.x, self.y + 280), (self.x + 420, self.y + 280), 5
        )
        pygame.draw.line(
            surface, (0, 0, 0), (self.x, self.y + 140), (self.x + 420, self.y + 140), 5
        )

    def draw_tic_tac_toe(self, surface):
        for i in range(9):
            if self.board[i]:
                surface.blit(
                    self.list_image[(self.board[i] + 1) // 2],
                    (self.x + 140 * (i % 3), self.y + 140 * (i // 3)),
                )

    def draw_result(self, surface):
        if self.check_win() != None:
            surface.blit(
                self.list_result[self.check_win() + 1],
                (620, 50),
            )

    def on_click(self, event):
        if (not self.pause) and self.hover_rect.collidepoint(event.pos):
            ind = self.mpos_to_ind(event.pos)
            if not self.board[ind]:
                self.board[ind] = self.turn
                self.turn = -self.turn
                if self.mode and self.turn != self.player:
                    self.pause = True
                    if self.check_win() == None:
                        self.bot_play()
                        self.pause = False

                if self.check_win():
                    self.pause = True

    def bot_play(self):
        self.board = self.bot_rl.play(self.board, -self.player)
        self.turn = -self.turn

    def mpos_to_ind(self, m_pos):
        x = m_pos[0] - self.x
        y = m_pos[1] - self.y
        return x // 140 + 3 * (y // 140)

    def check_win(self):
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
            if (
                self.board[a] == self.board[b] == self.board[c]
                and self.board[a] is not None
            ):
                return self.board[a]

        if all(cell is not None for cell in self.board):
            return 0

        return None

    def to_pause(self):
        self.pause = not self.pause

    def switch_player(self):
        self.player = -self.player
        self.init_board()

    def switch_mode(self):
        self.mode = 1 - self.mode
