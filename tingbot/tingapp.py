import collections
import json
import os
import sys

default_settings = 'default_settings.json'
general_settings = 'settings.json'
local_settings = 'local_settings.json'
info_file = 'app.tbinfo'

def load_json(path,filename):
    filename = os.path.join(path,filename)
    try:
        with open(filename,'r') as fp:
            result = json.load(fp)
            if isinstance(result,dict):
                return result
            else:
                return {}
    except IOError,ValueError:
        #either non-existent file or empty filename
        return {}

def save_json(path,filename,obj):
    filename = os.path.join(path,filename)
    with open(app_settings,'w') as fp:
        json.dump(filename,obj)

class SettingsDict(collections.MutableMapping):

    def __init__(self,path):
        #note we do NOT initialise self.dct or self.local_settings here - this ensures we
        #raise an error in the event that they are accessed before self.load
        self.loaded = False
        self.path = path
    
    def __contains__(self,item):
        return item in self.dct
        
    def __len__(self):
        print "__len__"
        return len(self.dct)
        
    def __getitem__(self,key):
        if not self.loaded:
            self.load()
        return self.dct[key]
     
    def __setitem__(self,key,value):
        if not self.loaded:
            self.load()
        self.dct[key] = value
        self.local_settings[key] = value
        self.save()
        
    def __delitem__(self,key):
        del self.dct[key]
        
    def __iter__(self):
        return iter(self.dct)
        
        
    def load(self):
        self.dct = load_json(self.path,default_settings)
        self.dct.update(load_json(self.path,general_settings))
        self.local_settings = load_json(self.path,local_settings)
        self.dct.update(self.local_settings)
        self.loaded = True            
    
    def save(self):
        save_json(self.path,local_settings,self.local_settings)
        
class TingApp(object):
    def __init__(self,path=None):
        """path is the root path of the app you want to inspect
           if path is None, then will let you inspect the current app"""
        if path is None:
            path = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.info = load_json(path,info_file)
        self.settings = SettingsDict(path)
            
app = TingApp()
