from utils import elements
import pygame


class Animal(elements.Board):
    def __init__(self, x, y, image_path=None):
        super().__init__(x, y, image_path)
        self.grid_size = [30, 40]
        self.board_size = [400 // 30, 400 // 40]
        self.board = [[0] * self.board_size[1] for _ in range(self.board_size[0])]
        self.load_image()

    def init_board(self):
        pass

    def load_image(self):
        self.mahjong = pygame.transform.scale(
            pygame.image.load(r"./data/img/grape.png"), (30, 39)
        )

    def draw(self, surface):
        super().draw(surface)
        self.draw_elements(surface)

    def draw_elements(self, surface):
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                if self.board[i][j] == 0:
                    self.draw_one_element(surface, (i, j), self.board[i][j])

    def draw_one_element(self, surface, pos, element):
        surface.blit(
            self.mahjong,
            (100 + pos[0] * self.grid_size[0], 100 + pos[1] * self.grid_size[1]),
        )
