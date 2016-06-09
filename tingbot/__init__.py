import warnings
try:
    import pygame
except ImportError:
    print 'Failed to import pygame'
    print '-----------------------'
    print ''
    print 'tingbot-python requires pygame. Please download and install pygame 1.9.1'
    print 'or later from http://www.pygame.org/download.shtml'
    print ''
    print "If you're using a virtualenv, you should make the virtualenv with the "
    print "--system-site-packages flag so the system-wide installation is still "
    print "accessible."
    print ''
    print '-----------------------'
    print ''
    raise

from . import platform_specific, input, quit

from .graphics import screen, Surface, Image
from .run_loop import main_run_loop, every, once
from .input import touch
from .button import press,left_button,midleft_button,midright_button,right_button
from .web import webhook
from .tingapp import app

#enable deprecation warnings
warnings.filterwarnings("once",".*",DeprecationWarning)

platform_specific.fixup_env()
quit.fixup_sigterm_behaviour()

def run(loop=None):
    if loop is not None:
        every(seconds=1.0/30)(loop)

    main_run_loop.add_after_action_callback(screen.update_if_needed)

    main_run_loop.add_wait_callback(input.poll)
    # in case screen updates happen in input.poll...
    main_run_loop.add_wait_callback(screen.update_if_needed)

    main_run_loop.run()

__all__ = [
    'run', 'screen', 'Surface', 'Image', 'every', 'touch', 'press', 'button', 'webhook',
    'left_button', 'midleft_button', 'midright_button', 'right_button',
]
__author__ = 'Joe Rickerby'
__email__ = 'joerick@mac.com'
__version__ = '0.4.0'
