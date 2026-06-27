import pygame
from src.Const import SEED_IMG
class Seed(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load(SEED_IMG).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90,90))
        self.rect = self.image.get_rect(center=(x, y))

        self.v_speed = -6
        self.gravity =0.4
        self.ground_y = y
        self.can_collect = False
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if self.rect.centery <= self.ground_y or self.v_speed < 0:
            self.rect.y += self.v_speed
            self.v_speed += self.gravity

            if self.rect.centery > self.ground_y:
                self.rect.centery = self.ground_y
                self.v_speed = 0

        # Só deixa o player coletar após 700 milissegundos (tempo do pulinho terminar)
        if pygame.time.get_ticks() - self.spawn_time > 700:
            self.can_collect = True