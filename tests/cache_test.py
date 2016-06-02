import unittest
import time
import httpretty
import mock
import re

import tingbot.cache as cache
import tingbot.graphics as graphics
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
        self.assertEqual(cache.get_last_modified(resp),100.0)
        
    def test_bad_last_modified(self):
        resp = DummyResponse(headers=idict({'last-modified':'ted'}))
        self.assertEqual(cache.get_last_modified(resp),None)
        
    def test_date(self):
        resp = DummyResponse(headers=idict({'last-modified':formatdate(200.0)}))
        self.assertEqual(cache.get_last_modified(resp),200.0)
        
    def test_bad_date(self):
        resp = DummyResponse(headers=idict({'last-modified':'phil'}))
        self.assertEqual(cache.get_last_modified(resp),None)
        
    def test_no_useful_headers(self):    
        resp = DummyResponse(headers=idict({}))
        self.assertEqual(cache.get_last_modified(resp),None)
        
    
class TestGetMaxAge(TimeControlCase):
    def test_simple_case(self):
        resp = DummyResponse(headers=idict({'cache-control':'max-age = 300'}))
        self.assertEqual(cache.get_max_age(resp,400),300)
        
    def test_bad_cache_control(self):
        resp = DummyResponse(headers=idict({'cache-control':'max-age = fred'}))
        self.assertEqual(cache.get_max_age(resp,400),60)
        
    def test_plain_max_age(self):
        resp = DummyResponse(headers=idict({'max-age':'500'}))
        self.assertEqual(cache.get_max_age(resp,400),500)
        
    def test_bad_max_age(self):
        resp = DummyResponse(headers=idict({'max-age':'ten'}))
        self.assertEqual(cache.get_max_age(resp,400),60)
        
    def test_empty_headers(self):
        resp = DummyResponse(headers=idict({}))
        self.assertEqual(cache.get_max_age(resp,400),60)

class TestWebImage(TimeControlCase):
    def setUp(self):
        super(TestWebImage,self).setUp()
        httpretty.enable()
        self.image_content = open("tingbot/broken_image.png",'r').read()
        
    def tearDown(self):
        httpretty.disable()
        super(TestWebImage,self).tearDown()

    def test_basic_load(self):
        httpretty.register_uri(httpretty.GET,"http://example.com/cats.png",body=self.image_content)
        f = cache.WebImage('http://example.com/cats.png')
        
    def test_raises_error_on_bad_URL(self):
        httpretty.register_uri(httpretty.GET,"http://example.com/cats.png",body="not found",status=404)
        with self.assertRaises(IOError):
            f = cache.WebImage('http://example.com/cats.png')
            
    def test_is_fresh_while_within_maxage(self):
        httpretty.register_uri(httpretty.GET,"http://example.com/cats.png",
                               body=self.image_content, max_age=300, last_modified = formatdate(200.0))
        httpretty.register_uri(httpretty.HEAD,"http://example.com/cats.png",
                               max_age=300, last_modified = formatdate(300.0) )
        f = cache.WebImage('http://example.com/cats.png')
        time.time.tm=1200
        self.assertTrue(f.is_fresh())
        
    def test_is_fresh_on_recheck_with_last_modified_unchanged(self):
        httpretty.register_uri(httpretty.GET,"http://example.com/cats.png",
                               body=self.image_content, max_age=300, last_modified = formatdate(200.0) )
        httpretty.register_uri(httpretty.HEAD,"http://example.com/cats.png",
                               max_age=300, last_modified = formatdate(200.0) )
        f = cache.WebImage('http://example.com/cats.png')
        time.time.tm=1400
        self.assertTrue(f.is_fresh())
                
    def test_is_fresh_on_recheck_with_last_modified_changed(self):
        httpretty.register_uri(httpretty.GET,"http://example.com/cats.png",
                               body=self.image_content, max_age=300, last_modified = formatdate(200.0) )
        httpretty.register_uri(httpretty.HEAD,"http://example.com/cats.png",
                               max_age=300, last_modified = formatdate(300.0) )
        f = cache.WebImage('http://example.com/cats.png')
        time.time.tm=1400
        self.assertFalse(f.is_fresh())
                
    def test_is_fresh_on_recheck_with_etag_unchanged(self):
        httpretty.register_uri(httpretty.GET,"http://example.com/cats.png",
                               body=self.image_content, max_age=300, etag="a", last_modified = formatdate(200.0) )
        httpretty.register_uri(httpretty.HEAD,"http://example.com/cats.png",
                               max_age=300, etag="a", last_modified = formatdate(300.0) )
        f = cache.WebImage('http://example.com/cats.png')
        time.time.tm=1400
        self.assertTrue(f.is_fresh())
        
    def test_is_fresh_on_recheck_with_etag_changed(self):
        httpretty.register_uri(httpretty.GET,"http://example.com/cats.png",
                               body=self.image_content, max_age=300, etag="a", last_modified = formatdate(200.0) )
        httpretty.register_uri(httpretty.HEAD,"http://example.com/cats.png",
                               max_age=300, etag="b", last_modified = formatdate(300.0) )
        f = cache.WebImage('http://example.com/cats.png')
        time.time.tm=1400
        self.assertFalse(f.is_fresh())
        
    def test_is_fresh_if_no_last_modified_or_etag(self):
        httpretty.register_uri(httpretty.GET,"http://example.com/cats.png",
                               body=self.image_content, max_age=300)
        httpretty.register_uri(httpretty.HEAD,"http://example.com/cats.png",
                               max_age=300)
        f = cache.WebImage('http://example.com/cats.png')
        time.time.tm=1400
        self.assertFalse(f.is_fresh())
                   
class TestFileImage(unittest.TestCase):
    def test_basic_load(self):
        f = cache.FileImage('tingbot/broken_image.png')
        
    def test_bad_location(self):
        with self.assertRaises(IOError):
            f = cache.FileImage('tingbot_bork/broken_image.png')
    
    @mock.patch('tingbot.cache.os.path.getmtime')     
    def test_is_fresh_if_unchanged_mod_time(self,mtime):
        mtime.return_value = 200
        f = cache.FileImage('tingbot/broken_image.png')
        self.assertTrue(f.is_fresh())
    
    @mock.patch('tingbot.cache.os.path.getmtime')     
    def test_is_fresh_if_changed_mod_time(self,mtime):
        mtime.return_value = 200
        f = cache.FileImage('tingbot/broken_image.png')
        mtime.return_value = 300
        self.assertFalse(f.is_fresh())
    
class TestImageCache(TimeControlCase):
    def setUp(self):
        super(TestImageCache,self).setUp()
        httpretty.enable()
        self.image_content = open("tingbot/broken_image.png",'r').read()
        self.tiny_content = open("tests/blank.png",'r').read()
        httpretty.register_uri(httpretty.GET,re.compile("http://example.com/..png"), body=self.image_content)
        httpretty.register_uri(httpretty.GET,re.compile("http://example.com/tiny/..png"), body=self.tiny_content)
        
    def tearDown(self):
        httpretty.disable()
        super(TestImageCache,self).tearDown()

    def test_can_init(self):
        c = cache.ImageCache()
        
    def test_loads_one_file(self):
        c = cache.ImageCache(1000000)
        image  = c.get_image("http://example.com/a.png")
        self.assertIsInstance(image,graphics.Image)
        
    def test_loads_gif(self):
        c = cache.ImageCache(1000000)
        image = c.get_image('tests/GifSample.gif')    
        self.assertIsInstance(image,graphics.GIFImage)
        
    def test_loads_one_massive_file(self):
        c = cache.ImageCache(100)
        image = c.get_image("http://example.com/a.png")
        self.assertIsInstance(image,graphics.Image)
        
    def test_removes_a_file_when_full(self):
        image_size = cache.WebImage('http://example.com/a.png').get_size()
        c = cache.ImageCache(image_size+1)
        a = c.get_image('http://example.com/a.png')
        b = c.get_image('http://example.com/b.png')
        self.assertEqual(len(c.images),1)
        
    def test_removes_oldest_file_when_full(self):
        image_size = cache.WebImage('http://example.com/a.png').get_size()
        print image_size
        c = cache.ImageCache(image_size+1)
        a_url = 'http://example.com/a.png'
        b_url = 'http://example.com/b.png'
        a = c.get_image(a_url)
        b = c.get_image(b_url)
        self.assertFalse(a_url in c.images)
        self.assertTrue(b_url in c.images)
        
    def test_removes_more_than_one_file_if_needed(self):
        image_size = cache.WebImage('http://example.com/a.png').get_size()
        c = cache.ImageCache(image_size+1)
        tiny_url_a = 'http://example.com/tiny/a.png'        
        tiny_url_b = 'http://example.com/tiny/b.png'        
        url_d = 'http://example.com/a.png'
        a = c.get_image(tiny_url_a)
        b = c.get_image(tiny_url_b)
        d = c.get_image(url_d)
        self.assertEqual(len(c.images),1)
        self.assertFalse(tiny_url_a in c.images)
        self.assertFalse(tiny_url_b in c.images)
        self.assertTrue(url_d in c.images)
                
    def test_successfully_reloads_an_expired_file(self):
        httpretty.register_uri(httpretty.GET,re.compile("http://example.com/x/1.png"), body=self.image_content, etag="a", max_age="300")
        c = cache.ImageCache()
        a = c.get_image("http://example.com/x/1.png")
        httpretty.register_uri(httpretty.GET,re.compile("http://example.com/x/1.png"), body=self.image_content, etag="b", max_age="300")
        httpretty.register_uri(httpretty.HEAD,re.compile("http://example.com/x/1.png"), etag="b", max_age="300")
        time.time.tm=1400
        b = c.get_image("http://example.com/x/1.png")

