from utils import elements
import pygame
import random


class Lines98(elements.Board):
    def __init__(self, x, y, image_path=None):
        super().__init__(x, y, image_path)
        self.grid_size = 40
        self.board_size = 420 // self.grid_size
        self.width = self.height = self.grid_size * self.board_size
        self.hover_rect = self.rect.inflate(
            -(420 - self.width) - 1 / 2, -(420 - self.width) / 2 - 1
        )
        self.init_board()
        self.load_image_and_font()

    # Reinitiate the board
    def init_board(self):
        self.board = [None] * self.board_size**2
        self.clicked = None
        self.angle = 0
        self.board[0] = 1
        self.board[1] = 1
        self.board[10] = 4
        self.score = 0
        self.pause = False

    def load_image_and_font(self):  # Load image for Lines98
        self.font = pygame.font.Font("./font/LovelyKids-gxly4.ttf", 35)
        list_file = [f"img/star {i+1}.png" for i in range(8)]
        self.list_image = [
            pygame.image.load(file).convert_alpha() for file in list_file
        ]
        random.shuffle(self.list_image)

    # Draw board on surface
    def draw(self, surface):
        super().draw(surface)
        if self.clicked != None:
            self.angle += 1
        self.draw_grid(surface)
        self.draw_elements(surface)
        self.draw_result(surface)

    def draw_grid(self, surface):  # Draw grid for the board
        for i in range(self.board_size + 1):
            pygame.draw.line(
                surface,
                (128, 128, 128),
                (
                    self.x + (420 - self.width) // 2 + self.grid_size * i,
                    self.y + (420 - self.width) // 2,
                ),
                (
                    self.x + (420 - self.width) // 2 + self.grid_size * i,
                    self.y + self.width + (420 - self.width) // 2,
                ),
                3,
            )
        for i in range(self.board_size + 1):
            pygame.draw.line(
                surface,
                (128, 128, 128),
                (
                    self.x + (420 - self.width) // 2,
                    self.y + (420 - self.width) // 2 + self.grid_size * i,
                ),
                (
                    self.x + self.width + (420 - self.width) // 2,
                    self.y + (420 - self.width) // 2 + self.grid_size * i,
                ),
                3,
            )

    def draw_elements(self, surface):  # Draw elements inside the board
        for i in range(self.board_size**2):
            if self.board[i]:
                if i == self.clicked:
                    rotated_image = pygame.transform.rotate(
                        self.list_image[self.board[i] - 1], self.angle
                    )
                    surface.blit(
                        rotated_image,
                        (
                            self.x
                            + (420 - self.width) // 2
                            + (i % self.board_size) * self.grid_size
                            + 5,
                            self.y
                            + (420 - self.width) // 2
                            + (i // self.board_size) * self.grid_size
                            + 5,
                        ),
                    )
                else:
                    surface.blit(
                        self.list_image[self.board[i] - 1],
                        (
                            self.x
                            + (420 - self.width) // 2
                            + (i % self.board_size) * self.grid_size
                            + 5,
                            self.y
                            + (420 - self.width) // 2
                            + (i // self.board_size) * self.grid_size
                            + 5,
                        ),
                    )

    def draw_result(self, surface):  # Show result
        pass

    # Action on click
    def on_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hover_rect.collidepoint(event.pos):
                ind_clicked = self.mpos_to_ind(event.pos)

                # Reclick equal cancel clicked animation
                if self.clicked == ind_clicked:
                    self.clicked = None
                    self.angle = 0
                # No star clicked -> the star is now clicked
                elif self.clicked == None:
                    if self.board[ind_clicked]:
                        self.clicked = ind_clicked

                # Move the star if is reachable
                elif self.is_reachable(ind_clicked, {self.clicked}, self.board, None):
                    self.board[ind_clicked] = self.board[self.clicked]
                    self.board[self.clicked] = None
                    self.clicked = None
                    self.angle = 0

    def mpos_to_ind(self, mpos) -> int:  # Mouse Position to Indice on board
        x = mpos[0] - self.x - (420 - self.width) // 2
        y = mpos[1] - self.y - (420 - self.width) // 2
        ind = x // self.grid_size + y // self.grid_size * self.board_size
        return ind

    # BFS to indicate if a star cn move to a position
    def adjacent(self, place) -> set:  # Return adjacent indice of grid
        result = set()
        if place % self.board_size != 0:
            result.add(place - 1)
        if place % self.board_size != self.board_size - 1:
            result.add(place + 1)
        if place // self.board_size != 0:
            result.add(place - self.board_size)
        if place // self.board_size != self.board_size - 1:
            result.add(place + self.board_size)
        return result

    def adjacents(self, places: list) -> set:  # Get adjacent by list
        result = set()
        for place in places:
            result.update(self.adjacent(place))
        return result

    def is_reachable(
        self, dest, start: set, board, passed_place: set = None
    ) -> (
        bool
    ):  # Return True if the destination (dest) can be reached from the starting (start) position
        if passed_place is None:
            passed_place = set()
        if dest in start:
            return True
        if len(start) == 0:
            return False
        new_start = {
            place
            for place in self.adjacents(start)
            if board[place] is None and place not in passed_place
        }
        passed_place.update(new_start)
        return self.is_reachable(dest, new_start, board, passed_place)

    # In dev
    def ball_move(self):
        pass

    def print(self):
        for i in range(self.board_size):
            print(
                self.board[i * self.board_size : i * self.board_size + self.board_size]
            )
