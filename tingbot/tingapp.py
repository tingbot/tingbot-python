import collections
import json
import os
import sys
import hashlib
import logging
from .utils import cached_property, get_resource
from .graphics import Image

def load_json(filename):
    try:
        with open(filename, 'r') as fp:
            result = json.load(fp)
            if not isinstance(result, dict):
                raise ValueError('Failed to load %s because it should contain a dictionary object, not an array.' % filename)
            return result
    except ValueError:
        raise ValueError('Failed to load %s because it\'s not a valid JSON file' % filename)
    except IOError:
        #either non-existent file or empty filename
        return {}


def save_json(filename, obj):
    data = json.dumps(obj)

    with open(filename, 'w') as fp:
        fp.write(data)


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
        del self.local_settings[key]

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


def generic_icon(name):
    name_hash = int(hashlib.md5(name).hexdigest(), 16)
    color_options = [
        'blue', 'teal', 'green', 'olive', 'yellow', 'orange', 'red',
        'fuchsia', 'purple', 'maroon'
    ]
    color = color_options[name_hash % len(color_options)]

    letter = name[0].lower()
    icon = Image(size=(96, 96))

    icon.fill(color=color)
    image = get_resource('default-icon-texture-96.png')
    icon.image(image)
    font = get_resource('MiniSet2.ttf')

    descenders = ['g', 'p', 'q', 'y']
    ascenders = ['b', 'd', 'f', 'h', 'k', 'l', 't']
    y_offset = 0

    if letter in descenders:
        y_offset -= 8
    if letter in ascenders:
        y_offset += 6

    icon.text(letter,
        xy=(52, 41 + y_offset),
        color='white',
        font=font,
        font_size=70)

    # they're a little large compared to the real icons, let's size them down a bit
    resized_icon = Image(size=(96,96))
    resized_icon.image(icon, scale=0.9)

    return resized_icon


class TingApp(object):
    def __init__(self, path=None):
        """path is the root path of the app you want to inspect
           if path is None, then will let you inspect the current app"""
        if path is None:
            path = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.path = path
        self.settings = SettingsDict(path)

    @cached_property
    def info(self):
        return load_json(os.path.join(self.path, 'app.tbinfo'))

    @property
    def name(self):
        if 'name' in self.info and self.info['name'] != '':
            return self.info['name']
        else:
            return os.path.basename(self.path)

    @cached_property
    def icon(self):
        icon_path = os.path.join(self.path, 'icon.png')

        if not os.path.isfile(icon_path):
            return generic_icon(self.name)

        try:
            icon = Image.load(icon_path)
        except:
            logging.exception('Failed to load icon at %s', icon_path)
            return generic_icon(self.name)

        if icon.size != (96, 96):
            # resize the icon by redrawing in the correct size
            resized_icon = Image(size=(96, 96))
            resized_icon.image(icon, scale='shrinkToFit')
            return resized_icon

        return icon
            
app = TingApp()
