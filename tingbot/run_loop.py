import sys, operator, time, traceback
from .utils import Struct, CallbackList
from . import error

class Timer(Struct):
    def __init__(self, **kwargs):
        self.active = True
        super(Timer, self).__init__(**kwargs)

    def stop(self):
        self.active = False

    def run(self):
        if self.active:
            self.action()

class every(object):
    def __init__(self, hours=0, minutes=0, seconds=0, background=False):
        self.period = (hours * 60 + minutes) * 60 + seconds
        self.background = background

    def __call__(self, f):
        create_timer(action=f, period=self.period, repeating=True, background=self.background)
        return f

def create_timer(action, hours=0, minutes=0, seconds=0, period=0, repeating=True, background=False):
    if period == 0:
        period = (hours * 60 + minutes) * 60 + seconds
    timer = Timer(action=action, period=period, repeating=repeating, next_fire_time=None, background=background)
    RunLoop.schedule(timer)
    return timer


class once(object):
    def __init__(self, hours=0, minutes=0, seconds=0, background=False):
        self.period = (hours * 60 + minutes) * 60 + seconds
        self.background = background

    def __call__(self, f):
        create_timer(action=f, period=self.period, repeating=False, background=self.background)
        return f

class RunLoop(object):

    stack = []

    def __init__(self, parent=None):
        if parent:
            self.timers = [x for x in parent.timers if x.background]
            self._wait_callbacks = parent._wait_callbacks.copy()
            self._before_action_callbacks = parent._before_action_callbacks.copy()
            self._after_action_callbacks = parent._after_action_callbacks.copy()
        else:
            self.timers = []
            self._wait_callbacks = CallbackList()
            self._before_action_callbacks = CallbackList()
            self._after_action_callbacks = CallbackList()
        self.stack.append(self)

    @classmethod
    def spawn(cls):
        if cls.stack:
            run_loop = cls(cls.stack[-1])
        else:
            run_loop = cls()
        return run_loop

    @classmethod
    def schedule(cls, timer):
        cls.stack[-1]._schedule(timer)

    def _schedule(self, timer):
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
                            self._schedule(next_timer)
            else:
                try:
                    self._wait(start_time + 0.1)
                except Exception as e:
                    self._error(e)
        self.running = True  # prevent an outer loop from stopping if inner loop has been stopped
        self.stack.pop()  # remove this run_loop from the stack

    @classmethod
    def stop(cls):
        cls.stack[-1].running = False

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
