import pygame


class Scene:
    def __init__(self):
        self._next = self

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)


class Menu(Scene):
    def __init__(self):
        super().__init__()
    
    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass


class Menu2(Scene):
    def __init__(self):
        super().__init__()
    
    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass


class Game(Scene):
    def __init__(self):
        super().__init__()

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass


class GameOver(Scene):
    def __init__(self):
        super().__init__()

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass