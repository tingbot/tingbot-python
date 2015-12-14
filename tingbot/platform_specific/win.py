import os

window_controller = None

def fixup_window():
    window_controller = None


def fixup_env():
    import pygame
    icon_file = os.path.join(os.path.dirname(__file__), 'simulator-icon.png')
    pygame.display.set_icon(pygame.image.load(icon_file))
    pygame.display.set_caption("TingbotSimulator")

button_callback = None


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
