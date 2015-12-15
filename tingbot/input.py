import pygame
import sys
from collections import namedtuple
from .utils import call_with_optional_arguments
from .graphics import screen

mouse_down = False
hit_areas = []
active_hit_areas = []

HitArea = namedtuple('HitArea', ('rect', 'relative', 'callback'))

def poll():
    if not pygame.display.get_init():
        return

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down(pygame.mouse.get_pos())

        elif event.type == pygame.MOUSEMOTION:
            mouse_move(pygame.mouse.get_pos())

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_up(pygame.mouse.get_pos())

        elif event.type == pygame.KEYDOWN:
            command_down = (event.mod & 1024) or (event.mod & 2048)

            if event.key == 113 and command_down:
                sys.exit()

        elif event.type == pygame.QUIT:
            sys.exit()

def mouse_down(pos):
    from .graphics import screen, _xy_subtract
    for hit_area in hit_areas:
        if hit_area.rect.collidepoint(pos):
            active_hit_areas.append(hit_area)
            if hit_area.relative:
                temp_pos = _xy_subtract(pos,screen.surface.get_abs_offset())
            else:
                temp_pos = pos
            call_with_optional_arguments(hit_area.callback, xy=temp_pos, action='down')

def mouse_move(pos):
    from .graphics import screen, _xy_subtract
    for hit_area in active_hit_areas:
        if hit_area.relative:
            temp_pos = _xy_subtract(pos,screen.surface.get_abs_offset())
        else:
            temp_pos = pos
        call_with_optional_arguments(hit_area.callback, xy=temp_pos, action='move')

def mouse_up(pos):
    from .graphics import screen, _xy_subtract
    for hit_area in active_hit_areas:
        if hit_area.relative:
            temp_pos = _xy_subtract(pos,screen.surface.get_abs_offset())
        else:
            temp_pos = pos
        call_with_optional_arguments(hit_area.callback, xy=temp_pos, action='up')

    active_hit_areas[:] = []

class touch(object):
    def __init__(self, xy=None, size=None, align='center'):
        from .graphics import _topleft_from_aligned_xy, screen, _xy_add

        if xy is None and size is None:
            xy = (160, 120)
            size = screen.size
            align = 'center'
        elif size is None:
            size = (50, 50)

        topleft = _topleft_from_aligned_xy(xy=xy, align=align, size=size, surface_size=screen.size)
        offset = screen.surface.get_abs_offset()
        topleft  = _xy_add(topleft,offset)
        self.rect = pygame.Rect(topleft, size)

    def __call__(self, f):
        hit_areas.append(HitArea(self.rect, True, f))
        return f
