import collections
import json
import os
import sys

module_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
default_settings = os.path.join(module_dir,'default_settings.json')
gui_settings = os.path.join(module_dir,'gui_settings.json')
app_settings = os.path.join(module_dir,'app_settings.json')
print default_settings,gui_settings,app_settings

def load_json(filename):
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

class SettingsDict(collections.MutableMapping):

    def __init__(self):
        #note we do NOT initialise self.dct or self.local_settings here - this ensures we
        #raise an error in the event that they are accessed before self.load
        self.loaded = False
    
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
        self.dct = load_json(default_settings)
        self.dct.update(load_json(gui_settings))
        self.local_settings = load_json(app_settings)
        self.dct.update(self.local_settings)
        self.loaded = True            
    
    def save(self):
        with open(app_settings,'w') as fp:
            json.dump(fp,self.local_settings)
            
config = SettingsDict()
