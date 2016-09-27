import unittest
import tingbot.tingapp as tingapp
import json
import os
import tempfile
import shutil

def fake_load_json(filename):
    if os.path.basename(filename) == 'default_settings.json':
        return {'a':1, 'b':2, 'c':3}
    elif os.path.basename(filename) == 'settings.json':
        return {'b':4, 'c':5}
    elif os.path.basename(filename) == 'local_settings.json':
        return {'c':6}

class TestSettings(unittest.TestCase):
    def setUp(self):
        self.fake_tingapp_dir = tempfile.mkdtemp()

        with open(os.path.join(self.fake_tingapp_dir, 'default_settings.json'), 'w') as f:
            json.dump({'a':1, 'b':2, 'c':3}, f)
        with open(os.path.join(self.fake_tingapp_dir, 'settings.json'), 'w') as f:
            json.dump({'b':4, 'c':5}, f)
        with open(os.path.join(self.fake_tingapp_dir, 'local_settings.json'), 'w') as f:
            json.dump({'c':6}, f)

        self.settings = tingapp.SettingsDict(self.fake_tingapp_dir)
        
    def tearDown(self):
        shutil.rmtree(self.fake_tingapp_dir)

    def local_settings_contents(self):
        with open(os.path.join(self.fake_tingapp_dir, 'local_settings.json')) as f:
            return json.load(f)

    def test_simple_assign_and_retrieve(self):
        self.settings['fred'] = 12
        self.assertEqual(self.settings['fred'],12)
        
    def test_load_from_defaults(self):
        self.assertEqual(self.settings['a'],1)
        
    def test_load_from_gui(self):
        self.assertEqual(self.settings['b'],4)

    def test_load_from_locals(self):
        self.assertEqual(self.settings['c'],6)
        
    def test_save_updates_only_local_vars(self):
        self.settings.load()
        self.settings.save()
        self.assertEqual(self.local_settings_contents(),{'c':6})
    
    def test_assign_to_existing(self):
        self.settings['a'] = 25
        self.assertEqual(self.local_settings_contents(),{'a':25,'c':6})
        
    def test_update_existing(self):
        self.settings['c'] = 8
        self.assertEqual(self.local_settings_contents(),{'c':8})
        
    def test_assign_to_new_key(self):
        self.settings['fred'] = 15
        self.assertEqual(self.local_settings_contents(),{'fred':15,'c':6})

    def test_contains(self):
        self.assertEqual('a' in self.settings, True)

    @unittest.expectedFailure                
    def test_assign_to_subkey(self):
        self.settings['map'] = {}
        self.settings['map']['subkey'] = 12
        self.assertEqual(self.local_settings_contents(),{'map':{'subkey':12},'c':6})
