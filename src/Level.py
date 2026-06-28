import pygame
import random
from src.Player import Player
from src.Enemy import Enemy
from src.Boss import Boss
from src.Const import WIN_WIDTH, WIN_HEIGHT, MAIN_BG, GUARDIAN_SPECIAL_ATTACK, GUARDIAN_SPECIAL_ATTACK_SOUND, SEED_IMG, TRIBE_LEADER_THEME, TROPHY, GAME_OVER, TRIBE_LEADER_DEFEATED, GUARDIAN_DEFEATED, TAMANHO_TRIBE_LEADER, TAMANHO_PLAYER, HEART_IMAGE
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
        self.boss_group = pygame.sprite.GroupSingle()

        # Jogador
        self.player = Player(x=100, y=100)
        self.all_sprites.add(self.player)

        thunder_img = pygame.image.load(GUARDIAN_SPECIAL_ATTACK).convert_alpha()
        self.thunder_image = pygame.transform.scale(thunder_img, (700, 850))

        self.thunder_sound = pygame.mixer.Sound(GUARDIAN_SPECIAL_ATTACK_SOUND)
        self.thunder_sound.set_volume(0.3)

        self.special_attack_active = False
        self.special_attack_end_time = 0

        #BOSS
        self.ghosts_killed = 0
        self.boss_spawned = False

        # personagens no estado de derrota
        self.img_player_defeated = pygame.image.load(GUARDIAN_DEFEATED).convert_alpha()
        self.img_player_defeated = pygame.transform.scale(self.img_player_defeated, (int(TAMANHO_PLAYER[0] * 1.5), int(TAMANHO_PLAYER[1] * 1.5)))
        self.img_boss_defeated = pygame.image.load(TRIBE_LEADER_DEFEATED).convert_alpha()
        self.img_boss_defeated = pygame.transform.scale(self.img_boss_defeated, (int(TAMANHO_TRIBE_LEADER[0] * 1.5), int(TAMANHO_TRIBE_LEADER[1] * 1.5)))

        #CONFIGURAÇÃO DO HUD
        pygame.font.init()  # Garante que o sistema de fontes iniciou
        self.hud_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.alert_font = pygame.font.SysFont("Arial", 28, bold=True)
        seed_raw = pygame.image.load(SEED_IMG).convert_alpha() #small seed for the HUD
        self.hud_seed_image = pygame.transform.scale(seed_raw, (90, 90))
        heart_raw = pygame.image.load(HEART_IMAGE).convert_alpha()
        self.hud_heart_image = pygame.transform.scale(heart_raw, (100, 100))

        # Troféu da vitória e título de Game Over gráficos
        self.img_trophy = pygame.image.load(TROPHY).convert_alpha()
        self.img_trophy = pygame.transform.scale(self.img_trophy, (650, 580))
        self.img_game_over_title = pygame.image.load(GAME_OVER).convert_alpha()
        self.img_game_over_title = pygame.transform.scale(self.img_game_over_title, (500, 320))  # Título destacado

        self.game_over = False
        self.game_won = False
        self.end_timer = 0

        self.end_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.sub_font = pygame.font.SysFont("Arial", 24, bold=False)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        # Evento customizado para spawnar inimigos a cada 3s
        SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_ENEMY_EVENT, 2800)

        while running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                #QUIT event on X
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                #checks if its time to create a enemy from the interval
                if event.type == SPAWN_ENEMY_EVENT and not self.special_attack_active and not self.boss_spawned:
                    ghost = Enemy(x=WIN_WIDTH, y=220, speed=random.randint(2, 5), player=self.player)
                    self.all_sprites.add(ghost)
                    self.enemies.add(ghost)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.player.start_attack()

                    if event.key == pygame.K_e:
                        if self.player.seeds_collected >= 10 and not self.special_attack_active:
                            self.player.seeds_collected -= 10 #decresce as se
                            self.special_attack_active = True
                            self.special_attack_end_time = current_time + 1500 #ends in 1.5 seconds
                            self.thunder_sound.play()
                            if hasattr(self.player, 'image_still'):
                                self.player.image = self.player.image_still
                            print(f'!!!Ataque especial ativado')

            #so pode enfrentar o boss, depois de passar por 20 fantasmas e coletar o suficiente para o ataque especial
            if self.ghosts_killed >= 20 and not self.boss_spawned and self.player.seeds_collected >= 10 :
                self.boss_spawned = True
                for enemy in self.enemies:
                    enemy.kill()
                for seed in self.seeds:
                    seed.kill()

                pygame.mixer.music.stop()
                pygame.mixer.music.load(TRIBE_LEADER_THEME)
                pygame.mixer.music.play(-1) #Musica em loop

                the_boss = Boss(x=WIN_WIDTH + 150, y=550, player=self.player)
                self.boss_group.add(the_boss)
                self.all_sprites.add(the_boss)

                print("O CHEFE DA FLORESTA APARECEU!")

            if self.special_attack_active:
                if current_time >= self.special_attack_end_time:
                    self.thunder_sound.stop()
                    self.special_attack_active = False

                    if self.boss_spawned and self.boss_group.sprite:
                        boss =self.boss_group.sprite
                        for i in range(3) :
                            boss.hit()
                        if boss.lives <=0 and not self.game_over:
                            self.game_over = True
                            self.game_won = True
                            self.end_timer = current_time + 4000
                            print("PARABÉNS, VOCE DERROTOU O CHEFE DA TRIBO")
                    else:
                        for enemy in list(self.enemies):
                            enemy.hit()
                            self.ghosts_killed += 1
                            print("O Raio caiu! Todos os fantasmas foram eliminados.")
            else:

                if not self.boss_spawned:
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
                if not self.game_over:
                    self.all_sprites.update()

                for seed in list(self.seeds):
                    # Só coleta se a semente já caiu no chão E encostou no hitbox do jogador
                    if seed.can_collect and self.player.hitbox.colliderect(seed.rect):
                        seed.kill()  # Remove a semente de todos os grupos automaticamente
                        self.player.seeds_collected += 1
                        print(f"Sementes: {self.player.seeds_collected}/10")

                if not self.boss_spawned:
                    for enemy in self.enemies:
                        pygame.draw.rect(self.window, (0, 255, 0), enemy.hitbox, 2)
                        if self.player.hitbox.colliderect(enemy.hitbox):
                            if self.player.is_attacking:
                                enemy.hit()  # Fantasma leva dano
                                # Knockback (empurrão) baseado no hitbox
                                if enemy.lives <= 0:
                                    self.ghosts_killed += 1
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
                                    if self.player.lives <= 0 and not self.game_over:
                                        self.game_over = True
                                        self.game_won = False
                                        self.end_timer = current_time + 4000
                else:
                    if self.boss_group.sprite:
                        boss = self.boss_group.sprite
                        pygame.draw.rect(self.window, (255, 0, 0), boss.hitbox, 2)
                        # O Boss.py gerencia o dano DELE no player. Aqui checamos o dano do PLAYER no Boss:
                        if self.player.hitbox.colliderect(boss.hitbox):
                            if self.player.is_attacking:
                                # Se o jogador apertou Q ou E, o Boss leva dano e o jogador causa recuo
                                boss.hit()
                                if self.player.rect.x < boss.hitbox.x:
                                    self.player.rect.x -= 60
                                else:
                                    self.player.rect.x += 60

                                if boss.lives <= 0 and not self.game_over:
                                    print("VOCÊ VENCEU A DEMO!")
                                    self.game_over = True
                                    self.game_won = True
                                    self.end_timer = current_time + 4000
                                    print("PARABÉNS, VOCE DERROTOU O CHEFE DA TRIBO")
                            else:
                                boss.execute_attack()
                                if self.player.lives <= 0:
                                    print("Player atingido pelo Boss! Game Over.")
                                    self.game_over = True
                                    self.game_won = False
                                    self.end_timer = current_time + 4000

            self.window.blit(self.bg_image, (self.bg_x, 0))
            self.window.blit(self.bg_image, (self.bg_x + WIN_WIDTH, 0))
            if self.bg_x <= -WIN_WIDTH: self.bg_x = 0

            #draw all sprites again hover the bg
            self.all_sprites.draw(self.window)

            #desenha o especial
            if self.special_attack_active:
                if self.boss_spawned and self.boss_group.sprite:
                    # Desenha o raio gigante em cima do Boss
                    boss = self.boss_group.sprite
                    thunder_rect = self.thunder_image.get_rect()
                    thunder_rect.centerx = boss.rect.centerx
                    thunder_rect.centery = boss.rect.centery - 100
                    self.window.blit(self.thunder_image, thunder_rect)
                else:
                    for enemy in self.enemies:
                        thunder_rect = self.thunder_image.get_rect()

                        thunder_rect.centerx = enemy.rect.centerx
                        margem_para_subir = 100
                        thunder_rect.centery = enemy.rect.centery - margem_para_subir
                        # OPÇÃO B: Se o raio for muito alto e precisar vir OBRIGATORIAMENTE do topo da tela (y=0):
                        # thunder_rect.centerx = enemy.rect.centerx
                        # thunder_rect.top = 0
                        self.window.blit(self.thunder_image, thunder_rect)

            self.draw_hud()
            if self.game_over:
                if self.game_won:
                    self.draw_win_screen()
                else:
                    self.draw_game_over_screen()
                #verifica tempo de espera pra fechar a fase
                if current_time >= self.end_timer:
                    running = False
            pygame.display.flip()
            clock.tick(60)

    def draw_hud(self):
        counter_text = f'Sementes Místicas Coletadas ({self.player.seeds_collected})'
        surf_text = self.hud_font.render(counter_text, True, (255, 255, 255))

        margin_right = 20
        margin_left = 20
        margin_bottom = 25

        heart_w = self.hud_heart_image.get_width()
        heart_h = self.hud_heart_image.get_height()

        pos_texto_x = WIN_WIDTH - surf_text.get_width() - margin_right
        pos_texto_y = WIN_HEIGHT - surf_text.get_height() - margin_bottom

        pos_heart_y = pos_texto_y + (surf_text.get_height() - heart_h) // 2
        for i in range(self.player.lives):
            pos_heart_x = margin_left + ( i * 30)
            self.window.blit(self.hud_heart_image, (pos_heart_x, pos_heart_y))

        # Posiciona a imagem da semente logo à esquerda do texto (com 8px de espaço)
        pos_semente_x = pos_texto_x - self.hud_seed_image.get_width()
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

    def draw_win_screen(self):
        """Desenha a tela opaca de vitória com texto dourado"""
        # 1. Máscara escura semitransparente
        overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.window.blit(overlay, (0, 0))

        trophy_rect = self.img_trophy.get_rect(center=(WIN_WIDTH / 2, 130))
        self.window.blit(self.img_trophy, trophy_rect)

        # 3. Título de Vitória (Dourado) logo abaixo do troféu
        text_str = "PARABÉNS, VOCÊ DERROTOU O CHEFE DA TRIBO"
        text_surf = self.end_font.render(text_str, True, (255, 215, 0))
        text_rect = text_surf.get_rect(center=(WIN_WIDTH / 2, 260))
        self.window.blit(text_surf, text_rect)

        # 4. Desenha o Boss Caído no chão (Y=550 para combinar com o nível do combate)
        boss_def_rect = self.img_boss_defeated.get_rect(midbottom=(WIN_WIDTH / 2, 620))
        self.window.blit(self.img_boss_defeated, boss_def_rect)

        # 5. Subtítulo na parte inferior da tela
        sub_str = "RETORNANDO AO MENU... [Aguarde]"
        sub_surf = self.sub_font.render(sub_str, True, (200, 200, 200))
        sub_rect = sub_surf.get_rect(center=(WIN_WIDTH / 2, 490))
        self.window.blit(sub_surf, sub_rect)

    def draw_game_over_screen(self):
        # 1. Máscara escura semitransparente de fundo
        overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        overlay.set_alpha(195)
        overlay.fill((0, 0, 0))
        self.window.blit(overlay, (0, 0))

        # 2. Desenha o PNG gráfico de Game Over na parte superior central
        go_title_rect = self.img_game_over_title.get_rect(center=(WIN_WIDTH / 2, 130))
        self.window.blit(self.img_game_over_title, go_title_rect)

        if self.boss_spawned:
            text_str = "VOCÊ FOI DERROTADO PELO CHEFE DA TRIBO, TENTE NOVAMENTE"
        else:
            text_str = "VOCÊ FOI DERROTADO, TENTE NOVAMENTE"
        text_surf = self.end_font.render(text_str, True, (255, 50, 50))
        text_rect = text_surf.get_rect(center=(WIN_WIDTH / 2, 260))
        self.window.blit(text_surf, text_rect)

        # 4. Desenha o seu Personagem Caído/Derrotado no chão (Y=550)
        player_def_rect = self.img_player_defeated.get_rect(midbottom=(WIN_WIDTH / 2, 620))
        self.window.blit(self.img_player_defeated, player_def_rect)

        # 5. Subtítulo na parte inferior da tela
        sub_str = "RETORNANDO AO MENU... [Aguarde]"
        sub_surf = self.sub_font.render(sub_str, True, (200, 200, 200))
        sub_rect = sub_surf.get_rect(center=(WIN_WIDTH / 2, 490))
        self.window.blit(sub_surf, sub_rect)