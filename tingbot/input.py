import pygame
import sys
from collections import namedtuple
from .utils import call_with_optional_arguments
from .graphics import screen, _topleft_from_aligned_xy, _xy_add, _xy_subtract

mouse_down = False
hit_areas = []
active_hit_areas = []

HitArea = namedtuple('HitArea', ('rect', 'callback'))

class EventHandler(object):
    """call poll to handle touch events. Inherit from this class if you want
    to create a new touch handler, eg for within a modal dialog box"""

    def poll(self):
        if not pygame.display.get_init():
            return
        for event in pygame.event.get():
            # filter events if a touch handler is installed
            self.touch_handler(event)
            if event.type == pygame.KEYDOWN:
                command_down = (event.mod & 1024) or (event.mod & 2048)

                if event.key == 113 and command_down:
                    sys.exit()

            elif event.type == pygame.QUIT:
                sys.exit()

    def touch_handler(self, event):
        handle_events(event)

def handle_events(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_down(pygame.mouse.get_pos())

    elif event.type == pygame.MOUSEMOTION:
        mouse_move(pygame.mouse.get_pos())

    elif event.type == pygame.MOUSEBUTTONUP:
        mouse_up(pygame.mouse.get_pos())


def mouse_down(pos):
    for hit_area in hit_areas:
        if hit_area.rect.collidepoint(pos):
            active_hit_areas.append(hit_area)
            call_with_optional_arguments(hit_area.callback, xy=pos, action='down')

def mouse_move(pos):
    for hit_area in active_hit_areas:
        call_with_optional_arguments(hit_area.callback, xy=pos, action='move')

def mouse_up(pos):
    for hit_area in active_hit_areas:
        call_with_optional_arguments(hit_area.callback, xy=pos, action='up')

    # clear the list
    active_hit_areas[:] = []

class touch(object):
    def __init__(self, xy=None, size=None, align='center'):
        if xy is None and size is None:
            xy = (160, 120)
            size = screen.size
            align = 'center'
        elif size is None:
            size = (50, 50)

        topleft = _topleft_from_aligned_xy(xy=xy, align=align, size=size, surface_size=screen.size)
        self.offset = screen.surface.get_abs_offset()
        topleft = _xy_add(topleft, self.offset)
        self.rect = pygame.Rect(topleft, size)

    def __call__(self, f):
        def offset_callback(xy, action):
            temp_xy = _xy_subtract(xy, self.offset)
            call_with_optional_arguments(f, xy=temp_xy, action=action)

        hit_areas.append(HitArea(self.rect, offset_callback))
        return f
