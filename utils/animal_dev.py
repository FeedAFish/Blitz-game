from utils import elements
import random
import pygame


class PathNode:
    def __init__(self, x, y, turns, direction, path):
        self.x = x
        self.y = y
        self.turns = turns
        self.direction = direction
        self.path = path if path else []


class Animal(elements.Board):
    def __init__(self, x, y, image_path=None):
        super().__init__(x, y, image_path)
        self.grid_size = [30, 50]
        self.board_size = [360 // self.grid_size[0], 400 // self.grid_size[1]]
        self.x = 120
        self.y = 100
        self.hover_rect = pygame.rect.Rect(
            self.x + 1,
            self.y + 1,
            self.board_size[0] * self.grid_size[0] - 1,
            self.board_size[1] * self.grid_size[1] - 1,
        )
        self.init_board()

    def init_board(self):
        self.clicked = None
        self.pause = False
        self.counter = 0
        self.path = None
        self.load_image()
        lst = [
            i
            for i in range(1, self.board_size[0] * self.board_size[1] // 4 + 1)
            for _ in range(4)
        ]
        random.shuffle(lst)
        self.board = [
            [0] * (self.board_size[1] + 2) for _ in (range(self.board_size[0] + 2))
        ]
        for i in range(0, self.board_size[0]):
            for j in range(0, self.board_size[1]):
                self.board[i + 1][j + 1] = lst.pop()

    def load_image(self):
        self.mahjong = pygame.transform.scale(
            pygame.image.load(r"./data/img/mahjong.png"),
            (self.grid_size[0] - 1, self.grid_size[1] - 2),
        )

        lst = random.sample(range(1, 77), self.board_size[0] * self.board_size[1] // 4)
        self.food = [
            pygame.transform.scale(
                pygame.image.load(rf"./data/img/food/food_{i}.png"), (16, 16)
            )
            for i in lst
        ]
        self.rect_element = self.food[0].get_rect()

    def draw(self, surface):
        super().draw(surface)
        self.draw_clicked(surface)
        self.draw_elements(surface)
        self.draw_matched(surface)

    def draw_clicked(self, surface):
        if self.clicked:
            pygame.draw.rect(
                surface,
                (0, 0, 0),
                (
                    self.x + self.clicked[0] * self.grid_size[0] - self.grid_size[0],
                    self.y + self.clicked[1] * self.grid_size[1] - self.grid_size[1],
                    self.grid_size[0],
                    self.grid_size[1],
                ),
                2,
            )

    def draw_elements(self, surface):
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                self.draw_one_element(surface, (i, j), self.board[i + 1][j + 1])

    def draw_one_element(self, surface, pos, element):
        if element:
            surface.blit(
                self.mahjong,
                (
                    self.x + pos[0] * self.grid_size[0],
                    self.y + pos[1] * self.grid_size[1] + 1,
                ),
            )
            self.rect_element.center = (
                self.x + pos[0] * self.grid_size[0] + self.grid_size[0] // 2,
                self.y + pos[1] * self.grid_size[1] + self.grid_size[1] // 2,
            )
            surface.blit(
                self.food[element - 1],
                self.rect_element,
            )

    def draw_matched(self, surface):
        if self.path:
            if self.counter == 20:
                self.pause = False
                self.counter = 0
                self.path = None
                return
            self.counter += 1
            for pos, npos in zip(self.path[:-1], self.path[1:]):
                self.draw_gradient_line(surface, pos, npos)

    def draw_gradient_line(self, surface, start, end):
        outline_color = (248, 212, 105)
        inline_color = (246, 154, 58)
        x_0, y_0 = (
            self.x
            - self.grid_size[0]
            + start[0] * self.grid_size[0]
            + self.grid_size[0] // 2,
            self.y
            - self.grid_size[1]
            + start[1] * self.grid_size[1]
            + self.grid_size[1] // 2,
        )
        x_1, y_1 = (
            self.x
            - self.grid_size[0]
            + end[0] * self.grid_size[0]
            + self.grid_size[0] // 2,
            self.y
            - self.grid_size[1]
            + end[1] * self.grid_size[1]
            + self.grid_size[1] // 2,
        )

        pygame.draw.line(
            surface,
            outline_color,
            (x_0, y_0),
            (x_1, y_1),
            5,
        )

        pygame.draw.line(
            surface,
            inline_color,
            (x_0, y_0),
            (x_1, y_1),
            1,
        )

    def is_reachable(
        self, start: tuple[int, int], dest: tuple[int, int], max=2
    ) -> bool:
        if not self.board:
            return None

        passed_place = set()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # right, left, down, up
        queue = []
        for i in range(4):
            queue.append(PathNode(start[0], start[1], 0, i, [start]))

        while queue:
            node = queue.pop(0)
            if node.x == dest[0] and node.y == dest[1]:
                return node.path

            for direction in directions:
                new_x = node.x + direction[0]
                new_y = node.y + direction[1]

                if (
                    0 <= new_x < self.board_size[0] + 2
                    and 0 <= new_y < self.board_size[1] + 2
                ):
                    if self.board[new_x][new_y] != 0 and (
                        new_x != dest[0] or new_y != dest[1]
                    ):
                        continue

                    new_turns = node.turns + (
                        node.direction != directions.index(direction)
                    )

                    if new_turns > max:
                        continue

                    state = (new_x, new_y, direction, new_turns)
                    if state not in passed_place:
                        passed_place.add(state)
                        queue.append(
                            PathNode(
                                new_x,
                                new_y,
                                new_turns,
                                directions.index(direction),
                                node.path + [(new_x, new_y)],
                            )
                        )

    def mpos_to_ind(self, m_pos):
        # Mouse Position to Indice on board
        x = m_pos[0] - self.x
        y = m_pos[1] - self.y
        return (x // self.grid_size[0]) + 1, (y // self.grid_size[1]) + 1

    def on_click(self, event):
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and not self.pause
        ):
            if self.hover_rect.collidepoint(event.pos):
                pos = self.mpos_to_ind(event.pos)
                if (
                    self.clicked
                    and self.clicked != pos
                    and self.board[pos[0]][pos[1]]
                    and self.board[self.clicked[0]][self.clicked[1]]
                    == self.board[pos[0]][pos[1]]
                ):
                    self.path = self.is_reachable(self.clicked, pos)
                    if self.path:
                        self.board[pos[0]][pos[1]] = self.board[self.clicked[0]][
                            self.clicked[1]
                        ] = 0
                        self.pause = True
                    self.clicked = None
                elif self.clicked:
                    self.clicked = None
                else:
                    if self.board[pos[0]][pos[1]]:
                        self.clicked = pos
