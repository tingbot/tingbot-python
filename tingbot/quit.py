import sys, signal
import pygame

def fixup_sigterm_behaviour():
    '''
    SDL registers its own signal handler for SIGTERM, which pushes a SDL_QUIT event to the event
    loop, instead of killing the process right away. This is a problem for us, because when using
    the fbcon drivers, the process activates and locks a virtual terminal which survives after the
    process dies. We need to ensure that the process cleans up this virtual terminal, otherwise the
    Tingbot needs a reboot.

    We do this by calling the cleanup and exiting straight away on SIGTERM.
    '''

    # this installs the 'bad' SIGTERM handler
    pygame.display.init()

    def quit_handler(sig, frame):
        pygame.quit()
        sys.exit(128 + sig)

    # this overwrites it with our SIGTERM handler
    signal.signal(signal.SIGTERM, quit_handler)
