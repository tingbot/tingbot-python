import unittest
from tingbot.button import Button


class ButtonTestCase(unittest.TestCase):
    def setUp(self):
        self.button = Button()

    def assertActions(self, action_types):
        self.assertEqual(action_types, [a.type for a in self.button.actions])

    def testPress(self):
        self.button.add_event('down', timestamp=1)
        self.button.add_event('up', timestamp=1.5)
        self.button.process_events(time=2)
        self.assertActions(['down', 'up', 'press'])

    def testHold(self):
        self.button.add_event('down', timestamp=1)
        self.button.add_event('up', timestamp=3)
        self.button.process_events(3.1)
        self.assertActions(['down', 'hold', 'up'])

    def testIncrementalHold(self):
        self.button.add_event('down', timestamp=1)
        self.button.process_events(time=1.1)
        self.assertActions(['down'])

        self.button.process_events(time=2.1)
        self.assertActions(['down', 'hold'])

        self.button.add_event('up', timestamp=3)
        self.button.process_events(time=3.1)
        self.assertActions(['down', 'hold', 'up'])
        
    def testRepeatedPress(self):
        self.button.add_event('down', timestamp=1)
        self.button.add_event('up', timestamp=1.5)
        self.button.add_event('down', timestamp=3.5)
        self.button.add_event('up', timestamp=4.0)
        self.button.process_events(time=4.1)
        self.assertActions(['down', 'up', 'press','down', 'up', 'press'])
        
    def testRepeatedQuickPress(self):
        self.button.add_event('down', timestamp=1)
        self.button.add_event('up', timestamp=1.5)
        self.button.add_event('down', timestamp=1.6)
        self.button.add_event('up', timestamp=2.2)
        self.button.process_events(time=4.1)
        self.assertActions(['down', 'up', 'press','down', 'up', 'press'])
