import pygame
from .widget import Widget
from ..graphics import _color


class CheckBox(Widget):
    """A CheckBox widget
    Attributes:
        label: text on the checkbox
        value: whether checkbox checked or not
        callback: function to be called when the checkbox value changes. Is passed True if checkbox ticked
        
    Style Attributes:
        bg_color: background color
        checkbox_color: color of the checkbox when not pressed
        checkbox_text_color: color to use for text
        checkbox_text_font: font to use (default)
        checkbox_text_font_size: font size to use
    """
    def __init__(self, xy, size, align="center", parent=None, style=None, label="", callback=None):
        """create a button with size and position specified by xy, size and align
        it will have parent as a containing widget or will be placed directly on screen if parent is None
        use style to specify button color, activated button color, text color and font
        text: text to display on the checkbox
        callback: a function to be called when the checkbox value changes. Is passed True if checkbox ticked
        """
        super(CheckBox,self).__init__(xy,size,align,parent,style)
        self.label = label
        self.value = False
        self.callback = callback
        
    def get_box_rect(self):
        """returns a rect for the area of the checkbox"""
        (w,h) = self.size
        i = self.style.checkbox_text_font_size
        return pygame.Rect((3,(h-i)/2),(i,i))    
        
    def on_touch(self,xy,action):
        if action=="up":
            (w,h) = self.size
            if self.get_box_rect().inflate(3,3).collidepoint(xy):
                self.value = not self.value
                if self.callback:
                    self.callback(self.value)
        self.update()
        
    def draw(self):
        (w,h) = self.size
        #clear background
        self.fill(self.style.bg_color)
        #draw bounding box
        box = self.get_box_rect()
        pygame.draw.rect(self.surface,_color(self.style.checkbox_color),box.inflate(1,1),1)
        
        if self.value:
            self.line(box.topleft,box.bottomright,color = self.style.checkbox_color)
            self.line(box.bottomleft,box.topright,color = self.style.checkbox_color)
        
        self.text(self.label,
                  xy = box.inflate(6,6).midright,
                  align = 'left',
                  color=self.style.checkbox_text_color,
                  font = self.style.checkbox_text_font,
                  font_size = self.style.checkbox_text_font_size)
                  

