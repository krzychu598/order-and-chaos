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
    """
    Main function to run the Order and Chaos game.
    """
    pygame.init()

    # display screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Order and Chaos")

    # initialize clock
    clock = pygame.time.Clock()

    # load sounds and handle potential exceptions on non-Windows platforms
    do_sounds_work = True
    try:
        click_sound = pygame.mixer.Sound(r"Files/click_sound.wav")
        music = pygame.mixer.Sound(r"Files/menu_music.wav")
        lose_sound = pygame.mixer.Sound(r"Files/lose_sound.wav")
        win_sound = pygame.mixer.Sound(r"Files/win_sound.wav")
        lose_sound.set_volume(0.3)
        win_sound.set_volume(0.3)
    except pygame.error:
        do_sounds_work = False
        print("sounds work only on Windows")

    # create fonts for text rendering
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    big_font = pygame.font.Font(None, 100)

    # convert images
    chaos_image.convert()
    order_image.convert()
    square_image.convert()

    # set initial scene to Menu
    active_scene = Menu(screen)

    # Set up music if sound is enabled
    if do_sounds_work == True:
        music.set_volume(0.3)
        music.play()

    # main game loop
    while active_scene is not None:
        # get the current state
        current_time = pygame.time.get_ticks()
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()

        # handle events that could always happen
        for event in events:
            if event.type == pygame.QUIT:
                active_scene = None
            if do_sounds_work == True and event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()

        # here happen things specified in each scene class
        active_scene.ProcessInput(events, mouse_pos, current_time)
        active_scene.Render(screen=screen, font=font, extra_font=big_font)

        # change of scene
        if active_scene != active_scene.next_scene:
            # play game over sounds if sound is enabled
            if get_game_mode() == "game over" and do_sounds_work == True:
                if get_order_or_chaos() == check_victory():
                    win_sound.play()
                else:
                    lose_sound.play()
            active_scene = active_scene.next_scene

            # Clear the screen and events for the next scene
            screen.fill("black")
            events.clear()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    game()
