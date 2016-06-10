#image cache
import time
import re
import rfc822
import calendar
import requests
import io
import os
import threading
from urlparse import urlparse

def get_http_timestamp(dt):
    return calendar.timegm(rfc822.parsedate(dt))

def get_server_date(response):
    try:
        return get_http_timestamp(response.headers['date'])
    except (KeyError, TypeError):
        # no date supplied, have to assume no time offset
        return time.time()

def get_last_modified(response):
    """try and determine the last_modified time of a request"""
    try:
        return get_http_timestamp(response.headers['last-modified'])
    except (KeyError, TypeError):
        return None

def get_max_age(response, last_modified):
    """return how many seconds from original access this response is valid for"""
    try:
        return int(re.match(r"max-age\W*=\W*(\d+)", response.headers['cache-control']).group(1))
    except (KeyError, ValueError, AttributeError, TypeError) as e:
        pass
    try:
        return int(response.headers['max-age'])
    except (KeyError, ValueError):
        pass
    try:
        return get_http_timestamp(response.headers['expires']) - get_server_date(response)
    except (KeyError, TypeError):
        #really no info from server  so guess based on last-modified
        if last_modified:
            return min(24*60*60, (get_server_date(response) - last_modified)/10)
        else:
            #not even a last_modified - so conservative guess of 60s
            return 60

def get_etag(response):
    try:
        return response.headers['etag']
    except KeyError:
        return None

def is_url(loc):
    """returns true if loc is a url, and false if not"""
    return (urlparse(loc).scheme != '')


class ImageEntry(object):
    #abstract base class
    def get_image(self):
        self.last_accessed = time.time()  # local time
        return self.image

    def get_size(self):
        return self.image.get_memory_usage()


class WebImage(ImageEntry):
    def __init__(self, url):
        import graphics
        self.url = url
        response = requests.get(url)
        response.raise_for_status()  # raise exception if url not appropriate
        self.set_attributes(response)
        image_file = io.BytesIO(response.content)
        self.image = graphics.Image.load_file(image_file, url)
        self.last_accessed = time.time()  # local time
        self.retrieved = time.time()  # local time

    def set_attributes(self, response):
        self.last_modified = get_last_modified(response)  # server time
        self.max_age = get_max_age(response, self.last_modified)  # seconds unit, no timeframe
        self.etag = get_etag(response)

    def is_fresh(self):
        now = time.time()
        if (now-self.retrieved) < self.max_age:  # local time - local time
            return True
        try:
            response = requests.head(self.url)
            response.raise_for_status()
            old_lm = self.last_modified
            old_etag = self.etag
            self.retrieved = time.time()
            self.set_attributes(response)
            if old_etag and self.etag == old_etag:
                return True
            if old_lm and self.last_modified == old_lm:
                return True
        except IOError:
            return False
        return False

class FileImage(ImageEntry):
    def __init__(self, filename):
        import graphics
        self.filename = filename
        self.image = graphics.Image.load_filename(filename)
        self.last_modified = os.path.getmtime(filename)
        self.last_accessed = time.time()

    def is_fresh(self):
        try:
            return self.last_modified == os.path.getmtime(self.filename)
        except IOError:
            return False

class ImageCache(object):
    def __init__(self, cache_size = 2*10**6):
        self.images = {}
        self.size = 0
        self.cache_size = cache_size
        self.lock = threading.RLock()

    def get_image(self, location):
        image = self.images.get(location)
        if image and image.is_fresh():
            return image.image
        if is_url(location):
            image = WebImage(location)
        else:
            image = FileImage(location)
        self.add_image(location, image)
        return image.image        
            
    def add_image(self, location, image):
        with self.lock:
            #delete image if already in cache and being over-written
            if location in self.images:
                self.del_image(location)
            self.images[location] = image
            self.size += image.get_size()

            #clean out cache if too big
            if self.size > self.cache_size:
                for key in sorted(self.images, key = lambda a:self.images[a].last_accessed):
                    if self.size <= self.cache_size:
                        break
                    elif key != location:
                        self.del_image(key)

    def del_image(self, location):
        with self.lock:
            self.size -= self.images[location].get_size()
            del self.images[location]
