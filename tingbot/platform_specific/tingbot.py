import os, subprocess, re
from ..utils import only_call_once

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

###########
# Buttons #
###########

button_callback = None

def register_button_callback(callback):
    global button_callback
    ensure_button_setup()
    button_callback = callback

button_pins = (17, 23, 24, 14)

@only_call_once
def ensure_wiringpi_setup():
    import wiringpi
    wiringpi.wiringPiSetupGpio()

@only_call_once
def ensure_button_setup():
    import wiringpi

    ensure_wiringpi_setup()

    for button_pin in button_pins:
        wiringpi.pinMode(button_pin, wiringpi.INPUT)
        wiringpi.wiringPiISR(button_pin, wiringpi.INT_EDGE_BOTH, GPIO_callback)

button_previous_states = [0, 0, 0, 0]

def GPIO_callback():
    import wiringpi
    global button_previous_states

    button_states = [wiringpi.digitalRead(pin) for pin in button_pins]

    for button_index, (old, new) in enumerate(zip(button_previous_states, button_states)):
        if old != new and button_callback is not None:
            button_callback(button_index, 'down' if (new == 1) else 'up')

    button_previous_states = button_states

#############
# Backlight #
#############

@only_call_once
def ensure_backlight_setup():
    subprocess.check_call(['gpio', '-g', 'mode', '18', 'pwm'])
    subprocess.check_call(['gpio', '-g', 'pwmr', '65536'])

def set_backlight(brightness):
    '''
    Sets the backlight of the screen to `brightness`. `brightness` is a number from 0 to 100.
    '''
    ensure_backlight_setup()

    if brightness <= 4:
        # linear scaling from 0 to 4
        value = brightness
    else:
        # cubic scaling from 4 to 100
        value = 65536 * (brightness/100.0)**3

    subprocess.check_call(['gpio', '-g', 'pwm', '18', str(value)])

###############
# Peripherals #
###############

udev_context = None

def ensure_udev_setup():
    global udev_context
    if udev_context is None:
        import pyudev
        udev_context = pyudev.Context()

def count_peripherals(name):
    ensure_udev_setup()

    args = {name: 1}
    devices = udev_context.list_devices(**args)
    unique_devices = set(x.properties['ID_PATH'] for x in devices)
    return len(unique_devices)

def mouse_attached():
    return count_peripherals('ID_INPUT_MOUSE') > 0

def keyboard_attached():
    return count_peripherals('ID_INPUT_KEYBOARD') > 0

def joystick_attached():
    return count_peripherals('ID_INPUT_JOYSTICK') > 0

###########
# Network #
###########

class WifiCell():
    attribute_patterns = {
        'ssid': r'ESSID:"(.+)"',
        'link_quality': r'Link Quality\s*=\s*(-?\d+)',
        'signal_level': r'Signal Level\s*=\s*(-?\d+)'
        }

    def __init__(self, data):
        for attr, pattern in self.attribute_patterns.items():
            match = re.search(pattern, data, flags=re.I)
            if match:
                if attr in ('ssid',):
                    setattr(self, attr, match.group(1))
                else:
                    setattr(self, attr, int(match.group(1)))
            else:
                setattr(self, attr, None)

def get_wifi_cell():
    """
    Returns the current wifi cell (if attached)
    Returns "" if not currently attached
    Returns None if no wifi adapter present
    """
    try:
        iw_data = subprocess.check_output(['iwconfig', 'wlan0'])
    except subprocess.CalledProcessError:
        # wlan0 not found
        return None
    return WifiCell(iw_data)

#########
# Audio #
#########

def setup_audio():
    subprocess.check_call(['tbsetupaudio'])
