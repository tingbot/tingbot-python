import pygame
import os

button_callback = None

left_margin = 25
bottom_margin = 12
top_margin = 12

bot_width = 470
bot_height = 353

background_color = (50, 50, 50)
button_color = (170, 170, 170)

simulator = None

class Simulator(object):
    def __init__(self):
        pygame.init()
        height = top_margin + bot_height + bottom_margin
        width = bot_width + left_margin
        self.surface = pygame.display.set_mode((width, height))

        self.screen = self.surface.subsurface((86, 54, 320, 240))
        bot_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'bot.png'))
        self.surface.fill(background_color)
        self.surface.blit(bot_image, (left_margin, top_margin))

        button_positions = (85, 125, 345, 385)
        self.buttons = []
        for button_index, x_position in enumerate(button_positions):
            button_surface = self.surface.subsurface(x_position, top_margin, 22, 12)
            button = Button(button_surface, button_index)
            self.buttons.append(button)

        pygame.display.update()


class Button(object):
    def __init__(self, surface, number):
        from ..input import hit_areas, HitArea
        self.number = number
        surface.fill(button_color)

        # register our button as something clickable
        self.surface = surface
        hit_areas.append(HitArea(pygame.Rect(surface.get_abs_offset(), surface.get_size()), self.click))

    def click(self, xy, action):
        if action == 'down':
            w, h = self.surface.get_size()
            self.surface.fill(background_color, (0, 0, w, h*0.2))
            self.surface.fill(button_color, (0, h*0.2, w, h))
            if button_callback:
                button_callback(self.number, 'down')
        elif action == 'up':
            self.surface.fill(button_color)
            if button_callback:
                button_callback(self.number, 'up')
        pygame.display.update((self.surface.get_abs_offset(), self.surface.get_size()))

def ensure_setup():
    if simulator is None:
        setup()

def setup():
    global simulator
    simulator = Simulator()

def create_main_surface():
    ensure_setup()
    return simulator.screen

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
    ensure_setup()
    global button_callback
    button_callback = callback
