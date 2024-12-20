import pygame
import sys
from utils import elements


class Game:
    def __init__(self, width, height, background_path="data/img/bg.png"):
        pygame.init()
        pygame.display.set_caption("Blitz Game")
        self.running = True
        self.fps_base = False
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.main_bg = pygame.image.load(background_path).convert_alpha()
        self.board = pygame.image.load("data/img/board_bg.png").convert_alpha()
        self.main_menu()

    # Main Menu
    def main_menu(self):
        self.background = self.main_bg
        self.fps = 60
        self.fps_base = False
        self.load_list = []
        self.add_menu_buttons()

    def add_menu_buttons(self):
        menus = {"Play": self.choice_menu, "Exit": self.exit}
        y_pos = 300
        for menu, action in menus.items():
            self.load_list.append(
                elements.Button(
                    x=150,
                    y=y_pos,
                    image_path="./data/img/cloud_button.png",
                    text=menu,
                    action=action,
                )
            )
            y_pos += 110

    # Game choice menu
    def choice_menu(self):
        self.background = self.main_bg
        self.fps = 60
        self.fps_base = False
        self.load_list = []
        self.add_choice_buttons()

    def add_choice_buttons(self):
        menus = {
            "Tic-Tac-Toe": self.board_ttt,
            "Snake": self.board_snake,
            "Lines 98": self.board_lines,
            "Back": self.main_menu,
        }
        y_pos = 300 - len(menus) * 55 + 55
        for menu, action in menus.items():
            self.load_list.append(
                elements.Button(
                    x=150,
                    y=y_pos,
                    image_path="./data/img/cloud_button.png",
                    text=menu,
                    action=action,
                )
            )
            y_pos += 110

    # Board_TTT
    def board_ttt(self):
        self.background = self.board
        self.fps = 60
        self.fps_base = False
        self.load_list = []
        self.load_list.append(elements.Board_TTT(90, 90))
        self.load_list.append(
            elements.Button(
                x=700,
                y=200,
                image_path="./data/img/wooden_button.png",
                text="Restart",
                action=self.load_list[0].init_board,
            )
        )
        self.load_list.append(
            elements.Button(
                x=700,
                y=280,
                image_path="./data/img/wooden_button.png",
                text="Main Menu",
                action=self.main_menu,
            )
        )
        self.load_list.append(
            elements.Button(
                x=700,
                y=360,
                image_path="./data/img/wooden_button.png",
                text="Switch player",
                action=self.load_list[0].switch_player,
            )
        )

        self.load_list.append(
            elements.Button(
                x=700,
                y=440,
                image_path="./data/img/wooden_button.png",
                text="Switch mode",
                action=self.load_list[0].switch_mode,
            )
        )

    # Board Snake
    def board_snake(self):
        self.background = self.board
        self.fps = 10
        self.fps_base = True
        self.load_list = []
        self.load_list.append(elements.Board_Snake(90, 90))
        self.load_list.append(
            elements.Button(
                x=700,
                y=200,
                image_path="./data/img/wooden_button.png",
                text="Restart",
                action=self.load_list[0].init_board,
            )
        )
        self.load_list.append(
            elements.Button(
                x=700,
                y=280,
                image_path="./data/img/wooden_button.png",
                text="Main Menu",
                action=self.main_menu,
            )
        )
        self.load_list.append(
            elements.Button(
                x=700,
                y=360,
                image_path="./data/img/wooden_button.png",
                text="Pause",
                action=self.load_list[0].pause_trig,
            )
        )

    # Board Lines
    def board_lines(self):
        self.background = self.board
        self.fps = 60
        self.fps_base = False
        self.load_list = []
        self.load_list.append(elements.Lines98(90, 90))
        self.load_list.append(
            elements.Button(
                x=700,
                y=280,
                image_path="./data/img/wooden_button.png",
                text="Restart",
                action=self.load_list[0].init_board,
            )
        )
        self.load_list.append(
            elements.Button(
                x=700,
                y=360,
                image_path="./data/img/wooden_button.png",
                text="Main Menu",
                action=self.main_menu,
            )
        )
        self.load_list.append(
            elements.Button(
                x=700,
                y=440,
                image_path="./data/img/wooden_button.png",
                text=f"Grid size: {self.load_list[0].grid_size}",
                action=self.load_list[0].grid_change,
            )
        )

    # Handle in-app events
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.exit()

            for item in self.load_list:
                item.on_click(event)

        m_pos = pygame.mouse.get_pos()
        for item in self.load_list:
            item.is_hover(m_pos)

    # Draw components
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for item in self.load_list:
            item.draw(self.screen)
        pygame.display.flip()

    # Main run
    def run(self):
        """Main game loop"""
        while self.running:
            if self.fps_base:
                self.fps = self.load_list[0].get_speed()
            self.clock.tick(self.fps)
            self.handle_events()
            self.draw()

        # Quit Pygame
        self.exit()

    def exit(self):
        pygame.quit()
        sys.exit()
