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


class RunLoopExit(BaseException):
    pass


class RunLoop(object):
    def __init__(self):
        self.timers = []
        self._wait_callbacks = CallbackList()
        self._before_action_callbacks = CallbackList()
        self._after_action_callbacks = CallbackList()

    def schedule(self, timer):
        if timer.next_fire_time is None:
            if timer.repeating:
                # if it's repeating, and it's never been called, call it now
                timer.next_fire_time = 0
            else:
                # call it after 'period'
                timer.next_fire_time = time.time() + timer.period

        self.timers.append(timer)
        self._sort_timers()

    def remove_timer(self, action):
        '''remove a timer from the run loop'''
        if action not in [x.action for x in self.timers]:
            raise ValueError("Timer not found")

        self.timers[:] = [x for x in self.timers if x.action != action]

    def run(self, until=lambda: False):
        try:
            while True:
                if len(self.timers) > 0:
                    next_timer = self.timers[0]

                    try:
                        self._wait(next_timer.next_fire_time, until)
                    except Exception as e:
                        self._error(e)
                        continue

                    before_action_time = time.time()

                    try:
                        self._before_action_callbacks()
                        next_timer.action()
                        self._after_action_callbacks()
                    except Exception as e:
                        self._error(e)
                    finally:
                        if next_timer.repeating:
                            next_timer.next_fire_time = before_action_time + next_timer.period
                            self._sort_timers()
                        else:
                            self.timers.remove(next_timer)
                else:
                    try:
                        self._wait(time.time() + 0.1, until)
                    except Exception as e:
                        self._error(e)
        except RunLoopExit:
            pass

    def add_wait_callback(self, callback):
        self._wait_callbacks.add(callback)

    def add_before_action_callback(self, callback):
        self._before_action_callbacks.add(callback)

    def add_after_action_callback(self, callback):
        self._after_action_callbacks.add(callback)

    def _sort_timers(self):
        '''
        Sorts the timers list so that the next time to fire is at the top of the list.
        Should be called after timers are added, or next_fire_time is changed on any timer.
        '''
        self.timers.sort(key=operator.attrgetter('next_fire_time'))

    def _wait(self, until_time, until_func):
        self._wait_callbacks()

        while time.time() < until_time:
            if until_func() == True:
                raise RunLoopExit
            time.sleep(0.001)
            self._wait_callbacks()

    def _error(self, exception):
        sys.stderr.write('\n' + str(exception) + '\n')

        traceback.print_exc()

        error.error_screen(sys.exc_info())
        time.sleep(0.5)


main_run_loop = RunLoop()
