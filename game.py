import pygame
from constants import (
    chaos_image,
    order_image,
    square_image,
    SCREEN_SIZE,
)
from functions import check_victory
from scenes import Menu, Game


def main():
    pygame.init()

    # display screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Order and Chaos")

    # initialize clock
    clock = pygame.time.Clock()
    stop_display_time = pygame.time.get_ticks()

    # load sounds
    click_sound = pygame.mixer.Sound(r"chaos_and_order\Files/click_sound.wav")
    menu_music = pygame.mixer.Sound(r"chaos_and_order\Files/menu_music.wav")
    menu_click = pygame.mixer.Sound(r"chaos_and_order\Files/menu_click.wav")
    lose_sound = pygame.mixer.Sound(r"chaos_and_order\Files/lose_sound.wav")
    win_sound = pygame.mixer.Sound(r"chaos_and_order\Files/win_sound.wav")

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
    menu_music.set_volume(0.5)
    # menu_music.play()

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()

        # here happen things specified in each scene class
        active_scene.ProcessInput(events, mouse_pos, current_time)
        active_scene.Update()
        active_scene.Render(screen=screen, font=font, extra_font=big_font)

        if isinstance(active_scene, Game):
            win = check_victory()
            if win is not None:
                if win:
                    win_sound.play()
                elif win == False:
                    lose_sound.play()

        if active_scene != active_scene.next_scene:
            active_scene = active_scene.next_scene
            screen.fill("black")
            events.clear()
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
