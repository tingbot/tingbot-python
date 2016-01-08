#!/usr/bin/python
from tingbot import screen,gui,run

    
def loop():
    pass    
       
def print_text(text):       
    screen.rectangle((160,230),(320,20),'black')
    screen.text(text,(160,230),font_size=16)
       
def slider_cb(value):
    print_text("Slider value: %d" % int(value))

def value_callback(name,value):
    print_text(name + " value: " + str(value))

def pressed(name=""):
    print_text("%s pressed" % name)
    

style = gui.get_default_style()
style.slider_handle_color="aqua"
screen.fill(color="black")

but1 = gui.Button((50,30),(90,50),label="Button",callback=lambda: pressed("Button"))
but1.update()
but2 = gui.ToggleButton((150,30),(90,50),label="Toggle",callback = lambda x: value_callback("Toggle Button",x))
but2.update()

panel = gui.ScrollArea((0,60),(320,160),align="topleft",canvas_size=(640,240))

slider = gui.Slider((0,0),(200,20),align="topleft",
                    min_val=100,
                    max_val=200,
                    change_callback=slider_cb,parent=panel.scrolled_area)

chk1 = gui.CheckBox((0,30),(200,20),align="topleft",
                    parent=panel.scrolled_area, 
                    label="Checkbox 1", 
                    callback = lambda x: value_callback("Checkbox 1",x))
chk2 = gui.CheckBox((0,60),(200,20),align="topleft",
                    parent=panel.scrolled_area, 
                    label="Checkbox 2", 
                    callback = lambda x: value_callback("Checkbox 2",x))

group = gui.RadioGroup(callback=value_callback)
radio1 = gui.RadioButton((0,90),(200,20),align="topleft",
                         parent=panel.scrolled_area,
                         label="Radiobutton 1",
                         value=1,
                         group=group)
radio2 = gui.RadioButton((0,120),(200,20),align="topleft",
                         parent=panel.scrolled_area,
                         label="Radiobutton 2",
                         value=2,
                         group=group)
radio3 = gui.RadioButton((0,150),(200,20),align="topleft",
                         parent=panel.scrolled_area,
                         label="Radiobutton 3",
                         value=3,
                         group=group)
                         
panel.update(downwards=True)
run(loop)
