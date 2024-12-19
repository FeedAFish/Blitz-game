from utils import elements
import pygame


class Lines98(elements.Board):
    def __init__(self, x, y, image_path=None):
        super().__init__(x, y, image_path)
        self.grid_size = 40
        self.board_size = 420 // self.grid_size
        self.width = self.height = self.grid_size * self.board_size
        self.init_board()
        self.load_image_and_font()

    def init_board(self):
        self.board = [None] * self.board_size**2
        self.score = 0

    def load_image_and_font(self):
        self.font = pygame.font.Font("./font/LovelyKids-gxly4.ttf", 35)
        list_file = ["img/banana.png", "img/grape.png"]
        self.list_image = [
            pygame.image.load(file).convert_alpha() for file in list_file
        ]

    def draw(self, surface):
        super().draw(surface)
        self.draw_grid(surface)
        self.draw_elements(surface)
        self.draw_result(surface)

    def draw_grid(self, surface):
        pass

    def draw_elements(self, surface):
        pass

    def draw_result(self, surface):
        pass

    def on_click(self, event):
        pass

    def ball_move(self):
        pass


SIZE = 10


def adjacent(place) -> set:
    result = set()
    if place % SIZE != 0:
        result.add(place - 1)
    if place % SIZE != SIZE - 1:
        result.add(place + 1)
    if place // SIZE != 0:
        result.add(place - SIZE)
    if place // SIZE != SIZE - 1:
        result.add(place + SIZE)
    return result


def adjacents(places: list) -> set:
    result = set()
    for place in places:
        result.update(adjacent(place))
    return result


def is_reachable(dest, start: set, board, passed_place: set = set()) -> bool:
    if dest in start:
        return True
    if len(start) == 0:
        return False

    new_start = {
        place
        for place in adjacents(start)
        if board[place] == 0 and place not in passed_place
    }
    passed_place.update(new_start)
    return is_reachable(dest, new_start, board, passed_place)
