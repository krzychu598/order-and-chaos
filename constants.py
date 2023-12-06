import pygame

SIZE = 6
CELL_SIZE = 100
MIN_SCREEN_SIZE = 500
CELL_SIZE = max(CELL_SIZE, MIN_SCREEN_SIZE // SIZE)
CHAOS_SYMBOL = "x"
ORDER_SYMBOL = "o"
WIN_CONDITION = 5

rules_text = ["The player Order strives to create a",
              "five-in-a-row of either Xs or Os.",
              "The opponent Chaos endeavors to prevent this.",
              "Press space to change symbol",
              "Who you wanna play as?", "ORDER              CHAOS"]

chaos_image = pygame.image.load(r"chaos_and_order\Files\cross.png")
order_image = pygame.image.load(r"chaos_and_order\Files\circle.png")
square_image = pygame.image.load(r"chaos_and_order\Files\square.png")
cell_size = list([CELL_SIZE, CELL_SIZE])
chaos_image = pygame.transform.scale(chaos_image, cell_size)
order_image = pygame.transform.scale(order_image, cell_size)
square_image = pygame.transform.scale(square_image, cell_size)
