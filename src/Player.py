import pygame
from src.Entity import Entity
from src.Const import GUARDIAN_FORWARD, GUARDIAN_BACK, GUARDIAN_STILL, GUARDIAN_JUMP, TAMANHO_PLAYER, GUARDIAN_RIGHT_ATTACK, FOOTSTEPS_SOUND, GUARDIAN_ATTACK_SOUND, GUARDIAN_DAMANGE_SOUND

class Player(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 40, 60, (0, 0, 0))
        self.__speed = 5
        self.lives = 3
        self.invulnerable_timer = 0 #tempo de invencibilidade dps de tomar um hit
        self.attack_timer = 0
        self.footsteps_timer = 0
        self.is_attacking = False
        self.seeds_collected = 0

        #sounds
        self.footsteps_sound = pygame.mixer.Sound(FOOTSTEPS_SOUND)
        self.footsteps_sound.set_volume(0.3)

        self.hit_sound = pygame.mixer.Sound(GUARDIAN_ATTACK_SOUND)
        self.hit_sound.set_volume(0.5)

        self.damage_sound = pygame.mixer.Sound(GUARDIAN_DAMANGE_SOUND)
        self.damage_sound.set_volume(0.4)

        img_right = pygame.image.load(GUARDIAN_FORWARD).convert_alpha()
        self.image_right = pygame.transform.scale(img_right, TAMANHO_PLAYER)

        img_left = pygame.image.load(GUARDIAN_BACK).convert_alpha()
        self.image_left = pygame.transform.scale(img_left, TAMANHO_PLAYER)

        img_still = pygame.image.load(GUARDIAN_STILL).convert_alpha()
        self.image_still = pygame.transform.scale(img_still, TAMANHO_PLAYER)

        img_attack = pygame.image.load(GUARDIAN_RIGHT_ATTACK).convert_alpha()
        self.image_attack = pygame.transform.scale(img_attack, TAMANHO_PLAYER)

        img_jump = pygame.image.load(GUARDIAN_JUMP).convert_alpha()
        self.image_jump = pygame.transform.scale(img_jump, TAMANHO_PLAYER)

        self.image = self.image_still
        self.rect = self.image.get_rect(topleft=(x,y))
        #variaveis que determinam a "fisica do personagem" eixos x e y
        self.__vel_y = 0
        self.__gravity = 1
        self.__jump_force = -17
        self.__is_jumping = False
        self.__ground_level = 550  #chao
        self.hitbox = pygame.Rect(0, 0, 32, 50)  # Largura 32, Altura 50
        self.hitbox.center = self.rect.center

    def update(self):
        self.handle_input()
        self.apply_gravity()
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1 #decresce o tempo de ivulnerabilidade
        self.hitbox.center = self.rect.center

    def handle_input(self):
        keys = pygame.key.get_pressed()
        is_moving = False

        # 1. Movimentação (Define a base)
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.__speed
            self.image = self.image_left
            is_moving = True
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.__speed
            self.image = self.image_right
            is_moving = True
        else:
            self.image = self.image_still  # Estado padrão se nada acontece

        # 2. Pulo (Sobrescreve a imagem de movimento/still)
        if keys[pygame.K_UP] and not self.__is_jumping:
            self.__vel_y = self.__jump_force
            self.__is_jumping = True

        if self.__is_jumping:
            self.image = self.image_jump

        # 3. Ataque (Tem prioridade máxima - sobrescreve Pulo, Movimento ou Still)
        if keys[pygame.K_q] and self.attack_timer == 0:
            self.is_attacking = True
            self.attack_timer = 12
            self.hit_sound.play()

        if self.attack_timer > 0:
            self.attack_timer -= 1
            self.image = self.image_attack
            self.is_attacking = True  # Garante que o estado está ativo
        else:
            self.is_attacking = False

        if is_moving and not self.is_attacking and not self.__is_jumping:
            if self.footsteps_timer <= 0:
                self.footsteps_sound.play()
                self.footsteps_timer = 20
        else:
            # Se o jogador parou de andar, pulou ou atacou, para o som imediatamente
            self.footsteps_sound.stop()

        if self.footsteps_timer > 0:
            self.footsteps_timer -= 1


    def apply_gravity(self):
        #"gravidade" incrementando o eixo vertical
        self.__vel_y += self.__gravity
        self.rect.y += self.__vel_y

        #checa colisao com o chao
        if self.rect.bottom >= self.__ground_level:
            self.rect.bottom = (
                self.__ground_level)
            self.__vel_y = 0
            self.__is_jumping = False  #tocou o chao, pode pular novamente

    def take_damage(self):
        self.damage_sound.play()
        if self.invulnerable_timer == 0:
            self.lives -= 1
            self.invulnerable_timer = 120 # fica ivulneravel por 120 frames (2 segundos)
            return True
        self.damage_sound.stop()
        return False

    def start_attack(self):
        # Só dispara se não estiver atacando e não estiver pulando (opcional)
        if self.attack_timer == 0 and not self.__is_jumping:
            self.is_attacking = True
            self.attack_timer = 12
            self.hit_sound.play()
