import unittest
import subprocess
import json

import tingbot.hardware as hardware

class FakeDevice(object):
    def __init__(self, items):
        self.properties = items

class FakeContext(object):
    def __init__(self):
        with open("tests/peripherals.json", "r") as fp:
            devices = json.load(fp)
        self.devices = [FakeDevice(x) for x in devices]

    def list_devices(self, **kwargs):
        devs = []
        for k, v in kwargs.items():
            devs.extend([x for x in self.devices if k in x.properties])
        return devs

class TestPeripherals(unittest.TestCase):
    def setUp(self):
        hardware.udev_context = FakeContext()

    def test_count_peripherals(self):
        self.assertEqual(hardware.count_peripherals('SOMETHING RANDOM'), 0)
        self.assertEqual(hardware.count_peripherals('ID_INPUT_KEYBOARD'), 2)
        self.assertEqual(hardware.count_peripherals('ID_INPUT_MOUSE'), 1)
        self.assertEqual(hardware.count_peripherals('ID_INPUT_JOYSTICK'), 0)

    def test_mouse_attached(self):
        self.assertTrue(hardware.mouse_attached())

    def test_keyboard_attached(self):
        self.assertTrue(hardware.keyboard_attached())

    def test_joystick_attached(self):
        self.assertFalse(hardware.joystick_attached())

class TestNetwork(unittest.TestCase):
    def setUp(self):
        self.old_check_output = subprocess.check_output
        subprocess.check_output = self.generate_iw_config
        self.connected = True
        self.adapter = True

    def tearDown(self):
        subprocess.check_output = self.old_check_output

    def generate_iw_config(self, dummy):
        if self.adapter:
            if self.connected:
                return """
wlan0     IEEE 802.11bgn  ESSID:"wifi_test_cell"  
          Mode:Managed  Frequency:2.437 GHz  Access Point: 00:11:22:33:44:55   
          Bit Rate=150 Mb/s   Tx-Power=16 dBm   
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
          Link Quality=64/70  Signal level=-36 dBm  
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:1  Invalid misc:331   Missed beacon:0        
"""
            else:
                return """
wlan0     IEEE 802.11bgn  ESSID:off/any  
          Mode:Managed  Access Point: Not-Associated   Tx-Power=15 dBm   
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
"""
        else:
            raise subprocess.CalledProcessError(-1, "command failed")

    def test_get_wifi_cell_connected(self):
        self.connected = True
        cell = hardware.get_wifi_cell()
        self.assertEqual(cell.ssid, "wifi_test_cell")
        self.assertEqual(cell.link_quality, 64)
        self.assertEqual(cell.signal_level, -36)

    def test_get_wifi_cell_disconnected(self):
        self.connected = False
        cell = hardware.get_wifi_cell()
        self.assertIsNone(cell.ssid)
        self.assertIsNone(cell.link_quality)
        self.assertIsNone(cell.signal_level)

    def test_get_wifi_cell_no_adapter(self):
        self.adapter = False
        cell = hardware.get_wifi_cell()
        self.assertIsNone(cell)
