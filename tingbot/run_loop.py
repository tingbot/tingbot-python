import sys, operator, time, traceback
from .utils import Struct, CallbackList
from . import error
from .graphics import screen
from .input import EventHandler

class Timer(Struct):
    def __init__(self, **kwargs):
        self.active = True
        super(Timer, self).__init__(**kwargs)

    def stop(self):
        self.active = False

    def run(self):
        if self.active:
            self.action()

def create_timer(action, hours=0, minutes=0, seconds=0, period=0, repeating=True):
    if period == 0:
        period = (hours * 60 + minutes) * 60 + seconds
    timer = Timer(action=action, period=period, repeating=repeating, next_fire_time=None)
    main_run_loop.schedule(timer)
    return timer

class every(object):
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.period = (hours * 60 + minutes) * 60 + seconds

    def __call__(self, f):
        create_timer(action=f, period=self.period, repeating=True)
        return f

class once(object):
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.period = (hours * 60 + minutes) * 60 + seconds

    def __call__(self, f):
        create_timer(action=f, period=self.period, repeating=False)
        return f

class RunLoop(object):

    def __init__(self, event_handler=None):
        self._wait_callbacks = CallbackList()
        self._before_action_callbacks = CallbackList()
        self._after_action_callbacks = CallbackList()
        self.timers = []

        # add screen update callbacks
        self.add_after_action_callback(screen.update_if_needed)

        if event_handler:
            self.add_wait_callback(event_handler.poll)
            # in case screen updates happen in input.poll...
            self.add_wait_callback(screen.update_if_needed)

    def schedule(self, timer):
        if timer.next_fire_time is None:
            if timer.repeating:
                # if it's repeating, and it's never been called, call it now
                timer.next_fire_time = 0
            else:
                # call it after 'period'
                timer.next_fire_time = time.time() + timer.period

        self.timers.append(timer)
        self.timers.sort(key=operator.attrgetter('next_fire_time'), reverse=True)

    def run(self):
        self.running = True
        while self.running:
            start_time = time.time()

            if len(self.timers) > 0:
                next_timer = self.timers.pop()
                if next_timer.active:
                    try:
                        self._wait(next_timer.next_fire_time)

                        self._before_action_callbacks()
                        next_timer.run()
                        self._after_action_callbacks()
                    except Exception as e:
                        self._error(e)
                    finally:
                        if next_timer.repeating and next_timer.active:
                            next_timer.next_fire_time = start_time + next_timer.period
                            self.schedule(next_timer)
            else:
                try:
                    self._wait(start_time + 0.1)
                except Exception as e:
                    self._error(e)

    def stop(self):
        self.running = False

    def add_wait_callback(self, callback):
        self._wait_callbacks.add(callback)

    def add_before_action_callback(self, callback):
        self._before_action_callbacks.add(callback)

    def add_after_action_callback(self, callback):
        self._after_action_callbacks.add(callback)

    def _wait(self, until):
        self._wait_callbacks()

        while time.time() < until:
            time.sleep(0.001)
            self._wait_callbacks()

    def _error(self, exception):
        sys.stderr.write('\n' + str(exception) + '\n')

        traceback.print_exc()

        error.error_screen(sys.exc_info())
        time.sleep(0.5)


main_run_loop = RunLoop(event_handler=EventHandler())
