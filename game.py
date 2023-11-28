import pygame
import numpy as np
import time
SIZE = 6

table = np.zeros((SIZE, SIZE))
# print(table)


class Square(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, index):
        super().__init__()
        self.image = pygame.image.load(r"Files\square.png").convert()
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.empty = True
        self.index = index
        self.click_sound = pygame.mixer.Sound(r"Files\click_sound.wav")

    def update(self, events, mouse_pos, symbol):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos) and symbol == 'o' and self.empty:
                self.image = pygame.image.load(r"Files\circle.png").convert()
                self.empty = False
                self.click_sound.play()

            elif event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos) and symbol == 'x' and self.empty:
                self.image = pygame.image.load(r"Files\cross.png").convert()
                self.empty = False
                self.click_sound.play()


pygame.init()


screen = pygame.display.set_mode((SIZE * 100, SIZE * 100))
pygame.display.set_caption('Chaos and Order')
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 20)
menu_music = pygame.mixer.Sound(r"Files/menu_music.wav")

title_surface = font.render('Chaos and Order', True, "Red", "black")
title_rect = title_surface.get_rect(center=(SIZE * 50, 50))

order_rect = pygame.Rect((0, 400), (SIZE * 50, 200))
chaos_rect = pygame.Rect((SIZE * 50, 400), (SIZE * 50, 200))

rules_text = ["The player Order strives to create a", 
              "five-in-a-row of either Xs or Os.",
              "The opponent Chaos endeavors to prevent this.",
              "Press space to change symbol",
              "Who you wanna play as?"]


menu_music.set_volume(0.5)
menu_music.play()

square = pygame.sprite.Group()


def display_text(text_list, font, x_pos, y_pos):
    for text in text_list:
        text_surface = font.render(text, False, "Red", "black")
        text_rect = text_surface.get_rect(center=(x_pos, y_pos))
        screen.blit(text_surface, text_rect)
        y_pos += 30


def create_table():
    pos_y = 0
    pos_x = 0
    index = 0

    for row in table:
        pos_x = 0
        for rect in row:
            square.add(Square(pos_x, pos_y, index))
            pos_x += 100
            index += 1
        pos_y += 100


def switch_symbol():
    global symbol
    if symbol == 'o':
        symbol = 'x'
    else:
        symbol = 'o'


running = True
game_active = False
symbol = 'o'
player = ''

create_table()

while running:
    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                switch_symbol()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if chaos_rect.collidepoint(mouse_pos):
                    player = "chaos"
                    print(player)
                elif order_rect.collidepoint(mouse_pos):
                    player = "order"
                    print(player)
                square.empty()
                create_table()
                game_active = True
                events.clear()

    if game_active:
        square.draw(screen)
        square.update(events, mouse_pos, symbol)

    else:
        screen.blit(title_surface, title_rect)
        display_text(rules_text, font, SIZE * 50, 200)
        pygame.draw.rect(screen, "BLUE", order_rect)
        pygame.draw.rect(screen, "RED", chaos_rect)


    pygame.display.update()
    clock.tick(60)

pygame.quit()

#  add logic, 
