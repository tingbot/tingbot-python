import os


def fixup_env():
    import evdev
    os.environ["SDL_FBDEV"] = "/dev/fb1"

    mouse_path = None

    for device_path in evdev.list_devices():
        device = evdev.InputDevice(device_path)
        if device.name == "ADS7846 Touchscreen":
            mouse_path = device_path

    if mouse_path:
        os.environ["SDL_MOUSEDRV"] = "TSLIB"
        os.environ["SDL_MOUSEDEV"] = mouse_path
    else:
        print 'Mouse input device not found in /dev/input. Touch support not available.'

def create_main_surface():
    import pygame
    pygame.init()
    surface = pygame.display.set_mode((320, 240))
    import pygame.mouse
    pygame.mouse.set_visible(0)
    return surface

button_callback = None

def register_button_callback(callback):
    global button_callback
    ensure_button_setup()
    button_callback = callback

button_setup_done = False

def ensure_button_setup():
    global button_setup_done
    if not button_setup_done:
        button_setup()
    button_setup_done = True

button_pins = (11, 16, 18, 12)
button_pin_to_index = {
    11: 0,
    16: 1,
    18: 2,
    12: 3
}

def button_setup():
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    for button_pin in button_pins:
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(button_pin, GPIO.BOTH, bouncetime=200, callback=GPIO_callback)

button_previous_states = {
    0: 'up',
    1: 'up',
    2: 'up',
    3: 'up',
}

def GPIO_callback(pin):
    import RPi.GPIO as GPIO

    button_index = button_pin_to_index[pin]
    state = 'down' if GPIO.input(pin) else 'up'

    if button_callback is not None:
        # there is a race condition between the kernel seeing the change in the GPIO and
        # the above code running - so the GPIO input might have changed since then. In this case,
        # we can miss button presses. But we know _something_ happened on the GPIO, so we can at
        # least synthesise a 'toggle' event - this will be right most of the time.
        if state == button_previous_states[button_index]:
            toggle_state = 'up' if (state == 'down') else 'down'
            button_callback(button_index, state)

        button_callback(button_index, state)

    button_previous_states[button_index] = state
