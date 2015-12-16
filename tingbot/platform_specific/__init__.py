import platform
use_wrapper= False

def is_tingbot():
    """return True if running as a tingbot. We can update this function to be more smart in future"""
    return platform.machine().startswith('armv71')

def get_button_callback():
    raise TypeError("get_button_callback should be imported if using on anything which is not Mac or Tingbot")

if platform.system() == 'Darwin':
    from osx import fixup_env, fixup_window, register_button_callback
elif is_tingbot():
    from pi import fixup_env, fixup_window, register_button_callback
else:
    use_wrapper = True
    from linux import fixup_env, fixup_window, register_button_callback, get_button_callback

