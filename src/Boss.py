import pygame
from src.Const import WIN_WIDTH, TRIBE_LEADER_ATTACK, TRIBE_LEADER_LEFT, TRIBE_LEADER_RIGHT, TRIBE_LEADER_STILL, \
    TAMANHO_TRIBE_LEADER, TAMANHO_TRIBE_LEADER_BIGGER, TRIBE_LEADER_FOOTSTEPS, TRIBE_LEADER_ATTACK_SOUND

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.player = player
        self.__ground_level = 550
        self.lives = 6

        #boss imgs
        self.img_left = pygame.image.load(TRIBE_LEADER_LEFT).convert_alpha()
        self.img_right = pygame.image.load(TRIBE_LEADER_RIGHT).convert_alpha()
        self.img_still = pygame.image.load(TRIBE_LEADER_STILL).convert_alpha()
        self.img_attack = pygame.image.load(TRIBE_LEADER_ATTACK).convert_alpha()

        self.img_left = pygame.transform.scale(self.img_left, TAMANHO_TRIBE_LEADER)
        self.img_right = pygame.transform.scale(self.img_right, TAMANHO_TRIBE_LEADER)
        self.img_still = pygame.transform.scale(self.img_still, TAMANHO_TRIBE_LEADER)
        self.img_attack = pygame.transform.scale(self.img_attack, TAMANHO_TRIBE_LEADER_BIGGER)

        self.image = self.img_left

        #sounds fx
        self.attack_sound = pygame.mixer.Sound(TRIBE_LEADER_ATTACK_SOUND)
        self.attack_sound.set_volume(0.5)
        self.footsteps_sound = pygame.mixer.Sound(TRIBE_LEADER_FOOTSTEPS)
        self.footsteps_sound.set_volume(0.4)
        self.footsteps_timer = 0

        self.rect = self.image.get_rect(midbottom=(x, self.__ground_level))

        #hitbox padrao do boss
        self.hitbox = pygame.Rect(0, 0, 80, 120)
        self.hitbox.center = self.rect.center

        self.speed = 2
        self.attack_cooldown = 200
        self.last_attack_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        #distância entre o chefe e o player no eixo x
        distancia_x = self.player.rect.x - self.rect.x

        is_moving = False  #flag para controle de estados

        #controle de estados
        if current_time - self.last_attack_time < 400:
            self.image = self.img_attack
        else:
            if abs(distancia_x) > self.speed:
                if self.rect.x < self.player.rect.x:
                    self.rect.x += self.speed
                    self.image = self.img_right
                elif self.rect.x > self.player.rect.x:
                    self.rect.x -= self.speed
                    self.image = self.img_left
            else:
                self.image = self.img_still

        if is_moving:
            if self.footsteps_timer <=0:
                self.footsteps_sound.play()
                self.footsteps_timer = 30
        else:
            self.footsteps_sound.stop()

        if self.footsteps_timer > 0:
            self.footsteps_timer -= 1

        #reatualiza a imgem para nao afundar no chao
        self.rect = self.image.get_rect(midbottom=(self.rect.centerx, self.__ground_level))

        if self.image == self.img_attack:
            offset_y = 20 #deslocamento pes do boss
            self.rect = self.image.get_rect(midbottom=(self.rect.centerx, self.__ground_level + offset_y))
        else:
            self.rect = self.image.get_rect(midbottom=(self.rect.centerx, self.__ground_level))

        #hitbox segue o centro da imagem
        self.hitbox.center = self.rect.center

    def execute_attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = current_time
            self.image = self.img_attack
            self.attack_sound.play()

            #atualiza o frame para que fique exatamente no mesmo eixo
            self.rect = self.image.get_rect(midbottom=(self.rect.centerx, self.__ground_level))

            # Usa o sistema de dano do Player
            if self.player.take_damage():
                self.player.lives -= 1
                print(f"O Boss te acertou,vidas restantes: {self.player.lives}")

    def hit(self):
        self.lives -= 1
        print(f"Boss levou dano, vidas restantes: {self.lives}")
        if self.lives <= 0:
            self.kill()