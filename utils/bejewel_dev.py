from utils import elements
import pygame
import random

SPEED = 0.15
SIZE_REDUCE = 10


class Gem(elements.Element):
    def __init__(self, x, y, color_num, image_path=None):
        self.grid_size = 50
        self.color = color_num
        self.x = x
        self.y = y
        self.target_y = y
        self.target_x = x
        self.special = 0

    def draw(self, surface, image, width):
        color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        surface.blit(
            image,
            (
                SIZE_REDUCE // 2 + self.x * self.grid_size,
                SIZE_REDUCE // 2 + width - (self.y + 1) * self.grid_size,
            ),
        )
        if self.special:

            pygame.draw.rect(
                surface,
                color[self.special - 1],
                (
                    self.x * self.grid_size,
                    width - (self.y + 1) * self.grid_size,
                    self.grid_size,
                    self.grid_size,
                ),
                2,
            )

    def update_position(self):
        if self.y == self.target_y and self.x == self.target_x:
            return False

        delta_y = self.target_y - self.y
        if abs(delta_y) > SPEED:
            self.y += SPEED if delta_y > 0 else -SPEED
        else:
            self.y = self.target_y

        delta_x = self.target_x - self.x
        if abs(delta_x) > SPEED:
            self.x += SPEED if delta_x > 0 else -SPEED
        else:
            self.x = self.target_x

        return True


class Board_Bejeweled(elements.Board):
    def __init__(self, x, y, image_path=None):
        super().__init__(x, y, image_path)
        self.grid_size = 50
        self.board_size = 420 // self.grid_size
        self.x = 100
        self.y = 100
        self.width = self.grid_size * self.board_size
        self.hover_rect = pygame.Rect(self.x, self.y, self.width, self.width)
        self.load_image()
        self.load_font()
        self.init_board()

    def init_board(self):  # Create board
        self.board = [
            [Gem(j, i, random.randint(0, 6)) for i in range(self.board_size)]
            for j in range(self.board_size)
        ]  # Create a 2D array of gems by (col, row)

        self.clicked = None
        self.pause = True
        self.swap_made = None
        for i in self.board:
            for j in i:
                j.y += 2
        self.score = 0
        self.pause = True
        self.animation = True

    def load_image(self):
        self.gems = [
            pygame.image.load(f"data/img/bejeweled/bejeweled_{i}.png")
            for i in range(1, 8)
        ]
        self.gems = [
            pygame.transform.scale(
                gem, (self.grid_size - SIZE_REDUCE, self.grid_size - SIZE_REDUCE)
            )
            for gem in self.gems
        ]

    def load_font(self):
        self.font = pygame.font.Font("data/font/LovelyKids-gxly4.ttf", 25)

    def draw(self, surface):
        if self.animation:
            self.move()
        super().draw(surface)
        self.draw_grid(surface)
        self.draw_gems(surface)
        self.draw_result(surface)

    def draw_grid(self, surface):
        for i in range(self.board_size + 1):
            pygame.draw.line(
                surface,
                (128, 128, 128),
                (self.x, self.y + i * self.grid_size),
                (self.x + self.width, self.y + i * self.grid_size),
                1,
            )
            pygame.draw.line(
                surface,
                (128, 128, 128),
                (self.x + i * self.grid_size, self.y),
                (self.x + i * self.grid_size, self.y + self.width),
                1,
            )

    def draw_mask_canvas(self):
        self.mask_canvas = pygame.Surface((420, 420), pygame.SRCALPHA)
        self.mask_canvas.fill((0, 0, 0, 0))
        pygame.draw.rect(
            self.mask_canvas,
            (255, 255, 255, 255),
            (400, 400, 10, 10),
        )

    def draw_gems(self, surface):
        self.draw_mask_canvas()

        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j].draw(
                    self.mask_canvas, self.gems[self.board[i][j].color], self.width
                )
        self.draw_click()

        surface.blit(self.mask_canvas, (self.x, self.y))

    # Draw clicked on mask canvas
    def draw_click(self):
        if self.clicked:
            pygame.draw.rect(
                self.mask_canvas,
                (0, 0, 0),
                (
                    self.clicked[0] * self.grid_size,
                    self.width - (self.clicked[1] + 1) * self.grid_size,
                    self.grid_size,
                    self.grid_size,
                ),
                2,
            )

    # Draw score
    def draw_result(self, surface):
        text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = (700, 100)
        surface.blit(text, rect)

    def move(self):
        self.animation = False
        for i in self.board:
            for j in i:
                if j.update_position():
                    self.animation = True
        if not self.animation:
            self.find_regular_matches()
            self.remove_matches()
            self.add_missing_gems()

    # Mechannics
    def find_regular_matches(self):
        self.matches = set()
        self.special_vertical = set()
        self.special_horizontal = set()
        self.special_Lshape = set()

        # Check for vertical matches
        for col in range(self.board_size):
            count = 1
            for row in range(1, self.board_size):
                if self.board[col][row].color == self.board[col][row - 1].color:
                    count += 1
                else:
                    if count >= 3:
                        for i in range(count):
                            if (col, row - i - 1) in self.matches:
                                self.special_Lshape.add((col, row - i - 1))
                            self.matches.add((col, row - i - 1))
                        self.matches.update([(col, row - i - 1) for i in range(count)])
                        if count > 3:
                            self.special_vertical.add((col, row - 1))
                    count = 1
            if count >= 3:
                for i in range(count):
                    if (col, self.board_size - i - 1) in self.matches:
                        self.special_Lshape.add((col, self.board_size - i - 1))
                    self.matches.add((col, self.board_size - i - 1))
                if count > 3:
                    self.special_vertical.add((col, self.board_size - 1))

        # Check for horizontal matches
        for row in range(self.board_size):
            count = 1
            for col in range(1, self.board_size):
                if self.board[col][row].color == self.board[col - 1][row].color:
                    count += 1
                else:
                    if count >= 3:
                        for i in range(count):
                            if (col - i - 1, row) in self.matches:
                                self.special_Lshape.add((col - i - 1, row))
                            self.matches.add((col - i - 1, row))
                        if count > 3:
                            self.special_horizontal.add((col - 1, row))
                    count = 1
            if count >= 3:
                for i in range(count):
                    if (self.board_size - i - 1, row) in self.matches:
                        self.special_Lshape.add((self.board_size - i - 1, row))
                    self.matches.add((self.board_size - i - 1, row))
                if count > 3:
                    self.special_horizontal.add((self.board_size - 1, row))

    def proc_special_gems(self, gem_set: set):
        additional = set()
        for col, row in gem_set:
            if self.board[col][row].special:
                additional = self.update_additional(additional, col, row)
        additional -= self.matches

        self.matches.update(additional)
        if additional:
            self.proc_special_gems(additional)

    def update_additional(self, additional, col, row):
        if self.board[col][row].special == 1:
            additional.update([(col, i) for i in range(self.board_size)])
        elif self.board[col][row].special == 2:
            additional.update([(i, row) for i in range(self.board_size)])
        elif self.board[col][row].special == 3:
            additional.update(
                [
                    (i, j)
                    for i in range(max(0, col - 1), min(self.board_size, col + 2))
                    for j in range(max(0, row - 1), min(self.board_size, row + 2))
                ]
            )
        return additional

    def remove_matches(self):
        if len(self.matches) == 0:
            if self.swap_made:
                self.swap(
                    self.swap_made[2],
                    self.swap_made[3],
                    self.swap_made[0],
                    self.swap_made[1],
                )
            else:
                self.pause = False
            return
        self.proc_special_gems(self.matches)
        self.swap_made = None  # Reset/End swap state
        self.score += 10 * len(self.matches)  # Add score by matches
        self.animation = True  # Set animation to True to rerun self.move()

        self.matches = (
            self.matches
            - self.special_vertical
            - self.special_horizontal
            - self.special_Lshape
        )  # Keep special gems

        for col, row in self.special_horizontal:  # Special gems add
            self.board[col][row].special = 1

        for col, row in self.special_vertical:  # Special gems add
            self.board[col][row].special = 2

        for col, row in self.special_Lshape:  # Special gems add
            self.board[col][row].special = 3

        for col, row in sorted(
            self.matches, key=lambda x: (x[0], x[1]), reverse=True
        ):  # Remove gems
            self.board[col].pop(row)

    def add_missing_gems(self):
        for i, col in enumerate(self.board):
            col.extend(
                [
                    Gem(i, self.board_size + j, random.randint(0, 6))
                    for j in range(self.board_size - len(col))
                ]
            )
            for j in col:
                j.target_y = col.index(j)

    def swap(self, col1, row1, col2, row2):
        if abs(col1 - col2) + abs(row1 - row2) != 1:
            return
        self.board[col1][row1], self.board[col2][row2] = (
            self.board[col2][row2],
            self.board[col1][row1],
        )
        self.board[col1][row1].target_y = row1
        self.board[col2][row2].target_y = row2
        self.board[col1][row1].target_x = col1
        self.board[col2][row2].target_x = col2
        self.animation = True
        self.pause = True
        self.swap_made = (col1, row1, col2, row2) if not self.swap_made else None

    # Handle events
    def on_click(self, event):
        if self.pause or event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        x, y = event.pos
        if self.hover_rect.collidepoint(x, y):
            col = (x - self.x) // self.grid_size
            row = (self.width - (y - self.y)) // self.grid_size
            if not self.clicked:
                self.clicked = (col, row)
            else:
                self.swap(self.clicked[0], self.clicked[1], col, row)
                self.clicked = None
