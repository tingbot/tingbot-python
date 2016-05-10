#image cache
import time
import re
import rfc822
import calendar
import requests
import io

def get_http_timestamp(dt):
    return calendar.timegm(rfc822.parsedate(dt))

def get_last_modified(response):
    """try and determine the last_modified time of a request"""
    try:
        return get_http_timestamp(response.headers['last-modified'])
    except (KeyError,TypeError):
        pass
    try:
        return get_http_timestamp(response.headers['date'])
    except (KeyError,TypeError):
        return time.time()     

def get_max_age(response,last_modified):
    """return how many seconds from original access this response is valid for"""
    try:
        return int(re.match(r"max-age\W*=\W*(\d+)", response.headers['cache-control']).group(1))
    except (KeyError,ValueError,AttributeError,TypeError) as e:
        pass
    try:
        return int(response.headers['max-age'])
    except (KeyError,ValueError):
        pass
    try:
        return get_http_timestamp(response.headers['expires']) - time.time()
    except (KeyError,TypeError):
        #really no info from server  so guess based on last-modified
        return min(24*60*60,(time.time()-last_modified)/10)

class ImageEntry(object):
    #abstract base class
    def get_image(self):
        self.last_accessed = time.time()
        return self.image  
        
    def get_size(self):
        return self.image.surface.get_buffer().length  
    

class WebImage(ImageEntry):
    ##FIXME## include etags!
    def __init__(self,url):
        import graphics
        self.url = url
        response = requests.get(url)
        response.raise_for_status() #raise exception if url not appropriate
        self.set_attributes(response)
        image_file = io.BytesIO(response.content)        
        self.image = graphics.Image.load_file(image_file,url)
        self.last_accessed = time.time()
        self.retrieved = time.time()       
        
    def set_attributes(self,response):    
        self.last_modified = get_last_modified(response)
        self.max_age  = get_max_age(response,self.last_modified)
        
    def is_fresh(self):
        now = time.time()
        if (now-self.retrieved)<self.max_age:
            return True
        try:
            response = requests.head(self.url)
            response.raise_for_status()
            self.set_attributes(response)
            if self.last_modified<self.retrieved:
                return True
        except IOError:
            return False
        return False
        
class FileImage(object):
    pass
        
        
class ImageCache(object):
    def __init__(self):
        self.images = {}
        self.size = 0
        
    def get_image(self,location):
        if location in self.images:
            if self.images[location].is_fresh():
                return self.images[location].get_image()
            else:
                self.size -= self.images[location].get_size()
                del self.images[location]
        if is_url(location):
            self.images[location] = WebImage(location)
        else:
            self.images[location] = FileImage(location)
        self.size += self.images[location].get_size()
        return self.images[location].get_image()
        
