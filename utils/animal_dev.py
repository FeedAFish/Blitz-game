from utils import elements
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
        self.grid_size = [30, 40]
        self.board_size = [400 // 30, 400 // 40]
        self.x = 100
        self.y = 100
        self.hover_rect = pygame.rect.Rect(
            100, 100, self.board_size[0] * 30, self.board_size[1] * 40
        )
        self.init_board()
        self.load_image()

    def init_board(self):
        self.clicked = None
        self.board = [
            [0] * (self.board_size[1] + 2) for _ in (range(self.board_size[0] + 2))
        ]
        for i in range(3):
            for j in range(3):
                self.board[i + 1][j + 1] = 1
        # for i in range(self.board_size[0]):
        #     for j in range(self.board_size[1]):
        #         self.board[i + 1][j + 1] = 1

    def load_image(self):
        self.mahjong = pygame.transform.scale(
            pygame.image.load(r"./data/img/grape.png"), (30, 39)
        )

    def draw(self, surface):
        super().draw(surface)
        self.draw_elements(surface)
        if self.clicked:
            pygame.draw.rect(
                surface,
                (0, 0, 0),
                (
                    100 + self.clicked[0] * self.grid_size[0] - 30,
                    100 + self.clicked[1] * self.grid_size[1] - 40,
                    30,
                    40,
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
                (100 + pos[0] * self.grid_size[0], 100 + pos[1] * self.grid_size[1]),
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

                if 0 <= new_x < self.board_size[0] and 0 <= new_y < self.board_size[1]:
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
        return (x // 30) + 1, (y // 40) + 1

    def on_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hover_rect.collidepoint(event.pos):
                pos = self.mpos_to_ind(event.pos)
                if (
                    self.clicked
                    and self.board[pos[0]][pos[1]]
                    and self.board[self.clicked[0]][self.clicked[1]]
                    == self.board[pos[0]][pos[1]]
                ):
                    path = self.is_reachable(self.clicked, pos)
                    print(f"Clicked : {self.clicked}, Dest : {pos}")
                    if path:
                        print(path)
                    self.clicked = None
                elif self.clicked:
                    self.clicked = None
                else:
                    if self.board[pos[0]][pos[1]]:
                        self.clicked = pos
