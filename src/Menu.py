#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from src.Const import WIN_HEIGHT, WIN_WIDTH, C_ORANGE, MENU_OPTION, C_WHITE, C_YELLOW, MENU_BG_PATH, MENU_BG_SOUND_PATH, COMMANDS

class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load(MENU_BG_PATH).convert_alpha()
        self.rect = self.surf.get_rect() #as default on top = 0 and left = 0
        pygame.font.init()
        self.cmd_title_font = pygame.font.SysFont("Lucida Sans Typewriter", 24, bold=True)
        self.cmd_text_font = pygame.font.SysFont("Lucida Sans Typewriter", 18)

    def run(self):
        menu_option = 0
        pygame.mixer_music.load(MENU_BG_SOUND_PATH)
        pygame.mixer_music.play(-1)

        while True:
            # DRAW IMAGES
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(70, "Forest", C_ORANGE, ((WIN_WIDTH / 2), 150))
            self.menu_text(70, "Guardian", C_ORANGE, ((WIN_WIDTH / 2), 220))

            margin_left = 40
            line_y = 350
            space_bwt_lines = 30

            title_surf = self.cmd_title_font.render("LISTA DE COMANDOS:", True, C_ORANGE)
            self.window.blit(title_surf, (margin_left, line_y))

            line_y += space_bwt_lines + 10  # Dá um espaço extra após o título

            for command in COMMANDS:
                cmd_surf = self.cmd_text_font.render(command, True, C_WHITE)
                self.window.blit(cmd_surf, (margin_left, line_y))
                line_y += space_bwt_lines

            for i in range(len(MENU_OPTION)):
                y_pos = 350 + 50 * i  # 350 é o início, 50 é o espaçamento entre opções
                if i == menu_option:
                    self.menu_text(40, MENU_OPTION[i], C_YELLOW, ((WIN_WIDTH / 2), y_pos))
                else:
                    self.menu_text(40, MENU_OPTION[i], C_WHITE, ((WIN_WIDTH / 2), y_pos))
            pygame.display.flip()

            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close Window
                    quit()  # end pygame
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:  # DOWN KEY
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP:  # UP KEY
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN:  # ENTER
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
