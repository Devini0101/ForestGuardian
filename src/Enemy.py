import pygame
from src.Const import GHOST, TAMANHO_GHOST
from src.Entity import Entity

class Enemy(Entity):
    def __init__(self, x: int, y: int, speed: int):
        super().__init__(x, y, 40, 40, (0, 0, 0))
        self.__speed = speed
        ghost_img = pygame.image.load(GHOST).convert_alpha()
        self.image = pygame.transform.scale(ghost_img, TAMANHO_GHOST)
        self.lives = 2 #inimigo tem 2 hits de vida

    def update(self):
        #movimento sempre a esquerda
        self.rect.x -= self.__speed

        #se saiu da tela, o pygame deleta ele do grupo
        if self.rect.right < 0:
            self.kill()

    def hit(self):
        self.lives -=1
        if self.lives <=0:
            self.kill() #remove do sprite e morre