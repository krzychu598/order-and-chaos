import pygame
from constants import (
    chaos_image,
    order_image,
    square_image,
    SCREEN_SIZE,
)
from functions import check_victory, get_game_mode, get_order_or_chaos
from scenes import Menu


def game():
    pygame.init()

    # display screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Order and Chaos")

    # initialize clock
    clock = pygame.time.Clock()

    # load sounds
    # click_sound = pygame.mixer.Sound(r"chaos_and_order/Files/click_sound.wav")
    # music = pygame.mixer.Sound(r"chaos_and_order/Files/menu_music.wav")
    # lose_sound = pygame.mixer.Sound(r"chaos_and_order/Files/Files/lose_sound.wav")
    # win_sound = pygame.mixer.Sound(r"chaos_and_order/Files/win_sound.wav")
    # lose_sound.set_volume(0.3)
    # win_sound.set_volume(0.3)

    # create fonts
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    big_font = pygame.font.Font(None, 100)

    # convert images
    chaos_image.convert()
    order_image.convert()
    square_image.convert()

    # initial settings
    active_scene = Menu(screen)

    # set music
    # music.set_volume(0.3)
    # music.play()

    # main game loop
    while active_scene is not None:
        # get current state
        current_time = pygame.time.get_ticks()
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()

        # events that could always happen
        for event in events:
            if event.type == pygame.QUIT:
                active_scene = None
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     click_sound.play()

        # here happen things specified in each scene class
        active_scene.ProcessInput(events, mouse_pos, current_time)
        active_scene.Render(screen=screen, font=font, extra_font=big_font)

        # change of scene
        if active_scene != active_scene.next_scene:
            # play game over sounds
            # if get_game_mode() == "game over":
            #     if get_order_or_chaos() == check_victory():
            #         win_sound.play()
            #     else:
            #         lose_sound.play()
            active_scene = active_scene.next_scene

            screen.fill("black")
            events.clear()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    game()
