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





pygame.init()

screen = pygame.display.set_mode((800, 800))
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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
    square.draw(screen)
    # screen.blit(table_surface, (screen.get_width() / 2 - table_surface.get_width() / 2, screen.get_height() / 2 - table_surface.get_height() / 2))
    pygame.display.update()
    clock.tick(60)
