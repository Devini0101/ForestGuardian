import pygame
import random
from src.Player import Player
from src.Enemy import Enemy
from src.Const import WIN_WIDTH, WIN_HEIGHT, MAIN_BG

class Level:
    def __init__(self, window):
        self.window = window

        self.bg_image = pygame.image.load(MAIN_BG).convert()
        # Escala a imagem
        self.bg_image = pygame.transform.scale(self.bg_image, (WIN_WIDTH, WIN_HEIGHT))
        self.bg_x = 0 #pos inicial horizontal

        # Sprites
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Jogador
        self.player = Player(x=100, y=100)
        self.all_sprites.add(self.player)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        # Evento customizado para spawnar inimigos a cada 1.5s
        SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_ENEMY_EVENT, 1500)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Checa se está no tempo de criar um inimigo
                if event.type == SPAWN_ENEMY_EVENT:
                    ghost = Enemy(x=WIN_WIDTH, y=220, speed=random.randint(4, 8))
                    self.all_sprites.add(ghost)
                    self.enemies.add(ghost)

            if self.player.rect.x > WIN_WIDTH / 2:  #se o jogador passar do meio da tela
                diff = self.player.rect.x - (WIN_WIDTH / 2)
                self.player.rect.x = WIN_WIDTH / 2  #trava o player no meio
                self.bg_x -= diff  #move o fundo pra esquerda

                #move os inimigos na direcao contraria pro sincronismo
                for enemy in self.enemies:
                    enemy.rect.x -= diff

            #desenha o segundo fundo
            self.window.blit(self.bg_image, (self.bg_x, 0))
            self.window.blit(self.bg_image, (self.bg_x + WIN_WIDTH, 0))

            #resetar o fundo se ele sair da tela
            if self.bg_x <= -WIN_WIDTH:
                self.bg_x = 0

            #att os sprites
            self.all_sprites.update()

            hitted = pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask)
            if hitted:
                running = False
            # 2. Desenha os sprites por cima do fundo
            self.all_sprites.draw(self.window)

            pygame.display.flip()
            clock.tick(60)