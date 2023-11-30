import pygame
import random

# constants
SIZE = 6
CELL_SIZE = 100
CHAOS_SYMBOL = "x"
ORDER_SYMBOL = "o"

# files
chaos_image = pygame.image.load(r"chaos_and_order\Files\cross.png")
order_image = pygame.image.load(r"chaos_and_order\Files\circle.png")
square_image = pygame.image.load(r"chaos_and_order\Files\square.png")
cell_size = list([CELL_SIZE, CELL_SIZE])
chaos_image = pygame.transform.scale(chaos_image, cell_size)
order_image = pygame.transform.scale(order_image, cell_size)
square_image = pygame.transform.scale(square_image, cell_size)


# initialize matrix
table = []
for row in range(SIZE):
    table.append([0 for _ in range(SIZE)])
matrix = [list(row) for row in table]


class Square(pygame.sprite.Sprite):
    global chaos_image, order_image, square_image, click_sound

    def __init__(self, row, column):
        super().__init__()
        self.image = square_image
        self._pos_x = column * CELL_SIZE
        self._pos_y = row * CELL_SIZE
        self._row = row
        self._column = column
        self.rect = self.image.get_rect(topleft=(column * CELL_SIZE, row * CELL_SIZE))
        self._empty = True
        self._click_sound = click_sound

    def check_victory(self):
        pass

    def update_matrix(self, symbol):
        matrix[self._row][self._column] = symbol

    def update(self, symbol, player):
        if self._empty:
            if symbol == ORDER_SYMBOL:
                self.image = order_image
            else:
                self.image = chaos_image
            self._click_sound.play()
            self._empty = False

            self.check_victory()
            self.update_matrix(symbol)

            if player == "player":
                ai_move()
        elif player == "ai":
            ai_move()

    def input(self, events, mouse_pos, symbol):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos):
                self.update(symbol, player="player")


pygame.init()

click_sound = pygame.mixer.Sound(r"chaos_and_order\Files\click_sound.wav")
menu_music = pygame.mixer.Sound(r"chaos_and_order\Files/menu_music.wav")

screen = pygame.display.set_mode((SIZE * CELL_SIZE, SIZE * CELL_SIZE))
pygame.display.set_caption('Chaos and Order')
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 20)
chaos_image.convert()
order_image.convert()
square_image.convert()

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
# menu_music.play()

square = pygame.sprite.Group()


def display_text(text_list, font, x_pos, y_pos):
    for text in text_list:
        text_surface = font.render(text, False, "Red", "black")
        text_rect = text_surface.get_rect(center=(x_pos, y_pos))
        screen.blit(text_surface, text_rect)
        y_pos += 30


def create_table():
    row = 0
    column = 0
    for vertical in table:
        column = 0
        for rect in vertical:
            table[column][row] = Square(row, column)
            object = table[column][row]
            square.add(object)
            column += 1
        row += 1


def switch_symbol():
    global symbol
    if symbol == ORDER_SYMBOL:
        symbol = CHAOS_SYMBOL
    else:
        symbol = ORDER_SYMBOL


def ai_move():
    object = random.choice(square.sprites())
    symbol = random.choice([ORDER_SYMBOL, CHAOS_SYMBOL])
    object.update(symbol, player="ai")


running = True
game_active = False
symbol = ORDER_SYMBOL
player = ''


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
                elif order_rect.collidepoint(mouse_pos):
                    player = "order"
                square.empty()
                create_table()
                if player == "chaos":
                    ai_move()
                game_active = True
                events.clear()

    if game_active:
        square.draw(screen)
        for object in square:
            object.input(events, mouse_pos, symbol)

    else:
        screen.blit(title_surface, title_rect)
        display_text(rules_text, font, SIZE * 50, 200)
        pygame.draw.rect(screen, "BLUE", order_rect)
        pygame.draw.rect(screen, "RED", chaos_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

#  add logic
