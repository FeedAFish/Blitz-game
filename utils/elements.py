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
        font_path="./data/font/LovelyKids-gxly4.ttf",
        action=None,
    ):
        # Load the image and font
        try:
            self.original_image = pygame.image.load(image_path).convert_alpha()
        except:
            pygame.quit()
            sys.exit()
        self.font = (
            pygame.font.Font(font_path, 35)
            if font_path
            else pygame.font.SysFont(None, 35)
        )
        self.action = action if action else lambda: None

        # Resize image if it's too large (optional)
        max_width = 160
        original_width = self.original_image.get_width()
        if original_width > max_width:
            aspect_ratio = self.original_image.get_height() / original_width
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

    # Draw button on surface
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
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
        else:
            self.image = None

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
        self.hover_rect = self.rect.inflate(-5, -5)
        self.mode = 1
        self.player = -1
        try:
            self.bot_rl = bots.TicTacToeBot.load("data/bot/test_1.pkl")
        except FileNotFoundError:
            print("Bot file not found. Please ensure 'test_1.pkl' exists.")
            pygame.quit()
            sys.exit()
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

    def load_image(self):  # Load images for game
        def load_image_with_default(path, default_color=(255, 255, 255)):
            try:
                return pygame.image.load(path).convert_alpha()
            except pygame.error:
                # Create a default surface if image is not found
                surface = pygame.Surface((100, 100))
                surface.fill(default_color)
                return surface

        # Load images for game
        self.list_image = [
            load_image_with_default("data/img/banana.png"),
            load_image_with_default("data/img/grape.png"),
        ]
        self.list_result = [
            load_image_with_default("data/img/banana_w.png"),
            load_image_with_default("data/img/draw.png"),
            load_image_with_default("data/img/grape_w.png"),
        ]
        self.list_result = [
            pygame.image.load("data/img/banana_w.png").convert_alpha(),
            pygame.image.load("data/img/draw.png").convert_alpha(),
            pygame.image.load("data/img/grape_w.png").convert_alpha(),
        ]

    # Draw board
    def draw(self, surface):
        super().draw(surface)
        self.draw_grid(surface)
        self.draw_tic_tac_toe(surface)
        self.draw_result(surface)

    def draw_grid(self, surface):  # Draw grid for the board
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

    def draw_tic_tac_toe(self, surface):  # Draw tic-tac-toe on board
        for i in range(9):
            if self.board[i]:
                surface.blit(
                    self.list_image[(self.board[i] + 1) // 2],
                    (self.x + 140 * (i % 3), self.y + 140 * (i // 3)),
                )

    def draw_result(self, surface):  # Show result if match is finished
        if self.check_win() != None:
            surface.blit(
                self.list_result[self.check_win() + 1],
                (620, 50),
            )

    # Action on click
    def on_click(self, event):
        # Action on left click inside the board
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.pause and self.hover_rect.collidepoint(event.pos):
                ind = self.mpos_to_ind(event.pos)
                # Check position is available
                if not self.board[ind]:
                    self.board[ind] = self.turn
                    self.turn = -self.turn

                    # For PVE
                    if self.mode and self.turn != self.player:
                        self.pause = True
                        if self.check_win() is None:
                            self.bot_play()
                            self.pause = False

                    # Check winner each round
                    if self.check_win():
                        self.pause = True

    # Action on bot PVE
    def bot_play(self):
        self.board = self.bot_rl.play(self.board, -self.player)
        self.turn = -self.turn

    def mpos_to_ind(self, m_pos):  # Mouse Position to Indice on board
        x = m_pos[0] - self.x
        y = m_pos[1] - self.y
        return x // 140 + 3 * (y // 140)

    def check_win(self):  # Function for check winner
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

    # Manage gameplay
    def to_pause(self):
        self.pause = not self.pause

    def switch_player(self):
        self.player = -self.player
        self.init_board()

    def switch_mode(self):
        self.mode = 1 - self.mode
        self.init_board()


class Board_Snake(Board):
    def __init__(self, x, y, image_path=None):
        super().__init__(x, y, image_path)
        self.load_color_and_font()
        self.grid_size = 30
        self.width = 420 // self.grid_size
        self.height = 420 // self.grid_size
        self.init_board()

    def load_color_and_font(self):  # Load font and set color for game
        self.font = pygame.font.Font("./data/font/LovelyKids-gxly4.ttf", 35)
        self.s_color = (255, 0, 0)
        self.f_color = (0, 255, 0)

    # Reinitiate the board
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

    # Spawn food on board
    def spawn_food(self):
        while True:
            food_pos = (
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1),
            )
            if food_pos not in self.snake:
                return food_pos

    # Draw board on surface
    def draw(self, surface):
        # Snake move before board redrawn
        if not self.pause:
            self.move()

        # Board redrawn
        super().draw(surface)
        self.draw_snake(surface)
        self.draw_food(surface)
        self.draw_score(surface)

    def move(self):  # Snake moves
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
            self.speed = min(self.speed * 1.02, 20)  # Set a maximum speed limit of 20
        else:
            # Remove tail if food not eaten
            self.snake.pop()

        # Allow direction change again
        self.change_d = False

    def draw_snake(self, surface):  # Draw snake on board
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

    def draw_food(self, surface):  # Draw food
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

    def draw_score(self, surface):  # Score shown on surface
        text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = (700, 100)
        surface.blit(text, rect)

    # Handle click/key-stroke event
    # Handle moving on pressing arrow keys
    def on_click(self, event):
        if (
            event.type == pygame.KEYDOWN
            and not self.pause
            and not self.end
            # Prevent 2 time changing direction
            and not self.change_d
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


class Lines98(Board):
    def __init__(self, x, y, image_path=None):
        super().__init__(x, y, image_path)
        self.grid_size = 40
        self.sizing_board()

        # Load sound and images
        self.load_sound()
        self.load_image_and_font()
        self.init_board()

    def sizing_board(self):  # Change board adapt to grid size
        self.board_size = 420 // self.grid_size
        self.width = self.height = self.grid_size * self.board_size
        self.hover_rect = self.rect.inflate(
            -(420 - self.width) - 1 / 2, -(420 - self.width) / 2 - 1
        )

    def load_sound(self):  # Load sound for Lines98
        self.error_sound = pygame.mixer.Sound("data/sound/error.mp3")
        self.point_sound = pygame.mixer.Sound("data/sound/point.mp3")
        self.loss_sound = pygame.mixer.Sound("data/sound/loss.mp3")

    def load_image_and_font(self):  # Load image for Lines98
        self.font = pygame.font.Font("./data/font/LovelyKids-gxly4.ttf", 35)
        list_file = [f"data/img/star {i+1}.png" for i in range(8)]
        self.list_image = [
            pygame.transform.scale(
                pygame.image.load(file).convert_alpha(),
                (self.grid_size - 10, self.grid_size - 10),
            )
            for file in list_file
        ]
        self.list_small = [
            pygame.transform.scale(
                pygame.image.load(file).convert_alpha(),
                ((self.grid_size - 10) // 2, (self.grid_size - 10) // 2),
            )
            for file in list_file
        ]

    # Reinitiate the board
    def init_board(self):
        self.board = [None] * self.board_size**2
        self.clicked = None
        self.angle = 0

        start_list = random.sample(self.get_available_grid(), 4)
        for i in range(4):
            self.board[start_list[i]] = random.randint(1, 8)
        self.next_stars = random.sample(self.get_available_grid(), 3)

        self.next_colors = [random.randint(1, 8) for _ in range(3)]
        self.score = 0
        self.pause = False

    # Change grid size
    def grid_change(self):
        self.grid_size = 90 - self.grid_size
        self.sizing_board()
        self.load_image_and_font()
        self.init_board()

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
        for i in self.next_stars:  # Draw next stars
            surface.blit(
                self.list_small[self.next_colors[self.next_stars.index(i)] - 1],
                (
                    self.x
                    + (420 - self.width) // 2
                    + (i % self.board_size) * self.grid_size
                    + (self.grid_size - 10) // 4
                    + 5,
                    self.y
                    + (420 - self.width) // 2
                    + (i // self.board_size) * self.grid_size
                    + (self.grid_size - 10) // 4
                    + 5,
                ),
            )

        for i in range(self.board_size**2):  # Draw stars
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
        text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = (700, 100)
        surface.blit(text, rect)
        if self.pause:
            text = self.font.render("Game Over", True, (0, 0, 0))
            rect = text.get_rect()
            rect.center = (700, 150)
            surface.blit(text, rect)

    # Action on click
    def on_click(self, event):
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and not self.pause
        ):  # Left click
            if self.hover_rect.collidepoint(event.pos):
                ind_clicked = self.mpos_to_ind(event.pos)

                if self.board[ind_clicked]:
                    if self.clicked != ind_clicked:  # The star is now clicked
                        self.clicked = ind_clicked
                    elif (
                        self.clicked == ind_clicked
                    ):  # Reclick equal cancel clicked animation
                        self.clicked = None
                        self.angle = 0
                # Move the star if is reachable
                elif self.clicked != None:
                    if self.is_reachable(ind_clicked, {self.clicked}, None):
                        self.move(self.clicked, ind_clicked)
                        current = self.score
                        self.get_point()
                        if current == self.score:
                            self.add_next_stars()
                            self.get_point()
                        if current != self.score:
                            pygame.mixer.Sound.play(self.point_sound)
                    else:
                        pygame.mixer.Sound.play(self.error_sound)

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
        self, dest, start: set, passed_place: set = None
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
            if self.board[place] is None and place not in passed_place
        }
        passed_place.update(new_start)
        return self.is_reachable(dest, new_start, passed_place)

    # Moving action
    def move(self, start, dest) -> list:  # Move star from start to dest
        self.board[dest] = self.board[start]
        self.board[start] = None
        self.clicked = None
        self.angle = 0

    def get_available_grid(self) -> list:  # Get all available places on the board
        result = [i for i in range(self.board_size**2) if self.board[i] is None]
        return result

    def get_point(
        self,
    ):  # Calculate total of stars that create at least 5 consecutive stars
        to_clear_indices = set()

        # Check rows
        for i in range(self.board_size):
            row = self.board[i * self.board_size : (i + 1) * self.board_size]
            row_indices = [(i, j) for j in range(self.board_size)]
            to_clear_indices.update(self.find_consecutive(row, row_indices))

        # Check columns
        for j in range(self.board_size):
            col = [self.board[i * self.board_size + j] for i in range(self.board_size)]
            col_indices = [(i, j) for i in range(self.board_size)]
            to_clear_indices.update(self.find_consecutive(col, col_indices))

        # Check diagonals (top-left to bottom-right)
        for start in range(
            -self.board_size + 1, self.board_size
        ):  # start determines which diagonal, from top-left to bottom-right
            diag = []
            diag_indices = []
            for i in range(self.board_size):
                j = i + start
                if 0 <= i < self.board_size and 0 <= j < self.board_size:
                    diag.append(self.board[i * self.board_size + j])
                    diag_indices.append((i, j))
            to_clear_indices.update(self.find_consecutive(diag, diag_indices))
        self.clear_line(to_clear_indices)

    def add_next_stars(self):  # Add next balls to the board
        for i in range(len(self.next_stars)):
            if self.board[self.next_stars[i]] is None:
                self.board[self.next_stars[i]] = self.next_colors[i]
            else:
                self.board[random.choice(self.get_available_grid())] = self.next_colors[
                    i
                ]
        recent = self.next_stars
        if self.get_available_grid():
            self.next_stars = random.sample(
                self.get_available_grid(), min(3, len(self.get_available_grid()))
            )
        else:  # Game over if no place available
            pygame.mixer.Sound.play(self.loss_sound)
            self.pause = True

        self.next_colors = [random.randint(1, 8) for _ in range(len(self.next_stars))]

    def clear_line(self, indices):  # Clear by indices
        for i, j in indices:
            self.board[i * self.board_size + j] = None

    def find_consecutive(self, lst, start_indices):  # Find consecutive stars
        count = 1
        to_clear = []
        for k in range(1, len(lst)):
            if lst[k] == lst[k - 1] and lst[k] != None:
                count += 1
            else:
                if count >= 5:
                    to_clear.extend(start_indices[k - count : k])
                    self.score += count + (count - 5) ** 2  # Score calculation
                count = 1
        if count >= 5:
            to_clear.extend(start_indices[-count:])
            self.score += count + (count - 5) ** 2  # Score calculation
        return to_clear
