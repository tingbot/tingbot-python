import time
import threading
import warnings
from collections import namedtuple
import Queue

from .utils import CallbackList

ButtonEvent = namedtuple('ButtonEvent', ('state', 'timestamp',))
ButtonAction = namedtuple('ButtonAction', ('type', 'timestamp',))

action_types = ['press', 'hold', 'down', 'up']


class Button(object):
    def __init__(self):
        self.event_queue = Queue.Queue()
        self.last_event = None
        self.hold_time = 1.0
        self.last_hold_check_time = 0
        self.callbacks = {x:CallbackList() for x in action_types}
        self.actions = []

    def process_events(self, time):
        while True:
            try:
                event = self.event_queue.get(block=False)
            except Queue.Empty:
                break

            self.fire_hold_if_due(event.timestamp)

            if event.state == 'down':
                self.fire(ButtonAction('down', timestamp=event.timestamp))
            elif event.state == 'up':
                self.fire(ButtonAction('up', timestamp=event.timestamp))

                # check to see if press should be fired
                if self.last_event.state == 'down':
                    press_duration = event.timestamp - self.last_event.timestamp

                    if press_duration < self.hold_time:
                        self.fire(ButtonAction('press', timestamp=event.timestamp))

            self.last_event = event

        self.fire_hold_if_due(time)

    def fire_hold_if_due(self, time):
        ''' check to see if the hold event needs to be fired '''

        if self.last_event and self.last_event.state == 'down':
            hold_trigger_time = self.last_event.timestamp + self.hold_time

            if self.last_hold_check_time < hold_trigger_time <= time:
                self.fire(ButtonAction('hold', timestamp=hold_trigger_time))

        self.last_hold_check_time = time

    def fire(self, action):
        self.actions.append(action)

    def run_callbacks(self):
        for action in self.actions:
            self.callbacks[action.type]()
        self.actions = []

    def add_event(self, action, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
        self.event_queue.put(ButtonEvent(action, timestamp))

    def add_callback(self, event, func):
        ensure_setup()
        self.callbacks[event].add(func)

    def __call__(self, f):
        print "calling"
        self.down(f)

    def down(self, f):
        self.add_callback('down', f)

    def up(self, f):
        self.add_callback('up', f)

    def press(self, f):
        self.add_callback('press', f)

    def hold(self, f):
        self.add_callback('hold', f)

# create buttons
button_names = ('left', 'midleft', 'midright', 'right')
buttons = {x:Button() for x in button_names}
left_button, midleft_button, midright_button, right_button = [buttons[x] for x in button_names]


is_setup = False

def ensure_setup():
    global is_setup
    if not is_setup:
        setup()
    is_setup = True

class press(object):
    def __init__(self, button):
        warnings.warn(
            'press is deprecated. Use <button_name>.down (or up, press, or hold) instead.',
            DeprecationWarning,
            stacklevel=2)
        self.button = buttons[button]

    def __call__(self, f):
        self.button.down(f)


def setup():
    from platform_specific import register_button_callback
    register_button_callback(button_callback)

    from .run_loop import main_run_loop
    main_run_loop.add_wait_callback(wait)

def button_callback(button_index, action):
    button_name = button_names[button_index]
    button = buttons[button_name]

    button.add_event(action)

def wait():
    for button in buttons.values():
        button.process_events(time.time())
        button.run_callbacks()
