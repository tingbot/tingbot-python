import unittest
import time
from tests.utils import TimeControlCase
from tingbot.button import Button
import tingbot.button

class TestButton(TimeControlCase):
    def test_creation(self):
        button = Button()
    
    def test_simple_press(self):
        button = Button()
        button.action("down")
        button.action("up")
        self.assertEqual(button.actions,["down","press","up"])
        
    def test_basic_long_press(self):
        button = Button()
        button.action("down")
        time.time.tm = 1000.1 +tingbot.button.long_click_time
        button.long_press(button.click_count)
        button.action("up")
        self.assertEqual(button.actions,["down","long_press","up"])
        
    def test_interrupted_long_press(self):
        button = Button()
        button.action("down")
        click_count = button.click_count
        time.time.tm = 1000.1 +tingbot.button.long_click_time
        button.action("up")
        button.long_press(click_count)
        self.assertEqual(button.actions,["down","long_press","up"])

    def test_repeated_presses(self):
        button = Button()
        button.action("down")
        button.action("up")
        time.time.tm = 1000.5 + tingbot.button.long_click_time
        button.action("down")
        button.action("up")
        self.assertEqual(button.actions,["down","press","up","down","press","up"])
        
    def test_close_repeated_presses(self):    
        button = Button()
        button.action("down")
        button.action("up")
        time.time.tm = 1000.5
        button.action("down")
        button.action("up")
        self.assertEqual(button.actions,["down","press","up","down","press","up"])
    
