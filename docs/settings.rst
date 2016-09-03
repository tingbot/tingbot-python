☑️ Settings
----------

You can store local data on the tingbot. Simply use `tingbot.app.settings` as a `dict <http://learnpythonthehardway.org/book/ex39.html>`_. This will store
any variables you like on a file in the application directory (called local_settings.json). This is
stored in `JSON <http://www.w3resource.com/JSON/introduction.php>`_ format. As a developer you can also supply
default settings for your app to start off with - specify these in default_settings.json. 

.. code-block:: python

    import tingbot
    
    #store an item
    tingbot.app.settings['favourite_colour'] = 'red'
    
    #local_settings.json on disk now contains: {"favourite_colour":"red"}
    
    #retrieve an item
    tingbot.screen.fill(tingbot.app.settings['favourite_colour'])

Any item that can be converted into text can be used in tingbot.app.settings - so strings, ints, floats, and even dicts
and lists can be used. However, beware, because if you assign to a subitem of `tingbot.app.settings`, this will not be
automatically saved to disk. You can force a save by calling `tingbot.app.settings.save()`

.. code-block:: python

    import tingbot
    
    #create a sub-dictionary
    tingbot.app.settings['ages'] = {'Phil':39,'Mabel',73}
    
    #local_settings.json on disk now contains: {"ages":{"Phil":39,"Mabel":73}}
    
    tingbot.app.settings['ages']['Barry'] = 74
    
    #Warning: local_settings.json has not been updated because you haven't directly changed tingbot.app.settings
    
    tingbot.app.settings.save()
    
    #now local_settings.json on disk now contains: {"ages":{"Phil":39,"Mabel":73,"Barry":74}}
