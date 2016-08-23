import collections
import json
import os
import sys


def load_json(filename):
    try:
        with open(filename, 'r') as fp:
            result = json.load(fp)
            if isinstance(result, dict):
                return result
            else:
                return {}
    except (IOError, ValueError):
        #either non-existent file or empty filename
        return {}


def save_json(filename, obj):
    with open(app_settings, 'w') as fp:
        json.dump(filename, obj)


class SettingsDict(collections.MutableMapping):
    '''
    Represents the tingapp.settings dict-like object.

    The settings are loaded from three files in the app bundle

      - default_settings.json 
          This file contains default settings as defined by the app creator
      - settings.json
          This file contains settings as set by a user when installing the app
          (via Tide, for example)
      - local_settings.json
          This file contains settings written by the app itself.

    Settings can be overridden by later files.

    Changes are always saved to the local_settings.json file.
    '''
    def __init__(self, path):
        #note we do NOT initialise self.dct or self.local_settings here - this ensures we
        #raise an error in the event that they are accessed before self.load
        self.loaded = False
        self.path = path
    
    def __contains__(self, item):
        if not self.loaded:
            self.load()
        return item in self.dct
        
    def __len__(self):
        if not self.loaded:
            self.load()
        return len(self.dct)
        
    def __getitem__(self, key):
        if not self.loaded:
            self.load()
        return self.dct[key]
     
    def __setitem__(self, key, value):
        if not self.loaded:
            self.load()
        self.dct[key] = value
        self.local_settings[key] = value
        self.save()
        
    def __delitem__(self, key):
        if not self.loaded:
            self.load()
        del self.dct[key]
        
    def __iter__(self):
        if not self.loaded:
            self.load()
        return iter(self.dct)

    def load(self):
        self.dct = load_json(os.path.join(self.path, 'default_settings.json'))
        self.dct.update(load_json(os.path.join(self.path, 'settings.json')))
        self.local_settings = load_json(os.path.join(self.path, 'local_settings.json'))
        self.dct.update(self.local_settings)
        self.loaded = True

    def save(self):
        save_json(os.path.join(self.path, 'local_settings.json'), self.local_settings)


class TingApp(object):
    def __init__(self, path=None):
        """path is the root path of the app you want to inspect
           if path is None, then will let you inspect the current app"""
        if path is None:
            path = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.info = load_json(os.path.join(path, 'app.tbinfo'))
        self.settings = SettingsDict(path)
            
app = TingApp()
