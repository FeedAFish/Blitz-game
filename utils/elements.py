import pygame
import sys
import random
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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.pause and self.hover_rect.collidepoint(event.pos):
                ind = self.mpos_to_ind(event.pos)

                if not self.board[ind]:
                    self.board[ind] = self.turn
                    self.turn = -self.turn

                    if self.mode and self.turn != self.player:
                        self.pause = True
                        if self.check_win() is None:
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


class Board_Snake(Board):
    def __init__(self, x, y, image_path=None):
        super().__init__(x, y, image_path)
        self.load_color_and_font()
        self.grid_size = 30
        self.width = 420 / self.grid_size
        self.height = 420 / self.grid_size
        self.init_board()

    def load_color_and_font(self):
        self.font = pygame.font.Font("./font/LovelyKids-gxly4.ttf", 35)
        self.s_color = (255, 0, 0)
        self.f_color = (0, 255, 0)

    def init_board(self):
        self.pause = False
        self.end = False
        self.snake = [(5, 5)]
        self.food = self.spawn_food()
        self.direction = (1, 0)

        # Prevent 2 times direction change
        self.change_d = False

        # Score and speed
        self.score = 0
        self.speed = 6

    def spawn_food(self):
        while True:
            food_pos = (
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1),
            )
            if food_pos not in self.snake:
                return food_pos

    def draw(self, surface):
        if not self.pause:
            self.move()
        super().draw(surface)
        self.draw_snake(surface)
        self.draw_food(surface)
        self.draw_score(surface)

    def move(self):
        head = self.snake[0]
        new_head = (
            (head[0] + self.direction[0]) % self.width,
            (head[1] + self.direction[1]) % self.height,
        )

        # Check for self-collision
        if new_head in self.snake[1:]:
            self.pause = True
            self.end = True
            return

        self.snake.insert(0, new_head)

        # Check if food is eaten
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()

            # Increase speed by 2%
            self.speed *= 1.02
        else:
            # Remove tail if food not eaten
            self.snake.pop()

        # Allow direction change again
        self.change_d = False

    def draw_snake(self, surface):
        # Draw head
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (
                90 + self.snake[0][0] * self.grid_size,
                90 + self.snake[0][1] * self.grid_size,
                self.grid_size - 1,
                self.grid_size - 1,
            ),
        )

        # Draw body
        for segment in self.snake[1:]:
            pygame.draw.rect(
                surface,
                self.s_color,
                (
                    90 + segment[0] * self.grid_size,
                    90 + segment[1] * self.grid_size,
                    self.grid_size - 1,
                    self.grid_size - 1,
                ),
            )

    def draw_food(self, surface):
        # Draw food
        pygame.draw.rect(
            surface,
            self.f_color,
            (
                90 + self.food[0] * self.grid_size,
                90 + self.food[1] * self.grid_size,
                self.grid_size - 1,
                self.grid_size - 1,
            ),
        )

    def draw_score(self, surface):
        text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = (700, 100)
        surface.blit(text, rect)

    def on_click(self, event):
        if (
            event.type == pygame.KEYDOWN
            and not self.pause
            and not self.change_d
            and not self.end
        ):
            # Prevent turning back on itself
            if event.key == pygame.K_UP and self.direction != (0, 1):
                self.direction = (0, -1)
                self.change_d = True
            elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                self.direction = (0, 1)
                self.change_d = True
            elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                self.direction = (-1, 0)
                self.change_d = True
            elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                self.direction = (1, 0)
                self.change_d = True

    def get_speed(self):
        return self.speed

    def pause_trig(self):
        if not self.snake[0] in self.snake[1:]:
            self.pause = not self.pause
