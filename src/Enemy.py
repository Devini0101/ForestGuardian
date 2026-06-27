import pygame
from src.Const import GHOST, TAMANHO_GHOST, GHOST_RIGHT
from src.Entity import Entity

class Enemy(Entity):
    def __init__(self, x: int, y: int, speed: int, player):
        super().__init__(x, y, 40, 40, (255, 0, 0))
        self.__speed = speed

        ghost_left = pygame.image.load(GHOST).convert_alpha()
        ghost_right = pygame.image.load(GHOST_RIGHT).convert_alpha()
        self.img_right = pygame.transform.scale(ghost_right, TAMANHO_GHOST)
        self.img_left = pygame.transform.scale(ghost_left, TAMANHO_GHOST)

        self.image = self.img_left
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(0, 0, 30, 35)
        self.hitbox.center = self.rect.center  # Centraliza o hitbox no fantasma

        self.player = player  # Guarda a referência do jogador
        self.lives = 1 #inimigo tem 1 hit de vida

    def update(self):
        distancia_x = self.player.rect.x - self.rect.x

        # abs() transforma número negativo em positivo.
        # Isso evita que o fantasma fique "tremendo" quando chegar exatamente na mesma posição do player.
        if abs(distancia_x) > self.__speed:
            if self.rect.x < self.player.rect.x:
                self.rect.x += self.__speed  # Persegue para a direita
                self.image = self.img_right
            elif self.rect.x > self.player.rect.x:
                self.rect.x -= self.__speed  # Persegue para a esquerda
                self.image = self.img_left

        self.hitbox.center = self.rect.center

    def hit(self):
        self.lives -=1
        if self.lives <=0:
            self.kill() #remove do sprite e morre