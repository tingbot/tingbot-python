import sys, operator, time, traceback, Queue
from .utils import Struct, CallbackList, deprecated_callable
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

class after(object):
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.period = (hours * 60 + minutes) * 60 + seconds

    def __call__(self, f):
        create_timer(action=f, period=self.period, repeating=False)
        return f

once = deprecated_callable(
    after,
    name='once',
    version='1.1.1',
    message='once has been renamed to \'after\'. Use \'after\' instead.')

class RunLoop(object):

    _call_after_queue = Queue.Queue()

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
            if len(self.timers) > 0:
                try:
                    self._wait(lambda: self.timers[-1].next_fire_time)
                except Exception as e:
                    self._error(e)
                    continue

                next_timer = self.timers.pop()

                if next_timer.active:
                    before_action_time = time.time()

                    try:
                        self._before_action_callbacks()
                        next_timer.run()
                        self._after_action_callbacks()
                    except Exception as e:
                        self._error(e)
                    finally:
                        if next_timer.repeating and next_timer.active:
                            next_timer.next_fire_time = before_action_time + next_timer.period
                            self.schedule(next_timer)
            else:
                try:
                    wait_delay = time.time() + 0.1
                    self._wait(lambda: wait_delay)
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
        
    @classmethod
    def call_after(cls, func):
        cls._call_after_queue.put(func)

    @classmethod
    def empty_call_after_queue(cls):
        while True:
            try:
                func = cls._call_after_queue.get_nowait()
                func()
                cls._call_after_queue.task_done()
            except Queue.Empty:
                break

        
    def _wait(self, until):
        self._wait_callbacks()

        while time.time() < until():
            if not self._call_after_queue.empty():
                self.empty_call_after_queue()
            time.sleep(0.001)
            self._wait_callbacks()

    def _error(self, exception):
        sys.stderr.write('\n' + str(exception) + '\n')

        traceback.print_exc()

        error.error_screen(sys.exc_info())
        time.sleep(0.5)


main_run_loop = RunLoop(event_handler=EventHandler())
