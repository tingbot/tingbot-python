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

button_pins = (17, 23, 24, 18)
button_pin_to_index = {
    17: 0,
    23: 1,
    24: 2,
    18: 3
}

def button_setup():
    import wiringpi

    wiringpi.wiringPiSetupGpio()

    for button_pin in button_pins:
        wiringpi.pinMode(button_pin, wiringpi.INPUT)
        wiringpi.wiringPiISR(button_pin, wiringpi.INT_EDGE_BOTH, GPIO_callback)

button_previous_states = [0, 0, 0, 0]

def GPIO_callback():
    import wiringpi
    global button_previous_states

    button_states = [wiringpi.digitalRead(pin) for pin in button_pins]

    for button_index, (old, new) in enumerate(zip(button_previous_states, button_states)):
        if old != new:
            button_callback(button_index, 'down' if (new == 1) else 'up')

    button_previous_states = button_states
