import platform, os

def is_tingbot():
    """
    Return True if running as a tingbot.
    """
    # TB_RUN_ON_LCD is an environment variable set by tbprocessd when running tingbot apps.
    return 'TB_RUN_ON_LCD' in os.environ

if platform.system() == 'Darwin':
    from osx import fixup_env, create_main_surface, register_button_callback
elif is_tingbot():
    from tingbot import fixup_env, create_main_surface, register_button_callback
else:
    from sdl_wrapper import fixup_env, create_main_surface, register_button_callback
