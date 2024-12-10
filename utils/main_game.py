import pygame
import sys
from utils import elements


class Game:
    def __init__(self, width, height, background_path="img/bg.png"):
        pygame.init()
        pygame.display.set_caption("Blitz Game")
        self.running = True
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.main_bg = pygame.image.load(background_path).convert_alpha()
        self.main_menu()

    # Main Menu
    def main_menu(self):
        self.background = self.main_bg
        self.load_list = []
        self.add_menu_buttons()

    def add_menu_buttons(self):
        menus = {"Play": self.choice_menu, "Exit": self.exit}
        buttons = []
        y_pos = 300
        for menu, action in menus.items():
            buttons.append(
                elements.Button(
                    x=150,
                    y=y_pos,
                    image_path="./img/cloud_button.png",
                    text=menu,
                    action=action,
                )
            )
            y_pos += 110
        self.load_list.append(buttons)

    # Game choice menu
    def choice_menu(self):
        self.background = self.main_bg
        self.load_list = []
        self.add_choice_buttons()

    def add_choice_buttons(self):
        menus = {
            "Tic-Tac-Toe": self.main_menu,
            "Back": self.main_menu,
        }
        buttons = []
        y_pos = 300 - len(menus) * 55 + 55
        for menu, action in menus.items():
            buttons.append(
                elements.Button(
                    x=150,
                    y=y_pos,
                    image_path="./img/cloud_button.png",
                    text=menu,
                    action=action,
                )
            )
            y_pos += 110
        self.load_list.append(buttons)

    # Handle in-app events
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for lists in self.load_list:
                        for item in lists:
                            item.on_click(event)

        m_pos = pygame.mouse.get_pos()
        for lists in self.load_list:
            for item in lists:
                item.is_hover(m_pos)

    # Draw components
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for item in self.load_list:
            for i in item:
                i.draw(self.screen)
        pygame.display.flip()

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
