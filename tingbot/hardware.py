import socket
import subprocess
import re
import pyudev

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
    match = re.search(r'ESSID:"(.+)"', iw_data)
    if match:
        return match.group(1)
    else:
        return ""
