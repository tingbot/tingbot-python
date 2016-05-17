import unittest
import tingbot.settings as settings
import json

def fake_load_json(filename):
    if filename == settings.default_settings:
        return {'a':1, 'b':2, 'c':3}
    elif filename == settings.gui_settings:
        return {'b':4, 'c':5}
    elif filename == settings.app_settings:
        return {'c':6}

class TestSettings(unittest.TestCase):
    def setUp(self):
        #monkey patch load and save functions
        self.load_json_old = settings.load_json
        self.save_json_old = settings.save_json
        settings.load_json = fake_load_json
        settings.save_json = self.fake_save_json
        self.settings = settings.SettingsDict()
        
    def tearDown(self):
        settings.save_json = self.save_json_old
        settings.load_json = self.load_json_old
        
    def fake_save_json(self,fp,obj):
        self.json_output = json.loads(json.dumps(obj))
        
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
        self.assertEqual(self.json_output,{'c':6})
    
    def test_assign_to_existing(self):
        self.settings['a'] = 25
        self.assertEqual(self.json_output,{'a':25,'c':6})
        
    def test_update_existing(self):
        self.settings['c'] = 8
        self.assertEqual(self.json_output,{'c':8})
        
    def test_assign_to_new_key(self):
        self.settings['fred'] = 15
        self.assertEqual(self.json_output,{'fred':15,'c':6})

    @unittest.expectedFailure                
    def test_assign_to_subkey(self):
        self.settings['map'] = {}
        self.settings['map']['subkey'] = 12
        self.assertEqual(self.json_output,{'map':{'subkey':12},'c':6})
