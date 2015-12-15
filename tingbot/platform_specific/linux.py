def fixup_window():
    pass

def fixup_env():
    pass
    
button_callback = None


def register_button_callback(callback):
    '''
    callback(button_index, action)
        button_index is a zero-based index that identifies which button has been pressed
        action is either 'down', or 'up'.

    The callback might not be called on the main thread.

    Currently only 'down' is implemented.
    '''
    global button_callback
    button_callback = callback
    
def get_button_callback():
    global button_callback
    return button_callback
