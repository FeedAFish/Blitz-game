from utils import elements
import pygame

SPEED = 0.05
SIZE_REDUCE = 10


class Gem(elements.Element):
    def __init__(self, x, y, color_num, image_path=None):
        self.grid_size = 40
        self.color = color_num
        self.x = x
        self.y = y - 2 if y < 2 else y - 1 if y < 4 else y
        self.target_y = y

    def draw(self, surface, image):
        surface.blit(
            image,
            (
                SIZE_REDUCE // 2 + self.x * self.grid_size,
                SIZE_REDUCE // 2 + self.y * self.grid_size,
            ),
        )

    def update_position(self):
        if self.y == self.target_y:
            return False
        self.y = min(self.target_y, self.y + SPEED)
        return True


class Board_Bejeweled(elements.Board):
    def __init__(self, x, y, image_path=None):
        super().__init__(x, y, image_path)
        self.grid_size = 40
        self.board_size = 420 // self.grid_size
        self.x = 100
        self.y = 100
        self.width = self.grid_size * self.board_size

        self.load_image()
        self.load_font()
        self.init_board()

    def init_board(self):
        self.board = [
            [Gem(j, i, j % 7) for i in range(self.board_size)]
            for j in range(self.board_size)
        ]
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
        self.move()
        super().draw(surface)
        self.draw_grid(surface)
        self.draw_gems(surface)

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
                    self.mask_canvas, self.gems[self.board[i][j].color]
                )

        surface.blit(self.mask_canvas, (self.x, self.y))

    def move(self):
        self.animation = False
        for i in self.board:
            for j in i:
                if j.update_position():
                    self.animation = True
        if not self.animation:
            self.pause = False
