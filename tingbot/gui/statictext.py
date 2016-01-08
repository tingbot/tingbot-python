from .widget import Widget
from ..graphics import _xy_from_align

class StaticText(Widget):
    """ A Text widget.
    This does nothing except from display text in a specified place on the screen
    
    Attributes:
        label: the text to display
        text_align: alignment of the text within the widget
    
    Style Attributes:
        bg_color
        statictext_color
        statictext_font
        statictext_font_size
    """
    def __init__(self,xy,size,align="center",parent=None,style=None,label="",text_align="center"):
        """create a text widget with size and position specified by xy, size and align
        it will have parent as a containing widget or will be placed directly on screen if parent is None
        use style to specify button color, activated button color, text color and font
        label: text to display on the button
        text_align: alignment of the text; one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright       
        """
        super(StaticText,self).__init__(xy,size,align,parent,style)
        self.label = label
        self.text_align = text_align
        
    def draw(self):
        pos = _xy_from_align(self.text_align,self.size)
        self.fill(self.style.bg_color)
        self.text(self.label, 
                  xy=pos, 
                  color=self.style.statictext_color, 
                  align = self.text_align, 
                  font=self.style.statictext_font, 
                  font_size=self.style.statictext_font_size)
