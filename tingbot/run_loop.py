import sys, operator, time, traceback
from .utils import Struct, CallbackList
from . import error

class Timer(Struct):
    pass


class every(object):
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.period = (hours * 60 + minutes) * 60 + seconds

    def __call__(self, f):
        timer = Timer(name=f.__name__, action=f, period=self.period, repeating=True, next_fire_time=None)

        main_run_loop.schedule(timer)

        return f

class once(object):
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.period = (hours * 60 + minutes) * 60 + seconds

    def __call__(self, f):
        timer = Timer(action=f, period=self.period, repeating=False, next_fire_time=None)

        main_run_loop.schedule(timer)

        return f

class RunLoop(object):
    def __init__(self):
        self.timers = []
        self._wait_callbacks = CallbackList()
        self._before_action_callbacks = CallbackList()
        self._after_action_callbacks = CallbackList()
        self.current_timers = []

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

    def remove_timer(self, action):
        """remove a timer from the list"""
        if self.current_timers:
            current_action = self.current_timers[-1].action
        else:
            current_action = None
        if action != current_action and action not in [x.action for x in self.timers]:
            raise ValueError("Timer not found")
        if current_action == action:  # account for being called from the timer requesting being stopped
            self.current_timers[-1].repeating = False
        self.timers[:] = [x for x in self.timers if x.action != action]

    def run(self):
        self.running = True
        while self.running:
            start_time = time.time()

            if len(self.timers) > 0:
                next_timer = self.timers.pop()
                self.current_timers.append(next_timer)

                try:
                    self._wait(next_timer.next_fire_time)

                    self._before_action_callbacks()
                    next_timer.action()
                    self._after_action_callbacks()
                except Exception as e:
                    self._error(e)
                finally:
                    if next_timer.repeating:
                        next_timer.next_fire_time = start_time + next_timer.period
                        self.schedule(next_timer)
                self.current_timers.pop()
            else:
                try:
                    self._wait(start_time + 0.1)
                except Exception as e:
                    self._error(e)
        self.running = True  # prevent an outer loop from stopping if inner loop has been stopped

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


main_run_loop = RunLoop()
