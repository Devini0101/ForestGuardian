import pygame
import random
from src.Player import Player
from src.Enemy import Enemy
from src.Const import WIN_WIDTH, WIN_HEIGHT, MAIN_BG, GUARDIAN_SPECIAL_ATTACK, GUARDIAN_SPECIAL_ATTACK_SOUND, SEED_IMG
from src.Seed import Seed

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
        self.seeds = pygame.sprite.Group()

        # Jogador
        self.player = Player(x=100, y=100)
        self.all_sprites.add(self.player)

        thunder_img = pygame.image.load(GUARDIAN_SPECIAL_ATTACK).convert_alpha()
        self.thunder_image = pygame.transform.scale(thunder_img, (700, 850))

        self.thunder_sound = pygame.mixer.Sound(GUARDIAN_SPECIAL_ATTACK_SOUND)
        self.thunder_sound.set_volume(0.3)

        self.special_attack_active = False
        self.special_attack_end_time = 0

        # --- NOVA PARTE: CONFIGURAÇÃO DO HUD/INTERFACE ---
        pygame.font.init()  # Garante que o sistema de fontes iniciou
        self.hud_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.alert_font = pygame.font.SysFont("Arial", 28, bold=True)
        seed_raw = pygame.image.load(SEED_IMG).convert_alpha() #small seed for the HUD
        self.hud_seed_image = pygame.transform.scale(seed_raw, (90, 90))

    def run(self):
        clock = pygame.time.Clock()
        running = True

        # Evento customizado para spawnar inimigos a cada 3s
        SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_ENEMY_EVENT, 3000)

        while running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                #QUIT event on X
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                #checks if its time to create a enemy from the interval
                if event.type == SPAWN_ENEMY_EVENT and not self.special_attack_active:
                    ghost = Enemy(x=WIN_WIDTH, y=220, speed=random.randint(2, 4), player=self.player)
                    self.all_sprites.add(ghost)
                    self.enemies.add(ghost)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.player.start_attack()

                    if event.key == pygame.K_e:
                        if self.player.seeds_collected >= 10 and not self.special_attack_active:
                            self.special_attack_active = True
                            self.special_attack_end_time = current_time + 1500 #ends in 1.5 seconds
                            self.thunder_sound.play()
                            if hasattr(self.player, 'image_still'):
                                self.player.image = self.player.image_still
                            print(f'!!!Ataque especial ativado')

            if self.special_attack_active:
                if current_time >= self.special_attack_end_time:
                    self.thunder_sound.stop()
                    self.special_attack_active = False
                    for enemy in list(self.enemies):
                        enemy.hit()  # Como eles têm 1 de vida, isso vai matá-los e chamará kill()
                        print("O Raio caiu! Todos os fantasmas foram eliminados.")
            else:
                if self.player.rect.x > WIN_WIDTH / 2:  #se o jogador passar do meio da tela
                    diff = self.player.rect.x - (WIN_WIDTH / 2)
                    self.player.rect.x = WIN_WIDTH / 2  #trava o player no meio
                    self.bg_x -= diff  #move o fundo pra esquerda

                    #move os inimigos na direcao contraria pro sincronismo
                    for enemy in self.enemies:
                        enemy.rect.x -= diff
                        enemy.hitbox.center = enemy.rect.center

                    for seed in self.seeds:
                        seed.rect.x -= diff

                # att os sprites (animações e posicoes)
                self.all_sprites.update()
                for seed in list(self.seeds):
                    # Só coleta se a semente já caiu no chão E encostou no hitbox do jogador
                    if seed.can_collect and self.player.hitbox.colliderect(seed.rect):
                        seed.kill()  # Remove a semente de todos os grupos automaticamente
                        self.player.seeds_collected += 1
                        print(f"Sementes: {self.player.seeds_collected}/10")

                for enemy in self.enemies:
                    pygame.draw.rect(self.window, (0, 255, 0), enemy.hitbox, 2)
                    if self.player.hitbox.colliderect(enemy.hitbox):
                        if self.player.is_attacking:
                            enemy.hit()  # Fantasma leva dano
                            # Knockback (empurrão) baseado no hitbox
                            if enemy.lives <= 0:
                                if random.random() < 0.25:  # 0.25 = 25%
                                    new_seed = Seed(enemy.rect.centerx, enemy.rect.centery)
                                    self.seeds.add(new_seed)
                                    self.all_sprites.add(new_seed)

                            if self.player.rect.x < enemy.rect.x:
                                enemy.rect.x += 40
                            else:
                                enemy.rect.x -= 40
                            enemy.hitbox.center = enemy.rect.center
                            print(f"Fantasma atingido! Vidas dele: {enemy.lives}")

                        else:
                            # Se o player não estava atacando, ele toma dano
                            if self.player.take_damage():
                                print(f"Player atingido! Vidas restantes: {self.player.lives}")
                                if self.player.lives <= 0:
                                    running = False  # Game Over

            self.window.blit(self.bg_image, (self.bg_x, 0))
            self.window.blit(self.bg_image, (self.bg_x + WIN_WIDTH, 0))

            if self.bg_x <= -WIN_WIDTH:
                self.bg_x = 0

            #draw all sprites again hover the bg
            self.all_sprites.draw(self.window)

            #desenha o especial
            if self.special_attack_active:
                for enemy in self.enemies:
                    thunder_rect = self.thunder_image.get_rect()
                    # OPÇÃO A: Alinha a base do raio com o centro do fantasma (Efeito clássico)
                    thunder_rect.centerx = enemy.rect.centerx
                    margem_para_subir = 100
                    thunder_rect.centery = enemy.rect.centery - margem_para_subir

                    # OPÇÃO B: Se o raio for muito alto e precisar vir OBRIGATORIAMENTE do topo da tela (y=0):
                    # thunder_rect.centerx = enemy.rect.centerx
                    # thunder_rect.top = 0

                    # Desenha a imagem do raio na tela usando a posição calculada
                    self.window.blit(self.thunder_image, thunder_rect)

            self.draw_hud()
            pygame.display.flip()
            clock.tick(60)

    def draw_hud(self):
        counter_text = f'Sementes Místicas Coletadas ({self.player.seeds_collected})'
        surf_text = self.hud_font.render(counter_text, True, (255, 255, 255))

        margin_right = 20
        margin_bottom = 25

        pos_texto_x = WIN_WIDTH - surf_text.get_width() - margin_right
        pos_texto_y = WIN_HEIGHT - surf_text.get_height() - margin_bottom

        # Posiciona a imagem da semente logo à esquerda do texto (com 8px de espaço)
        pos_semente_x = pos_texto_x - self.hud_seed_image.get_width() - 4
        # Centraliza verticalmente a sementinha com a linha do texto
        pos_semente_y = pos_texto_y + (surf_text.get_height() - self.hud_seed_image.get_height()) // 2

        self.window.blit(self.hud_seed_image, (pos_semente_x, pos_semente_y))
        self.window.blit(surf_text, (pos_texto_x, pos_texto_y))

        if self.player.seeds_collected >= 10 and not self.special_attack_active:
            text_alert = "HABILIDADE HABILITADA [E]"
            surf_alert = self.alert_font.render(text_alert, True, (0, 255, 128))
            # Centraliza no eixo X, e coloca um pouco acima da borda inferior
            pos_alerta_x = (WIN_WIDTH - surf_alert.get_width()) // 2
            pos_alerta_y = WIN_HEIGHT - surf_alert.get_height() - 30

            # Dá um efeito de "piscar" de leve usando o tempo do jogo (opcional, mas fica bem profissional!)
            if (pygame.time.get_ticks() // 250) % 2 == 0:
                self.window.blit(surf_alert, (pos_alerta_x, pos_alerta_y))