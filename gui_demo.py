#!/usr/bin/python

from datetime import datetime
from tingbot import press,touch,screen,gui,run

@press('right')
def right():
    screen.fill(color="blue")
    
@press('left')
def right():
    screen.fill(color="teal")
    
@press('midright')
def right():
    screen.fill(color="red")
    
@press('midleft')
def right():
    screen.fill(color="maroon")
    
@touch()
def draw(xy):
    #screen.rectangle(xy=xy,size=(5,5),color="white")
    pass
    
def loop():
    tm = datetime.now().strftime("%X")
    screen.rectangle((0,220),(320,20),align="topleft",color="navy")
    screen.text(tm,align="bottom",font_size=16,color="white")
    
       
def slider_cb(value):
    print "Slider value: %g" % value

def cb(pressed):
    panel.fill('black')
    panel.visible = pressed
    panel.update(downwards=True)
    print "button pressed"
    
def cb2():
    print "but2 pressed"

style = gui.get_default_style()
#style.slider_handle_color="red"
screen.fill(color="black")
panel = gui.ScrollArea((0,100),(320,120),align="topleft",canvas_size=(640,240))
slider = gui.Slider((0,0),(200,20),align="topleft",min_val=100,max_val=200,change_callback=slider_cb,parent=panel.scrolled_area)

but = gui.ToggleButton((55,55),(90,90),but_text="Panel",callback=cb)
but.pressed = True
but.update()
but2 = gui.Button((400,120),(100,100),align="topleft",parent=panel.scrolled_area,callback = cb2)
panel.update(downwards=True)
run(loop)
