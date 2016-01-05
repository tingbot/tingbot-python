import pygame
from .widget import Widget
from ..graphics import _color


class Button(Widget):
    """A Button widget
    Attributes:
        but_text: text on the widget
        callback: function to call when the button is pressed. No arguments taken
        
    Style Attributes:
        bg_color: background color
        button_color: color of this button when not pressed
        button_pressed_color: color to use when button pressed
        button_rounding: rounding in pixels of button corners. use 0 for square corners
        button_text_color: color to use for text
        button_text_font: font to use (default)
        button_text_font_size: font size to use
    """
    def __init__(self, xy, size, align="center", parent=None, style=None, but_text="OK", callback=None):
        """create a button with size and position specified by xy, size and align
        it will have parent as a containing widget or will be placed directly on screen if parent is None
        use style to specify button color, activated button color, text color and font
        but_text: text to display on the button
        callback: a function to be called when the button is pressed
        """
        super(Button,self).__init__(xy,size,align,parent,style)
        self.but_text = but_text
        self.pressed = False
        self.callback = callback
        
    def on_touch(self,xy,action):
        if action=="down":
            self.pressed = True
        elif action=="up":
            self.pressed = False
            if pygame.Rect((0,0),self.size).collidepoint(xy):
                if self.callback:
                    self.callback()
        self.update()
        
    def draw(self):
        (w,h) = self.size
        if self.pressed:
            color = self.style.button_pressed_color
        else:
            color = self.style.button_color
        self.fill(self.style.bg_color)
        rounding = self.style.button_rounding
        #draw two cross-pieces
        self.surface.fill(_color(color),((rounding,0),(w-rounding*2,h)))
        self.surface.fill(_color(color),((0,rounding),(w,h-rounding*2)))
        #now do circles at the edges
        coords = [(x,y) for x in (rounding,w-rounding) for y in (rounding,h-rounding)]
        for pos in coords:
            pygame.draw.circle(self.surface,_color(color),pos,rounding)
        
        self.text(self.but_text,
                  color=self.style.button_text_color,
                  font = self.style.button_text_font,
                  font_size = self.style.button_text_font_size)
                  
class ToggleButton(Button):
    """A button widget
    Attributes:
        but_text: text on the widget
        pressed: whether the button is currently pressed or not
        callback: function to call when the button is pressed. Passes pressed as an argument

    Style Attributes:
        bg_color: background color
        button_color: color of this button when not pressed
        button_pressed_color: color to use when button pressed
        button_rounding: rounding in pixels of button corners. use 0 for square corners
        button_text_color: color to use for text
        button_text_font: font to use (default)
        button_text_font_size: font size to use
    """
    def on_touch(self,xy,action):
        if action=="down":
            self.pressed = not self.pressed
        elif action=="up":
            if pygame.Rect((0,0),self.size).collidepoint(xy):
                if self.callback:
                    self.callback(self.pressed)
            else:
                self.pressed = not self.pressed #revert to previous state if touch moves out of the button before release
        self.update()
