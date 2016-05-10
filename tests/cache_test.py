import unittest
import time
from tingbot.cache import WebImage, FileImage, ImageCache, get_last_modified, get_max_age
from requests.structures import CaseInsensitiveDict as idict
from email.Utils import formatdate

class TimeHelper(object):
    def __init__(self):
        self.tm = 1000.0
    def __call__(self):
        return self.tm
        
class DummyResponse(object):
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)


class TimeControlCase(unittest.TestCase): 
    def setUp(self):
        mytime = TimeHelper()
        self.old_time = time.time
        time.time = mytime
        
    def tearDown(self):
        time.time = self.old_time

class TestGetLastModified(TimeControlCase):
    def test_simple_case(self):
        resp = DummyResponse(headers=idict({'last-modified':formatdate(100.0)}))
        self.assertEqual(get_last_modified(resp),100.0)
        
    def test_bad_last_modified(self):
        resp = DummyResponse(headers=idict({'last-modified':'ted'}))
        self.assertEqual(get_last_modified(resp),1000.0)
        
    def test_date(self):
        resp = DummyResponse(headers=idict({'last-modified':formatdate(200.0)}))
        self.assertEqual(get_last_modified(resp),200.0)
        
    def test_bad_date(self):
        resp = DummyResponse(headers=idict({'last-modified':'phil'}))
        self.assertEqual(get_last_modified(resp),1000.0)
        
    def test_no_useful_headers(self):    
        resp = DummyResponse(headers=idict({}))
        self.assertEqual(get_last_modified(resp),1000.0)
        
    
class TestGetMaxAge(TimeControlCase):
    def test_simple_case(self):
        resp = DummyResponse(headers=idict({'cache-control':'max-age = 300'}))
        self.assertEqual(get_max_age(resp,400),300)
        
    def test_bad_cache_control(self):
        resp = DummyResponse(headers=idict({'cache-control':'max-age = fred'}))
        self.assertEqual(get_max_age(resp,400),60)
        
    def test_plain_max_age(self):
        resp = DummyResponse(headers=idict({'max-age':'500'}))
        self.assertEqual(get_max_age(resp,400),500)
        
    def test_bad_max_age(self):
        resp = DummyResponse(headers=idict({'max-age':'ten'}))
        self.assertEqual(get_max_age(resp,400),60)
        
    def test_empty_headers(self):
        resp = DummyResponse(headers=idict({}))
        self.assertEqual(get_max_age(resp,400),60)

class TestWebImage(unittest.TestCase):
    def test_basic_load(self):
        f = WebImage('http://imgs.xkcd.com/static/terrible_small_logo.png')
                
class TestFileImage(unittest.TestCase):
    def test_basic_load(self):
        f = FileImage('tingbot/broken_image.png')
    
class TestImageCache(unittest.TestCase):
    pass
