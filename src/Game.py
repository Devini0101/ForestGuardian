import pygame
from src.Menu import Menu
from src.Const import WIN_HEIGHT, WIN_WIDTH
from src.Level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        while True:
            menu = Menu(self.window)
            # menu.run() retorna a string da opção escolhida (ex: "START" ou "PLAY")
            selected_option = menu.run()

            if selected_option == "JOGAR":  # Ajuste para a string que você usa no seu MENU_OPTION
                level = Level(self.window)
                level.run()
            elif selected_option == "SAIR":
                pygame.quit()
                quit()