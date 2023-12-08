import pygame
from functions import (
    display_text,
    display_rects,
    switch_symbol,
    opponent_move,
    initialize_matrix,
    create_sprites,
    check_victory,
    matrix,
)
from constants import (
    ORDER_SYMBOL,
    CHAOS_SYMBOL,
    CENTER,
    rules_text,
    square,
    screen_size,
    half_screen,
)

from Square import Square


class StateOfTheGame:
    def __init__(self):
        self._symbol = ORDER_SYMBOL
        self._game_mode = None
        self._order_or_chaos = None

    @property
    def get_symbol(self):
        return self._symbol

    def set_symbol(self, symbol):
        self._symbol = symbol

    @property
    def get_game_mode(self):
        return self._game_mode

    def set_game_mode(self, game_mode):
        self._game_mode = game_mode

    @property
    def get_order_or_chaos(self):
        return self._order_or_chaos

    def set_order_or_chaos(self, order_or_chaos):
        self._order_or_chaos = order_or_chaos

    def switch_symbol(self):
        if self._symbol == ORDER_SYMBOL:
            self._symbol = CHAOS_SYMBOL
        else:
            self._symbol = ORDER_SYMBOL


state = StateOfTheGame()


class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.next_scene = self
        self.current_time = 0
        self.stop_display_time = 0

    def ProcessInput(self):
        pass

    def Update(self):
        pass

    def Render(self):
        pass

    def SwitchToScene(self, next_scene):
        self.next_scene = next_scene

    def Terminate(self):
        self.SwitchToScene(None)


class Menu(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self._order_rect = pygame.Rect((0, 400), (half_screen, half_screen // 2))
        self._chaos_rect = pygame.Rect(
            (half_screen, 400), (half_screen, half_screen // 2)
        )
        self._main_menu = [(self._order_rect, "Order"), (self._chaos_rect, "Chaos")]

    def ProcessInput(self, events, mouse_pos, current_time):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._chaos_rect.collidepoint(mouse_pos):
                    state.set_order_or_chaos("chaos")
                    self.SwitchToScene(ChooseMode(self.screen))
                elif self._order_rect.collidepoint(mouse_pos):
                    state.set_order_or_chaos("order")
                    self.SwitchToScene(ChooseMode(self.screen))

    def Update(self):
        pass

    def Render(self, screen, font, *args, **kwargs):
        display_text(screen, rules_text, font, screen_size // 2, 50)
        display_rects(screen, self._main_menu, font)

    def SwitchToScene(self, next_scene):
        return super().SwitchToScene(next_scene)


class ChooseMode(Scene):
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
                    state.set_game_mode("pvp")
                    next = True
                if self._random_rect.collidepoint(mouse_pos):
                    print("your opponent plays randomly")
                    state.set_game_mode("random_ai")
                    next = True
                if self._ai_rect.collidepoint(mouse_pos):
                    print("you play against an ai")
                    state.set_game_mode("smart_ai")
                    next = True
                if next:
                    self.screen.fill("black")
                    initialize_matrix()
                    create_sprites(Square)

                    if state.get_order_or_chaos == "chaos":
                        opponent_move(state.get_game_mode)
                    self.SwitchToScene(Game(self.screen))

    def Update(self):
        pass

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
    def __init__(self, screen):
        super().__init__(screen)

    def ProcessInput(self, events, mouse_position, current_time):
        mouse_pos = mouse_position
        self.current_time = current_time
        for event in events:
            """Switch symbol if space pressed"""
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state.switch_symbol()
                self.stop_display_time = self.current_time + 1200
        for object in square:
            object.input(events, mouse_pos, state.get_symbol, state.get_game_mode)

    def Update(self):
        if check_victory():
            win = True if state.get_order_or_chaos == check_victory() else False
            self.SwitchToScene(GameOver(self.screen, win))

    def Render(self, screen, extra_font, *args, **kwargs):
        square.draw(screen)
        self.symbol_text = extra_font.render(state.get_symbol, True, "Black")

        if self.current_time < self.stop_display_time:
            screen.blit(self.symbol_text, self.symbol_text.get_rect(center=CENTER))


class GameOver(Scene):
    def __init__(self, screen, win):
        super().__init__(screen)
        self._state = win
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

    def Update(self):
        pass

    def Render(self, screen, font, *args, **kwargs):
        display_text(
            screen,
            [f"You won" if self._state else "You lost"],
            font,
            screen_size // 2,
            50,
        )
        display_rects(screen, self._over_options, font)
