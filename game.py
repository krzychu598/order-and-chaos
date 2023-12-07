import pygame
from Square import square, opponent_move, initialize_matrix, create_sprites, check_victory
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
pygame.display.set_caption('Order and Chaos')
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 20)
big_font = pygame.font.Font(None, 100)

# convert images
chaos_image.convert()
order_image.convert()
square_image.convert()

title_surface = font.render('Order snd Chaos', True, "Red", "black")
title_rect = title_surface.get_rect(center=(screen_size // 2, 50))

order_rect = pygame.Rect((0, 400), screen.get_rect().center)
chaos_rect = pygame.Rect((screen_size // 2, 400), screen.get_rect().center)
pvp_rect = pygame.Rect((0, 100), screen.get_rect().center)
random_rect = pygame.Rect((screen_size // 2, 100), screen.get_rect().center)
ai_rect = pygame.Rect((0, screen_size // 2 + 100), (screen_size, screen_size))



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
    active_screen = "menu"
    player = ''
    symbol_text = big_font.render(symbol, False, "Black")
    stop_display_time = pygame.time.get_ticks()
    game_mode = None

    menu_music.set_volume(0.5)
    # menu_music.play()

    while active_screen is not None:
        current_time = pygame.time.get_ticks()
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()

        for event in events:

            if event.type == pygame.QUIT:
                active_screen = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()

            if active_screen == "game":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    symbol = switch_symbol(symbol)
                    symbol_text = big_font.render(symbol, False, "Black")
                    stop_display_time = current_time + 1200

            elif active_screen == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if chaos_rect.collidepoint(mouse_pos):
                        player = "chaos"
                        print("You play as chaos")
                    elif order_rect.collidepoint(mouse_pos):
                        player = "order"
                        print("You play as order")
                    if chaos_rect.collidepoint(mouse_pos) or order_rect.collidepoint(mouse_pos):
                        screen.fill("black")
                        active_screen = "menu2"
                        events.clear()

            elif active_screen == "menu2":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    next = False
                    if pvp_rect.collidepoint(mouse_pos):
                        print("you play against another player")
                        game_mode = "pvp"
                        next = True
                    if random_rect.collidepoint(mouse_pos):
                        print("your opponent plays randomly")
                        game_mode = "random_ai"
                        next = True
                    if ai_rect.collidepoint(mouse_pos):
                        print("you play against an ai")
                        game_mode = "smart_ai"
                        next = True
                    if next:
                        screen.fill("black")
                        initialize_matrix()
                        create_sprites()

                        if player == "chaos":
                            opponent_move(game_mode)
                        active_screen = "game"
                        events.clear()
                    

        if active_screen == "game":
            square.draw(screen)
            for object in square:
                object.input(events, mouse_pos, symbol, game_mode)

            if check_victory():
                win = True if player == check_victory() else False
                if win:
                    win_sound.play()
                else:
                    lose_sound.play()
                screen.fill("black")
                active_screen = "menu"

        elif active_screen == "menu":
            screen.blit(title_surface, title_rect)
            display_text(rules_text, font, screen_size // 2, 200)
            pygame.draw.rect(screen, "BLUE", order_rect)
            pygame.draw.rect(screen, "RED", chaos_rect)
        
        elif active_screen == "menu2":
            display_text(["Order and Chaos", "Who you wanna play against?"], font, screen_size // 2, 50)
            pygame.draw.rect(screen, "Blue", pvp_rect)
            pygame.draw.rect(screen, "Red", random_rect)
            pygame.draw.rect(screen, "Pink", ai_rect)

        if current_time < stop_display_time:
            screen.blit(symbol_text, symbol_text.get_rect(center = screen.get_rect().center))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
