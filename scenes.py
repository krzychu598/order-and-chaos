import pygame
from functions import (
    display_text,
    display_rects,
    opponent_move,
    create_sprites,
    check_victory,
    initialize,
    set_order_or_chaos,
    set_game_mode,
    switch_symbol,
    update_square,
    get_symbol,
)
from constants import (
    CENTER,
    rules_text,
    square,
    screen_size,
    half_screen,
)

from Square import Square

# in this module scenes are created.
# Depending on the current scene different things are being displayed on screen
# also input is being processed differently


class Scene:
    """
    Base scene
    """

    def __init__(self, screen):
        self.screen = screen
        self.next_scene = self
        self.current_time = 0
        self.stop_display_time = 0

    def ProcessInput(self):
        pass

    def Render(self):
        pass

    def SwitchToScene(self, next_scene):
        self.next_scene = next_scene

    def Terminate(self):
        self.SwitchToScene(None)


class Menu(Scene):
    """
    Menu to choose game role
    """

    def __init__(self, screen):
        super().__init__(screen)
        self._order_rect = pygame.Rect((0, 400), (half_screen, half_screen // 2))
        self._chaos_rect = pygame.Rect(
            (half_screen, 400), (half_screen, half_screen // 2)
        )
        self._main_menu = [(self._order_rect, "Order"), (self._chaos_rect, "Chaos")]
        initialize()
        create_sprites(Square)

    def ProcessInput(self, events, mouse_pos, current_time):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._chaos_rect.collidepoint(mouse_pos):
                    set_order_or_chaos("chaos")
                    self.SwitchToScene(ChooseMode(self.screen))
                elif self._order_rect.collidepoint(mouse_pos):
                    set_order_or_chaos("order")
                    self.SwitchToScene(ChooseMode(self.screen))

    def Render(self, screen, font, *args, **kwargs):
        display_text(screen, rules_text, font, screen_size // 2, 50)
        display_rects(screen, self._main_menu, font)


class ChooseMode(Scene):
    """
    Menu to choose game mode allows to play against another player, random ai and smart ai
    """

    def __init__(self, screen):
        super().__init__(screen)
        self._pvp_rect = pygame.Rect((0, 200), (half_screen, half_screen // 2))
        self._random_rect = pygame.Rect(
            (half_screen, 200), (half_screen, half_screen // 2)
        )
        self._ai_rect = pygame.Rect(
            (0, half_screen // 2 + 200), (screen_size, half_screen // 2)
        )
        self._game_mode_menu = [
            (self._pvp_rect, "player vs player"),
            (self._random_rect, "random"),
            (self._ai_rect, "ai"),
        ]

    def ProcessInput(self, events, mouse_pos, current_time):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                next = False
                if self._pvp_rect.collidepoint(mouse_pos):
                    print("you play against another player")
                    set_game_mode("pvp")
                    next = True
                if self._random_rect.collidepoint(mouse_pos):
                    print("your opponent plays randomly")
                    set_game_mode("random_ai")
                    next = True
                if self._ai_rect.collidepoint(mouse_pos):
                    print("you play against an ai")
                    set_game_mode("smart_ai")
                    next = True
                if next:
                    opponent_move(begin=True)
                    self.SwitchToScene(Game(self.screen))

    def Render(self, screen, font, *args, **kwargs):
        display_text(
            screen,
            ["Order and Chaos", "Who you wanna play against?"],
            font,
            screen_size // 2,
            50,
        )
        display_rects(screen, self._game_mode_menu, font)


class Game(Scene):
    """
    Menu handling events in game
    """

    def __init__(self, screen):
        super().__init__(screen)

    def ProcessInput(self, events, mouse_position, current_time):
        mouse_pos = mouse_position
        self.current_time = current_time
        for event in events:
            """Switch symbol if space pressed"""
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                switch_symbol()
                self.stop_display_time = self.current_time + 1200

            if event.type == pygame.MOUSEBUTTONDOWN:
                """Updates clicked square"""
                update_square(mouse_pos)
                if check_victory() is not None:
                    set_game_mode("game over")
                    self.SwitchToScene(GameOver(self.screen, check_victory()))

    def Render(self, screen, extra_font, *args, **kwargs):
        square.draw(screen)
        self.symbol_text = extra_font.render(get_symbol(), True, "Black")

        if self.current_time < self.stop_display_time:
            screen.blit(self.symbol_text, self.symbol_text.get_rect(center=CENTER))


class GameOver(Scene):
    """
    Game over scene allows to play again or quit
    """

    def __init__(self, screen, who_won):
        super().__init__(screen)
        self._won = who_won
        self._play_again = pygame.Rect((0, 200), (half_screen, half_screen // 2))
        self._quit = pygame.Rect((half_screen, 200), (half_screen, half_screen // 2))
        self._over_options = [(self._play_again, "Play again"), (self._quit, "Quit")]

    def ProcessInput(self, events, mouse_pos, current_time):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._play_again.collidepoint(mouse_pos):
                    self.SwitchToScene(Menu(self.screen))
                elif self._quit.collidepoint(mouse_pos):
                    self.Terminate()

    def Render(self, screen, font, *args, **kwargs):
        display_text(
            screen,
            [f"{self._won.upper()} won"],
            font,
            screen_size // 2,
            50,
        )
        display_rects(screen, self._over_options, font)
