import platform

def is_tingbot():
    """return True if running as a tingbot. We can update this function to be more smart in future"""
    return platform.machine().startswith('armv71')

if platform.system() == 'Darwin':
    from osx import fixup_env, fixup_window, register_button_callback
elif is_tingbot():
    from pi import fixup_env, fixup_window, register_button_callback
else:
    from sdl_wrapper import fixup_env, fixup_window, register_button_callback

