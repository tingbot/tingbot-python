import unittest
import time

class TimeHelper(object):
    def __init__(self):
        self.tm = 1000.0
    def __call__(self):
        return self.tm

class TimeControlCase(unittest.TestCase): 
    def setUp(self):
        mytime = TimeHelper()
        self.old_time = time.time
        time.time = mytime
        
    def tearDown(self):
        time.time = self.old_time

