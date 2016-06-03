# coding: utf8

class Line(object):
    def __init__(self, string, string_metrics):
        self.string = string
        self.string_metrics = string_metrics

    def truncate(self, max_width, ellipsis, ellipsis_metrics):
        '''
        Returns a copy of the line, truncated so the width is less than 'max_width' if necessary.
        If truncated, 'ellipsis' is added at the end.
        '''
        # do we need to truncate?
        string_width = sum(char_metric[4] for char_metric in self.string_metrics)

        if string_width <= max_width:
            return Line(self.string, self.string_metrics)

        ellipsis_width = sum(char_metric[4] for char_metric in ellipsis_metrics)
        string_max_width = max_width - ellipsis_width
        line_width = 0

        for string_i in xrange(len(self.string)):
            # [4] refers to the 'advance' metric
            line_width += self.string_metrics[string_i][4]

            if line_width > string_max_width:
                return Line(
                    string=self.string[:string_i] + ellipsis,
                    string_metrics=self.string_metrics[:string_i] + ellipsis_metrics)

    def __repr__(self):
        return 'Line(string=%r)' % self.string

class Typesetter(object):
    def __init__(self, string, string_metrics):
        self.string = string
        self.string_metrics = string_metrics
        self.line_start = 0

    def suggest_line_break(self, start_i, max_width):
        line_width = 0
        last_split_point = None

        string_i = start_i
        char = None

        for string_i in xrange(start_i, len(self.string)):
            prev_char = char
            char = self.string[string_i]

            # handle newlines
            if char == '\n':
                # '+ 1' means break after the newline character
                return string_i + 1

            # [4] refers to the 'advance' metric
            line_width += self.string_metrics[string_i][4]

            # always break at the end of a string of whitespace
            if char.isspace():
                continue

            if prev_char in (' ', '-', '\t'):
                last_split_point = string_i

            if line_width > max_width:
                if last_split_point is None:
                    # there wasn't a split point before the line was too big. Break here
                    if string_i == start_i:
                        # don't return zero character line
                        return string_i + 1
                    else:
                        return string_i
                else:
                    # there was a possible split point back there. Return up to that split point
                    return last_split_point

        # got to the end of the string without wrapping
        return len(self.string)

    def create_line(self, start_i, end_i, remove_trailing_whitespace=False):
        if remove_trailing_whitespace:
            string = self.string[start_i:end_i].rstrip()
            string_metrics = self.string_metrics[start_i:start_i+len(string)]
        else:
            string = self.string[start_i:end_i]
            string_metrics = self.string_metrics[start_i:end_i]

        return Line(string, string_metrics)

    def lines(self, max_lines, max_width, ellipsis, ellipsis_metrics):
        lines = []
        line_start_i = 0

        for line_i in xrange(max_lines):
            final_line = (line_i == max_lines - 1)

            if final_line:
                line_end_i = len(self.string)
                remove_trailing_whitespace = False
            else:
                line_end_i = self.suggest_line_break(line_start_i, max_width)
                # remove trailing whitespace if the line's been broken
                remove_trailing_whitespace = (line_end_i != len(self.string))

            line = self.create_line(line_start_i, line_end_i, remove_trailing_whitespace)

            if final_line:
                line = line.truncate(max_width, ellipsis, ellipsis_metrics)

            lines.append(line)

            if line_end_i == len(self.string):
                break

            line_start_i = line_end_i

        return lines

def render_text(string, font, antialias, color, max_lines, max_width, ellipsis=u'…', align=0):
    ''' Render a multiline string to a pygame surface.

    Arguments:
      string - the string to render
      font - the pygame Font object to use
      antialias - whether to antialias the text
      color - an RGB or RGBA triple describing the color
      max_lines - the maximum lines to use before truncating the string
      max_width - the maximum width of each line
      ellipsis - the string used to indicate more text wasn't displayed
      align - horizontal alignment - 0=left, 0.5=center, 1=right
    '''
    import pygame

    string_metrics = font.metrics(string)
    ellipsis_metrics = font.metrics(ellipsis)

    lines = Typesetter(string, string_metrics).lines(
        max_lines=max_lines,
        max_width=max_width,
        ellipsis=ellipsis,
        ellipsis_metrics=ellipsis_metrics)

    line_surfaces = []

    for line in lines:
        line_surfaces.append(font.render(line.string, antialias, color))

    width = max(s.get_width() for s in line_surfaces)
    height = sum(s.get_height() for s in line_surfaces)

    surface = pygame.Surface((width, height), flags=pygame.SRCALPHA)

    y = 0
    for line_surface in line_surfaces:
        x = (width - line_surface.get_width()) * align
        surface.blit(line_surface, (x, y))
        y += line_surface.get_height()

    return surface
