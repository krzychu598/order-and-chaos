import pygame

# constants
SIZE = 6
TO_WIN = 5
CELL_SIZE = 100

# changing size of cell when chosen size of game is too big or too small
MIN_SCREEN_SIZE = 500
MAX_SCREEN_SIZE = 1000
CELL_SIZE = max(CELL_SIZE, MIN_SCREEN_SIZE // SIZE)
CELL_SIZE = min(CELL_SIZE, MAX_SCREEN_SIZE // SIZE)

CROSS = "x"
CIRCLE = "o"
screen_size = max(SIZE * CELL_SIZE, MIN_SCREEN_SIZE)
cell_size = list([CELL_SIZE, CELL_SIZE])
half_screen = screen_size // 2
SCREEN_SIZE = (screen_size, screen_size)
CENTER = (half_screen, half_screen)
rules_text = [
    "Order and Chaos",
    "",
    "",
    "",
    "The player Order strives to create a",
    "five-in-a-row of either Xs or Os.",
    "The opponent Chaos endeavors to prevent this.",
    "Click on square you want to put symbol in",
    "Press space to change symbol",
    "Who you wanna play as?",
]

# load images
chaos_image = pygame.image.load(r"Files/cross.png")
order_image = pygame.image.load(r"Files/circle.png")
square_image = pygame.image.load(r"Files/square.png")

# transform images
chaos_image = pygame.transform.scale(chaos_image, cell_size)
order_image = pygame.transform.scale(order_image, cell_size)
square_image = pygame.transform.scale(square_image, cell_size)

# create sprite group
square = pygame.sprite.Group()
