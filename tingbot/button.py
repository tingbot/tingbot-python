import time
import threading

from .utils import CallbackList
from .run_loop import once

event_types = ['press','long_press','down','up']
long_click_time = 1.0

class Button(object):
    def __init__(self):
        self.callbacks = {x:CallbackList() for x in event_types}
        self.was_pressed = False
        self.actions = []
        self.pressed = False
        self.down_time = 0
        self.click_count = 0
        self.lock = threading.Lock()
        
    def add_action(self,action):
        self.lock.acquire()
        self.actions.append(action)
        self.lock.release()

    def action(self,action):
        if action=="down":
            self.down_time = time.time()
            self.click_count += 1
            self.pressed_click_count = self.click_count
            once(seconds=long_click_time)(lambda: self.long_press(self.click_count))
        if action=="up":
            if (time.time()-self.down_time)>long_click_time:
                if self.pressed_click_count==self.click_count:
                    #our requested timer has not fired - main event loop must be busy
                    self.click_count +=1 #stops double fire when timer does run...
                    self.add_action('long_press')
            else:
                self.add_action('press')
                self.click_count +=1  
        self.add_action(action)
        
    def long_press(self,click_count):
        #do nothing if click_counts do not match as means something has happened in the meantime.
        if self.click_count==click_count:
            self.add_action('long_press')
            self.click_count += 1
            

    def run_callbacks(self):
        self.lock.acquire()
        for x in self.actions:
            self.callbacks[x]()
        self.actions = []
        self.lock.release()


buttons = {
    'left': Button(),
    'right': Button(),
    'midleft': Button(),
    'midright': Button(),
}

class press(object):
    def __init__(self, button_name, event_type="down"):
        ensure_setup()

        if button_name not in buttons:
            raise ValueError('Unknown button name "%s"' % button_name)
        
        self.button = buttons[button_name]

        if button_type not in press_types:
            raise ValueError('Unknown event type "%s' % event_type)
        self.event_type = event_type
        
    def __call__(self, f):
        self.button.callbacks[event_type].add(f)
        return f

is_setup = False

def ensure_setup():
    global is_setup
    if not is_setup:
        setup()
    is_setup = True


def setup():
    from platform_specific import register_button_callback
    register_button_callback(button_callback)

    from .run_loop import main_run_loop
    main_run_loop.add_wait_callback(wait)

def button_callback(button_index, action):
    button_names = ('left', 'midleft', 'midright', 'right')
    button_name = button_names[button_index]
    button = buttons[button_name]

    button.press(action)

def wait():
    for button in buttons.values():
        button.run_callbacks()
