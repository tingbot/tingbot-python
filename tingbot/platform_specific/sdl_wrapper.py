import pygame
import os
from ..graphics import Surface, color_map

button_callback = None

left_margin = 25
bottom_margin = 12
top_margin = 12

bot_width = 470
bot_height = 353

wrapper = None


class Wrapper(Surface):
    def __init__(self):
        height = top_margin + bot_height + bottom_margin
        width = bot_width + left_margin
        self.surface = pygame.display.set_mode((width, height))
        background = pygame.image.load(os.path.join(os.path.dirname(__file__), 'bot.png'))
        self.surface.fill((50, 50, 50))
        self.surface.blit(background, (left_margin, top_margin))
        self.screen = self.surface.subsurface((86, 54, 320, 240))
        xPositions = (85, 125, 345, 385)
        self.buttons = []
        for x in range(4):
            self.buttons.append(Button(self.surface.subsurface(xPositions[x], top_margin, 22, 12), x))
        pygame.display.update()


class Button(Surface):
    def __init__(self, surface, number):
        from ..input import hit_areas, HitArea
        self.number = number
        self.color = color_map['grey']
        surface.fill(self.color)

        # register our button as something clickable
        self.surface = surface
        hit_areas.append(HitArea(pygame.Rect(surface.get_abs_offset(), surface.get_size()), self.click))

    def click(self, xy, action):
        if action == 'down':
            w, h = self.surface.get_size()
            self.surface.fill((0, 0, 0, 0), (0, 0, w, h*0.2))
            self.surface.fill(self.color, (0, h*0.2, w, h))
            if button_callback:
                button_callback(self.number, 'down')
        elif action == 'up':
            self.surface.fill(self.color)
            if button_callback:
                button_callback(self.number, 'up')
        pygame.display.update((self.surface.get_abs_offset(),self.surface.get_size()))

def initialise_if_needed():
    global wrapper
    if wrapper is None:
        pygame.init()
        wrapper = Wrapper()

def create_main_surface():
    initialise_if_needed()
    return wrapper.screen


def fixup_env():
    pass


def register_button_callback(callback):
    '''
    callback(button_index, action)
        button_index is a zero-based index that identifies which button has been pressed
        action is either 'down', or 'up'.

    The callback might not be called on the main thread.

    Currently only 'down' is implemented.
    '''
    initialise_if_needed()
    global button_callback
    button_callback = callback
