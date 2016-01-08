defaults = {
    'bg_color'    :'black',
    
    'statictext_color':'white',
    'statictext_font': None,
    'statictext_font_size': 16,


    'button_color':(0,0,180),
    'button_pressed_color':(0,0,250),
    'button_rounding':10,
    'button_text_color':'white',
    'button_text_font':None, #use default font
    'button_text_font_size':24,
    
    'checkbox_color':'red', #color of the checkbox when not pressed
    'checkbox_text_color': 'white',
    'checkbox_text_font': None, 
    'checkbox_text_font_size': 16,
    
    'radiobutton_color':'red', #color of the radiobutton when not pressed
    'radiobutton_text_color': 'white',
    'radiobutton_text_font': None, 
    'radiobutton_text_font_size': 16,
    
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
