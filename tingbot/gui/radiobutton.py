import pygame
from .widget import Widget
from ..graphics import _color


class RadioGroup(object):
    """A class to collect Radiobuttons together
    
    Attributes:
        selected: currently selected widget"""
    def __init__(self,callback=None):
        """create a new radiobutton group
        callback: function to call when one of the radiobuttons is pressed. Will be passed
                  two arguments - first is the buttons label, second is it's value
        """
        self.callback = callback
        self.widgets = []
        self.selected = None
        
    def add_button(self,widget):
        self.widgets.append(widget)
        
    def remove_button(self,widget):
        self.widgets.remove(widget)
        
    def remove_all(self):
        self.widgets[:] = []
        
    def widget_activated(self,widget):
        self.selected = widget
        #deactivate all other widgets
        for widg in self.widgets:
            if widg is not widget:
                widg.pressed = False
                widg.update(upwards=False,downwards=False)
        if self.callback:
            self.callback(widget.label,widget.value)
                
class RadioButton(Widget):
    """A Radio Button widget
    Attributes:
        label: text on the radio button
        value: the value of the radio button
        pressed: whether this button is pressed or not.
        callback: function to be called when the radiobutton value changes. Is passed True if radiobutton ticked
        
    Style Attributes:
        bg_color: background color
        radiobutton_color: color of the radio button
        radiobutton_text_color: color to use for text
        radiobutton_text_font: font to use (default)
        radiobutton_text_font_size: font size to use
    """
    def __init__(self, xy, size, align="center", parent=None, style=None, label="", value=None, group=None, callback=None):
        """create a button with size and position specified by xy, size and align
        it will have parent as a containing widget or will be placed directly on screen if parent is None
        use style to specify button color, activated button color, text color and font
        text: text to display on the radiobutton
        callback: a function to be called when the radio button is selected. No argument passed
        """
        super(RadioButton,self).__init__(xy,size,align,parent,style)
        self.label = label
        if value == None:
            self.value = label
        else:
            self.value = value
        if group==None:
            raise ValueError("Group must be specified")
        self.group = group
        self.group.add_button(self)
        self.callback = callback
        self.pressed = False
        
    def get_box_rect(self):
        """returns a rect for the area of the radiobutton"""
        (w,h) = self.size
        i = self.style.radiobutton_text_font_size
        return pygame.Rect((3,(h-i)/2),(i,i))    
        
    def on_touch(self,xy,action):
        if action=="up":
            if self.get_box_rect().inflate(3,3).collidepoint(xy):
                self.pressed = True
                self.group.widget_activated(self)
                if self.callback:
                    self.callback()
        self.update()
        
    def draw(self):
        #clear background
        self.fill(self.style.bg_color)
        #draw bounding box
        box = self.get_box_rect()
        pygame.draw.ellipse(self.surface,_color(self.style.radiobutton_color),box,1)
        
        if self.pressed:
            pygame.draw.ellipse(self.surface,_color(self.style.radiobutton_color),box.inflate(-6,-6),0)
        
        self.text(self.label,
                  xy = box.inflate(6,6).midright,
                  align = 'left',
                  color=self.style.radiobutton_text_color,
                  font = self.style.radiobutton_text_font,
                  font_size = self.style.radiobutton_text_font_size)
                  

