import pygame
import sys
import pickle as pkl
from utils import elements


class Game:
    def __init__(self, width, height, background_path="img/bg.png"):
        pygame.init()
        pygame.display.set_caption("Blitz Game")
        self.running = True
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.main_bg = pygame.image.load(background_path).convert_alpha()
        self.board = pygame.image.load("img/board_bg.png").convert_alpha()
        self.main_menu()

    # Main Menu
    def main_menu(self):
        self.background = self.main_bg
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
                    image_path="./img/cloud_button.png",
                    text=menu,
                    action=action,
                )
            )
            y_pos += 110

    # Game choice menu
    def choice_menu(self):
        self.background = self.main_bg
        self.load_list = []
        self.add_choice_buttons()

    def add_choice_buttons(self):
        menus = {
            "Tic-Tac-Toe": self.board_ttt,
            "Back": self.main_menu,
        }
        y_pos = 300 - len(menus) * 55 + 55
        for menu, action in menus.items():
            self.load_list.append(
                elements.Button(
                    x=150,
                    y=y_pos,
                    image_path="./img/cloud_button.png",
                    text=menu,
                    action=action,
                )
            )
            y_pos += 110

    # Board
    def board_ttt(self):
        self.background = self.board
        self.load_list = []
        self.load_list.append(elements.Board_TTT(90, 90))
        self.load_list.append(
            elements.Button(
                x=700,
                y=200,
                image_path="./img/wooden_button.png",
                text="Restart",
                action=self.load_list[0].init_board,
            )
        )
        self.load_list.append(
            elements.Button(
                x=700,
                y=280,
                image_path="./img/wooden_button.png",
                text="Main Menu",
                action=self.main_menu,
            )
        )
        self.load_list.append(
            elements.Button(
                x=700,
                y=360,
                image_path="./img/wooden_button.png",
                text="Switch player",
                action=self.load_list[0].switch_player,
            )
        )

        self.load_list.append(
            elements.Button(
                x=700,
                y=440,
                image_path="./img/wooden_button.png",
                text="Switch mode",
                action=self.load_list[0].switch_mode,
            )
        )

    # Handle in-app events
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
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
            self.clock.tick(60)
            self.handle_events()
            self.draw()

        # Quit Pygame
        self.exit()

    def exit(self):
        pygame.quit()
        sys.exit()
