# coding: utf8
import os, time, numbers, math, io, warnings, sys
import pygame
import requests
import cache
from .utils import cached_property

# colors from http://clrs.cc/
color_map = {
    'aqua': (127, 219, 255),
    'blue': (0, 116, 217),
    'navy': (0, 31, 63),
    'teal': (57, 204, 204),
    'green': (46, 204, 64),
    'olive': (61, 153, 112),
    'lime': (1, 255, 112),
    'yellow': (255, 220, 0),
    'orange': (255, 133, 27),
    'red': (255, 65, 54),
    'fuchsia': (240, 18, 190),
    'purple': (177, 13, 201),
    'maroon': (133, 20, 75),
    'white': (255, 255, 255),
    'silver': (221, 221, 221),
    'gray': (170, 170, 170),
    'grey': (170, 170, 170),
    'black': (0, 0, 0),
}

broken_image_file = os.path.join(os.path.dirname(__file__), 'broken_image.png')

def _xy_add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def _xy_subtract(t1, t2):
    return (t1[0] - t2[0], t1[1] - t2[1])

def _xy_multiply(t1, t2):
    return (t1[0] * t2[0], t1[1] * t2[1])

def _xy_magnitude(t):
    return math.hypot(t[0], t[1])

def _xy_normalize(t):
    '''
    Returns a vector in the same direction but with length 1
    '''
    mag = float(_xy_magnitude(t))
    return (t[0]/mag, t[1]/mag)

def _xy_rotate_90_degrees(t):
    '''
    Returns a rotated vector 90 degrees in the anti-clockwise direction
    '''
    return (-t[1], t[0])

def _color(identifier_or_tuple):
    try:
        return color_map[identifier_or_tuple]
    except KeyError:
        return identifier_or_tuple

def _scale(scale):
    """ Given a numeric input, return a 2-tuple with the number repeated.
        Given a 2-tuple input, return the input

    >>> _scale(2)
    (2, 2)
    >>> _scale((1, 2,))
    (1, 2)
    >>> _scale('nonsense')
    Traceback (most recent call last):
        ...
    TypeError: argument should be a number or a tuple
    >>> _scale((1,2,3))
    Traceback (most recent call last):
        ...
    ValueError: scale should be a 2-tuple
    """
    if isinstance(scale, tuple):
        if len(scale) != 2:
            raise ValueError('scale should be a 2-tuple')
        return scale
    elif isinstance(scale, numbers.Real):
        return (scale, scale)
    else:
        raise TypeError('argument should be a number or a tuple')

def _font(font, font_size, antialias):
    pygame.font.init()
    if font is None:
        font = os.path.join(os.path.dirname(__file__), 'Geneva.ttf')
        if antialias is None:
            antialias = (font_size < 9 or 17 < font_size)

    if antialias is None:
        antialias = True

    return pygame.font.Font(font, font_size), antialias

def _anchor(align):
    mapping = {
        'topleft': (0, 0),
        'left': (0, 0.5),
        'bottomleft': (0, 1),
        'top': (0.5, 0),
        'center': (0.5, 0.5),
        'bottom': (0.5, 1),
        'topright': (1, 0),
        'right': (1, 0.5),
        'bottomright': (1, 1),
    }

    return mapping[align]

def _xy_from_align(align, surface_size):
    return _xy_multiply(surface_size, _anchor(align))

def _topleft_from_aligned_xy(xy, align, size, surface_size):
    if xy is None:
        xy = _xy_from_align(align, surface_size)

    anchor_offset = _xy_multiply(_anchor(align), size)
    return _xy_subtract(xy, anchor_offset)

image_cache = cache.ImageCache()

class Surface(object):
    def __init__(self, surface=None):
        if surface is None:
            if not hasattr(self, '_create_surface'):
                raise TypeError('surface must not be nil')
        else:
            self.surface = surface

    @cached_property
    def surface(self):
        ''' this function is only called once if a surface is not set in the constructor '''
        surface = self._create_surface()

        if not surface:
            raise TypeError('_create_surface should return a pygame Surface')

        return surface

    @property
    def size(self):
        return self.surface.get_size()

    def _fill(self, color, rect = None):
        if len(color)<=3:
            self.surface.fill(color,rect)
        elif len(color)>=4:
            if rect is None:
                rect = (0,0)+self.size
            tmp_surface = pygame.Surface(rect[2:3],pygame.SRCALPHA)
            tmp_surface.fill(color)
            self.surface.blit(tmp_surface,rect)

    def fill(self, color):
        self._fill(_color(color))

    def text(self, string, xy=None, color='grey', align='center', font=None, font_size=32, antialias=None, max_width=sys.maxsize, max_height=sys.maxsize, max_lines=sys.maxsize):
        if xy is None:
            if max_width == sys.maxsize:
                max_width = 320
            if max_height == sys.maxsize:
                max_height = 240

        text_image = Image.from_text(
            string,
            color=color,
            font=font,
            font_size=font_size,
            antialias=antialias,
            max_lines=max_lines,
            max_width=max_width,
            max_height=max_height,
            align=_anchor(align)[0])

        self.image(text_image, xy, align=align)

    def rectangle(self, xy=None, size=(100, 100), color='grey', align='center'):
        if len(size) != 2:
            raise ValueError('size should be a 2-tuple')

        xy = _topleft_from_aligned_xy(xy, align, size, self.size)

        self._fill(_color(color), xy+size)

    def line(self, start_xy, end_xy, width=1, color='grey', antialias=True):
        # antialiased thick lines aren't supported by pygame, and the aaline function has some
        # strange bugs on OS X (line comes out the wrong colors, see http://stackoverflow.com/q/24208783/382749)
        # so antialiasing isn't currently supported.

        if width == 1:
            pygame.draw.line(self.surface, _color(color), start_xy, end_xy, width)
        else:
            # we use a polygon to draw thick lines because the pygame line function has a very
            # strange line cap

            delta = _xy_subtract(end_xy, start_xy)
            delta_rotated = _xy_rotate_90_degrees(delta)

            # this is a hack to draw line the correct size - pygame.draw.polygon seems to outline
            # the polygons it draws as well as fill them, making the lines too thick.
            width -= 1

            perpendicular_offset = _xy_multiply(_xy_normalize(delta_rotated), _scale(width*0.5))

            points = (
                _xy_add(start_xy, perpendicular_offset),
                _xy_add(end_xy, perpendicular_offset),
                _xy_subtract(end_xy, perpendicular_offset),
                _xy_subtract(start_xy, perpendicular_offset),
            )

            pygame.draw.polygon(self.surface, _color(color), points)

    def image(self, image, xy=None, scale=1, align='center', raise_error=True):
        if isinstance(image, basestring):
            try:
                image = image_cache.get_image(image)
            except IOError:
                if raise_error:
                    raise
                else:
                    image = image_cache.get_image(broken_image_file)

        scale = _scale(scale)
        image_size = image.size

        surface = image.surface

        if scale != (1, 1):
            image_size = _xy_multiply(image_size, scale)
            image_size = tuple(int(d) for d in image_size)
            try:
                surface = pygame.transform.smoothscale(surface, image_size)
            except ValueError:
                surface = pygame.transform.scale(surface, image_size)

        xy = _topleft_from_aligned_xy(xy, align, image_size, self.size)

        self.surface.blit(surface, xy)


class Screen(Surface):
    def __init__(self):
        super(Screen, self).__init__()
        self.needs_update = False
        self.has_surface = False

    def _create_surface(self):
        from . import platform_specific
        surface = platform_specific.create_main_surface()
        self.has_surface = True
        return surface

    def ensure_display_setup(self):
        # setup pygame.display by calling the self.surface getter
        self.surface

    def update(self):
        pygame.display.update()
        self.needs_update = False

    def fill(self, *args, **kwargs):
        super(Screen, self).fill(*args, **kwargs)
        self.needs_update = True

    def text(self, *args, **kwargs):
        super(Screen, self).text(*args, **kwargs)
        self.needs_update = True

    def rectangle(self, *args, **kwargs):
        super(Screen, self).rectangle(*args, **kwargs)
        self.needs_update = True

    def image(self, *args, **kwargs):
        super(Screen, self).image(*args, **kwargs)
        self.needs_update = True

    def update_if_needed(self):
        if self.needs_update:
            self.update()


screen = Screen()


class Image(Surface):
    @classmethod
    def load(cls, filename):
        warnings.warn(
            'Image.load is deprecated. Use Image.load_filename instead.',
            DeprecationWarning,
            stacklevel=2)
        return cls.load_filename(filename)

    @classmethod
    def load_filename(cls, filename):
        """Open a local file as an Image"""
        image_file = open(filename, 'rb')
        return cls.load_file(image_file, filename)

    @classmethod
    def load_url(cls, url):
        """Open a url as an Image"""
        response = requests.get(url)
        response.raise_for_status()
        image_file = io.BytesIO(response.content)
        return cls.load_file(image_file, url)

    @classmethod
    def load_file(cls, file_object, name_hint):
        """load a file-like object as an image. Takes name_hint as an optional extra - if this
           finishes with .gif, then a GIFImage will be returned"""
        with file_object:
            # if it's a gif, load it using the special GIFImage class
            _, extension = os.path.splitext(name_hint)
            if extension.lower() == '.gif':
                return GIFImage(image_file=file_object)

            # ensure the screen surface has been created (otherwise pygame doesn't know the 'video mode')
            screen.ensure_display_setup()

            surface = pygame.image.load(file_object)
            surface = surface.convert_alpha()

        return cls(surface)

    @classmethod
    def from_text(cls, string, color='grey', font=None, font_size=32, antialias=None, max_lines=sys.maxsize, max_width=sys.maxsize, max_height=sys.maxsize, align=0):
        font, antialias = _font(font, font_size, antialias)
        color = _color(color)
        string = unicode(string)

        from .typesetter import render_text

        if max_height != sys.maxsize:
            line_height = font.get_linesize()
            max_lines = min(max_lines, int(max_height/line_height))

        surface = render_text(string, font, antialias, color, max_lines, max_width, ellipsis=u'…', align=align)

        return cls(surface=surface)

    def __init__(self, surface=None, size=None):
        pygame.init()
        surface = surface or pygame.Surface(size)
        super(Image, self).__init__(surface)

    def get_memory_usage(self):
        return self.surface.get_buffer().length

class GIFImage(Surface):
    def __init__(self, image_file): #image_file can be either a file-like object or filename
        pygame.init()
        from PIL import Image as PILImage
        self.frames = self._get_frames(PILImage.open(image_file))
        self.total_duration = sum(f[1] for f in self.frames)

    def _get_frames(self, pil_image):
        result = []

        pal = pil_image.getpalette()
        base_palette = []
        for i in range(0, len(pal), 3):
            rgb = pal[i:i+3]
            base_palette.append(rgb)

        all_tiles = []
        try:
            while 1:
                if not pil_image.tile:
                    pil_image.seek(0)
                if pil_image.tile:
                    all_tiles.append(pil_image.tile[0][3][0])
                pil_image.seek(pil_image.tell()+1)
        except EOFError:
            pil_image.seek(0)

        all_tiles = tuple(set(all_tiles))

        while 1:
            try:
                duration = pil_image.info["duration"] * 0.001
            except KeyError:
                duration = 0.1

            if all_tiles:
                if all_tiles in ((6,), (7,)):
                    pal = pil_image.getpalette()
                    palette = []
                    for i in range(0, len(pal), 3):
                        rgb = pal[i:i+3]
                        palette.append(rgb)
                elif all_tiles in ((7, 8), (8, 7)):
                    pal = pil_image.getpalette()
                    palette = []
                    for i in range(0, len(pal), 3):
                        rgb = pal[i:i+3]
                        palette.append(rgb)
                else:
                    palette = base_palette
            else:
                palette = base_palette
            try: # account for different versions of Pillow
                pygame_image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)
            except AttributeError:
                pygame_image = pygame.image.fromstring(pil_image.tostring(), pil_image.size, pil_image.mode)
            pygame_image.set_palette(palette)

            if "transparency" in pil_image.info:
                pygame_image.set_colorkey(pil_image.info["transparency"])

            result.append([pygame_image, duration])
            try:
                pil_image.seek(pil_image.tell()+1)
            except EOFError:
                break

        return result

    @property
    def surface(self):
        current_time = time.time()

        if not hasattr(self, 'start_time'):
            self.start_time = current_time

        try:
            gif_time = (current_time - self.start_time) % self.total_duration
        except ZeroDivisionError:
            gif_time = 0

        frame_time = 0

        for surface, duration in self.frames:
            frame_time += duration

            if frame_time >= gif_time:
                return surface

    def get_memory_usage(self):
        return sum(x[0].get_buffer().length for x in self.frames)
