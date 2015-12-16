import pygame
import os
from ..graphics import Surface,color_map

button_callback = None

class Wrapper(Surface):
    def __init__(self):
        self.surface = pygame.display.set_mode((470, 353))
        background = pygame.image.load(os.path.join(os.path.dirname(__file__), 'bot.png'))
        self.surface.blit(background,(0,0))
        self.screen = self.surface.subsurface((60,40,320,240))
        xPositions = (60, 100, 320, 360)
        self.buttons = []
        for x in range(4):
            self.buttons.append(Button(self.surface.subsurface(xPositions[x],0,22,12),x))

    def get_screen(self):
        return self.screen


class Button(Surface):
    def __init__(self,surface,number):
        from ..input import hit_areas,HitArea
        self.number = number
        surface.fill(color_map['white'])
        #register our button as something clickable
        self.surface = surface
        hit_areas.append(HitArea(pygame.Rect(surface.get_abs_offset(),surface.get_size()),self.click))

    def click(self,xy,action):
        if action=='down':
            (w,h) = self.surface.get_size()
            self.surface.fill((0,0,0,0),(0,0,w,h*0.2))
            self.surface.fill(color_map['white'],(0,h*0.2,w,h))
            if button_callback:
                button_callback(self.number,'down')
        elif action=='up':
            self.surface.fill(color_map['white'])
            if button_callback:
                button_callback(self.number,'up')


def fixup_window():
    pygame.init()
    wrapper = Wrapper()
    return wrapper.get_screen()

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
    global button_callback
    button_callback = callback

