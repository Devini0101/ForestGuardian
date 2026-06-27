import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple):
        super().__init__()
        # Cria uma superfície (retângulo colorido) para representar a entidade
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        # Pega o retângulo dessa imagem para tratar posicionamento e colisão
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass