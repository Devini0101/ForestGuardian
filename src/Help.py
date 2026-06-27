import pygame
from src.Const import WIN_WIDTH, WIN_HEIGHT, C_WHITE, C_ORANGE

class Help:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.SysFont("Lucida Sans Typewriter", 25)

    def run(self):
        running = True
        while running:
            # Fundo preto ou uma imagem de tutorial
            self.window.fill((0, 0, 0))

            # Título
            self.draw_text("Comandos do Guardião", 50, C_ORANGE, WIN_WIDTH / 2, 100)

            # Lista de Comandos
            commands = [
                "SETAS: Mover",
                "SETA CIMA: Pular",
                "ESC: Voltar ao Menu"
            ]

            for i, cmd in enumerate(commands):
                self.draw_text(cmd, 30, C_WHITE, WIN_WIDTH / 2, 200 + (i * 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Pressionar ESC para voltar
                        running = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont("Lucida Sans Typewriter", size)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(x, y))
        self.window.blit(surf, rect)