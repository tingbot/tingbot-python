import socket
from . import platform_specific

mouse_attached = platform_specific.mouse_attached
keyboard_attached = platform_specific.keyboard_attached
joystick_attached = platform_specific.joystick_attached
get_wifi_cell = platform_specific.get_wifi_cell

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
