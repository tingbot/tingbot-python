import pygame

is_setup = False

def ensure_setup():
    global is_setup
    if not is_setup:
        setup()
    is_setup = True


def setup():
    from platform_specific import setup_audio
    setup_audio()


class Sound(object):
    def __init__(self, path):
        self._pygame_sound = pygame.mixer.Sound(path)

    def play(self, loop=False):
        loops = -1 if loop else 0  # -1 means keep looping
        self._pygame_sound.play(loops=loops)

    def stop(self):
        self._pygame_sound.stop()
