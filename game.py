import pygame
from Square import Square, square, ai_move, initialize_matrix, create_sprites, check_victory
from constants import SIZE, CELL_SIZE, CHAOS_SYMBOL, ORDER_SYMBOL, MIN_SCREEN_SIZE, chaos_image, order_image, square_image, rules_text
pygame.init()

# load sounds
click_sound = pygame.mixer.Sound(r"chaos_and_order\Files/click_sound.wav")
menu_music = pygame.mixer.Sound(r"chaos_and_order\Files/menu_music.wav")
menu_click = pygame.mixer.Sound(r"chaos_and_order\Files/menu_click.wav")
lose_sound = pygame.mixer.Sound(r"chaos_and_order\Files/lose_sound.wav")
win_sound = pygame.mixer.Sound(r"chaos_and_order\Files/win_sound.wav")

screen_size = max(SIZE * CELL_SIZE, MIN_SCREEN_SIZE)
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption('Chaos and Order')
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 20)

# convert images
chaos_image.convert()
order_image.convert()
square_image.convert()

title_surface = font.render('Chaos and Order', True, "Red", "black")
title_rect = title_surface.get_rect(center=(screen_size // 2, 50))

order_rect = pygame.Rect((0, 400), (screen_size // 2, screen_size // 2))
chaos_rect = pygame.Rect((screen_size // 2, 400), (screen_size // 2, screen_size // 2))


def display_text(text_list, font, x_pos, y_pos):
    for text in text_list:
        text_surface = font.render(text, False, "Red", "black")
        text_rect = text_surface.get_rect(center=(x_pos, y_pos))
        screen.blit(text_surface, text_rect)
        y_pos += 30


def switch_symbol(symbol):
    if symbol == ORDER_SYMBOL:
        symbol = CHAOS_SYMBOL
    else:
        symbol = ORDER_SYMBOL
    return symbol


def main():
    symbol = ORDER_SYMBOL
    game_active = False
    running = True
    player = ''

    menu_music.set_volume(0.5)
    # menu_music.play()

    while running:
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()

        for event in events:

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()

            if game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    symbol = switch_symbol(symbol)
                    start_time = pygame.time

            else:
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if chaos_rect.collidepoint(mouse_pos):
                        player = "chaos"
                        print("You play as chaos")
                    elif order_rect.collidepoint(mouse_pos):
                        player = "order"
                        print("You play as order")
                    if chaos_rect.collidepoint(mouse_pos) or order_rect.collidepoint(mouse_pos):
                        screen.fill("black")
                        initialize_matrix()
                        create_sprites()

                        if player == "chaos":
                            ai_move()

                        game_active = True
                        events.clear()

        if game_active:
            if check_victory() == "order won":
                if player == "order":
                    print("Order won! You win!") #you win
                    win_sound.play()
                else:
                    print("Order won!, You lose!") #you lose
                    lose_sound.play()
                screen.fill("black")
                game_active = False
            elif check_victory() == "chaos won":
                if player == "chaos":
                    print("Chaos won! You win!") #you win
                    win_sound.play()
                else:
                    print("Chaos won!, You lose!") #you lose
                    lose_sound.play()
                screen.fill("black")
                game_active = False
            else:
                square.draw(screen)
                for object in square:
                    object.input(events, mouse_pos, symbol)
        else:
            screen.blit(title_surface, title_rect)
            display_text(rules_text, font, screen_size // 2, 200)
            pygame.draw.rect(screen, "BLUE", order_rect)
            pygame.draw.rect(screen, "RED", chaos_rect)

        pygame.display.update()
        clock.tick(60)
        pygame.time.Clock.tick

    pygame.quit()


if __name__ == "__main__":
    main()
