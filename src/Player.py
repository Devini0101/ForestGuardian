import pygame
from src.Entity import Entity
from src.Const import GUARDIAN_FORWARD, GUARDIAN_BACK, GUARDIAN_STILL, GUARDIAN_JUMP, TAMANHO_PLAYER

class Player(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 40, 60, (0, 0, 0))
        self.__speed = 5
        self.lives = 3
        self.invulnerable_timer = 0 #tempo de invencibilidade dps de tomar um hit

        img_right = pygame.image.load(GUARDIAN_FORWARD).convert_alpha()
        self.image_right = pygame.transform.scale(img_right, TAMANHO_PLAYER)

        img_left = pygame.image.load(GUARDIAN_BACK).convert_alpha()
        self.image_left = pygame.transform.scale(img_left, TAMANHO_PLAYER)

        img_still = pygame.image.load(GUARDIAN_STILL).convert_alpha()
        self.image_still = pygame.transform.scale(img_still, TAMANHO_PLAYER)

        img_jump = pygame.image.load(GUARDIAN_JUMP).convert_alpha()
        self.image_jump = pygame.transform.scale(img_jump, TAMANHO_PLAYER)

        self.image = self.image_still
        self.rect = self.image.get_rect(topleft=(x,y))
        #variaveis que determinam a "fisica do personagem" eixos x e y
        self.__vel_y = 0
        self.__gravity = 1
        self.__jump_force = -15
        self.__is_jumping = False
        self.__ground_level = 550  #chao

    def update(self):
        self.handle_input()
        self.apply_gravity()
        if self.invulnerable_timer > 0:
            self.invulnerable_timer =- 1 #decresce o tempo de ivulnerabilidade

    def handle_input(self):
        keys = pygame.key.get_pressed()
        is_moving = False

        #movimentacao lateral (eixos x)
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.__speed
            self.image = self.image_left
            is_moving = True

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.__speed
            self.image = self.image_right
            is_moving = True

        # pulo do jogador, se ja n tiver
        if keys[pygame.K_UP] and not self.__is_jumping:
            self.__vel_y = self.__jump_force
            self.__is_jumping = True

        if self.__is_jumping:
            self.image = self.image_jump  # Se está no ar, mostra imagem de pulo
        elif not is_moving:
            self.image = self.image_still  # Se não está no ar e soltou os botões de andar, fica parado

    def apply_gravity(self):
        #"gravidade" incrementando o eixo vertical
        self.__vel_y += self.__gravity
        self.rect.y += self.__vel_y

        #checa colisao com o chao
        if self.rect.bottom >= self.__ground_level:
            self.rect.bottom = self.__ground_level
            self.__vel_y = 0
            self.__is_jumping = False  #tocou o chao, pode pular novamente

    def take_damage(self):
        if self.invulnerable_timer == 0:
            self.lives -= 1
            self.invulnerable_timer = 60 # fica ivulneravel por 60 frames (1 segundo)
            return True
        return False
