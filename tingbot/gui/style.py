defaults = {
    'bg_color'    :'black',
    'button_color':'blue',
    'pressed_button_color':'aqua',
    'button_text_color':'white',
    'button_text_font':None, #use default font
    'button_text_font_size':32,
    'scrollbar_width':15,
    'slider_line_color':(40,40,40),
    'slider_handle_color':(200,200,200)
}

class Style(object):
    def __init__(self,**kwargs):
        self.__dict__.update(defaults)
        #update based on kwargs, check for invalid args also and throw error
        for arg,value in kwargs.items():
            if arg in defaults:
                self.__dict__[arg] = value
            else:
                raise TypeError("__init__() got an unexpected keyword argument '%s'" % arg)
   
default_style = Style()

def get_default_style():
    return default_style
