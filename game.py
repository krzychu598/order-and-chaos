from typing import Any
import pygame
import numpy as np

SIZE = 6

table = np.zeros((SIZE, SIZE))
print(table)





class Square(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(r"Chaos_and_Order\basic_shapes\square.png").convert()
        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))
        self.empty = True

    def clicked(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.MOUSEBUTTONDOWN]:
            self.image = pygame.image.load(r"Chaos_and_Order\basic_shapes\circle.png").convert()
            print("clicked")


    def update(self, events, mouse_pos, symbol):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos) and symbol == 'o' and self.empty:
                self.image = pygame.image.load(r"Chaos_and_Order\basic_shapes\circle.png").convert()
                self.empty = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos) and symbol == 'x' and self.empty:
                self.image = pygame.image.load(r"Chaos_and_Order\basic_shapes\cross.png").convert()
                self.empty = False




pygame.init()

screen = pygame.display.set_mode((SIZE * 100, SIZE * 100))
pygame.display.set_caption('Chaos and Order')


square = pygame.sprite.Group()

pos_y = 0
pos_x = 0

for row in table:
    pos_x = 0
    for rect in row:
        square.add(Square(pos_x, pos_y))
        pos_x += 100
    pos_y += 100




clock = pygame.time.Clock()


running = True

symbol = 'x'

def switch_symbol():
    global symbol
    if symbol == 'o':
        symbol = 'x'
    else:
        symbol = 'o'


while running:
    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            switch_symbol()

            
    square.draw(screen)
    square.update(events, mouse_pos, symbol)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

# add main menu explaining rules, add logic, add changing symbol