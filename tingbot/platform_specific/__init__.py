import sys, os

def is_running_on_tingbot():
    """
    Return True if running as a tingbot.
    """
    # TB_RUN_ON_LCD is an environment variable set by tbprocessd when running tingbot apps.
    return 'TB_RUN_ON_LCD' in os.environ

def no_op(*args, **kwargs):
    pass

def no_op_returning(return_value):
    def inner(*args, **kwargs):
        return return_value
    return inner

# set fallback functions (some of these will be replaced by the real versions below)
set_backlight = no_op
mouse_attached = no_op_returning(True)
keyboard_attached = no_op_returning(True)
joystick_attached = no_op_returning(False)
get_wifi_cell = no_op_returning(None)
setup_audio = no_op

if sys.platform == 'darwin':
    from osx import fixup_env, create_main_surface, register_button_callback
elif is_running_on_tingbot():
    from tingbot import (fixup_env, create_main_surface, register_button_callback,
                         set_backlight, mouse_attached, keyboard_attached, joystick_attached,
                         get_wifi_cell, setup_audio)
else:
    from sdl_wrapper import fixup_env, create_main_surface, register_button_callback
