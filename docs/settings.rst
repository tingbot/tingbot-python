☑️ Settings
----------

You can store local data on the tingbot. Simply use ``tingbot.app.settings`` as a `dict <http://learnpythonthehardway.org/book/ex39.html>`_. This will store
any variables you like on a file in the application directory (called local_settings.json). This is
stored in `JSON <http://www.w3resource.com/JSON/introduction.php>`_ format.

.. code-block:: python

    import tingbot
    
    #store an item
    tingbot.app.settings['favourite_colour'] = 'red'
    
    #local_settings.json on disk now contains: {"favourite_colour":"red"}
    
    #retrieve an item
    tingbot.screen.fill(tingbot.app.settings['favourite_colour'])

Any item that can be stored in JSON can be used in tingbot.app.settings - so strings, ints, floats, even dicts and lists can be used.

.. note::
    Take care when changing the insides of dicts or lists that are stored in tingbot.app.settings, as your changes will not be saved automatically.
    
    You can force a save by calling `tingbot.app.settings.save()`

    .. code-block:: python

        import tingbot
        
        # create a sub-dictionary
        tingbot.app.settings['ages'] = {'Phil': 39, 'Mabel': 73}
        
        # local_settings.json on disk now contains: {"ages":{"Phil":39,"Mabel":73}}
        
        tingbot.app.settings['ages']['Barry'] = 74
        
        # warning: local_settings.json has not been updated because you haven't directly changed tingbot.app.settings
        
        tingbot.app.settings.save()
        
        # now local_settings.json on disk now contains: {"ages":{"Phil":39,"Mabel":73,"Barry":74}}

Storage
'''''''

There are three settings files, that have different uses:

* ``default_settings.json`` When writing your app, you can put default values for your settings in this file. 

* ``settings.json`` Somebody who's downloaded your app can create this file in Tide to fill in some settings before uploading to Tingbot. This file should be 'gitignored' so it's not shared when the app is copied, and can contain secrets like API keys or passwords.

* ``local_settings.json`` When code within the app sets a setting, it's stored in this file. This prevents the app from overwriting data from the previous two files. This shouldn't be copied with an app and should be 'gitignored' too.

When the first setting is accessed the app loads each file in turn, so values in 'local_settings' override those in 'settings', which override those is 'default_settings'.
