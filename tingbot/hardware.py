import pyudev
import socket

udev_context = pyudev.Context()

def count_peripherals(name):
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

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addr = s.getsockname()[0]
    except IOError:
        ip_addr = None
    finally:
        s.close()
    return ip_addr
