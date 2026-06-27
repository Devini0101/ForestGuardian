import pygame
from src.Menu import Menu
from src.Const import WIN_HEIGHT, WIN_WIDTH
from src.Level import Level
from src.Help import Help

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        while True:
            menu = Menu(self.window)
            # menu.run() retorna a string da opção escolhida (ex: "START" ou "PLAY")
            selected_option = menu.run()

            if selected_option == "PLAY":  # Ajuste para a string que você usa no seu MENU_OPTION
                level = Level(self.window)
                level.run()
            elif selected_option == "COMMANDS":
                helper = Help(self.window)
                helper.run()
            elif selected_option == "EXIT":
                pygame.quit()
                quit()