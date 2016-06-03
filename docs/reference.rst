Reference
=========

Screen
------

.. py:function:: screen.fill(color)

    Fills the screen with the specified ``color``.

    ``color`` can be specified using a name (e.g. 'white', 'black'), or an RGB triple  (255, 0, 0)  

    .. code-block:: python
       :caption: Example: fill the screen with white

       screen.fill(color='white')

    .. code-block:: python
        :caption: Example: fill the screen with red

        screen.fill(color=(255, 0, 0))

.. py:function:: screen.text(string…, xy=…, color=…, align=…, font=…, font_size=…, max_width=…, max_lines=…, max_height=…)

    Draws text ``string``.

    ``xy`` is the position that the text will be drawn.

    Align is one of:

        topleft, left, bottomleft, top, center, bottom, topright, right, bottomright

    If a custom font is used, it must be included in the tingapp bundle.

    .. code-block:: python
        :caption: Example: Write 'Hello world' in black on the screen

        screen.text('Hello world!', color='black')

    .. code-block:: python
        :caption: Example: changing the alignment

        screen.text('Hello world!', xy=(20,20), color='black', align='topleft')

    .. code-block:: python
        :caption: Example: Using a custom font

        screen.text('Hello world!', color='black', font='Helvetica.ttf')

    .. code-block:: python
        :caption: Example: Changing the text size

        screen.text('Hello world!', color='black', font_size=50)

    .. code-block:: python
        :caption: Example: Confining text to a single line

        screen.text('Lorem ipsum dolor sit amet, consectetur adipiscing elit!', color='black', max_lines=1)

    .. code-block:: python
        :caption: Example: Confining text to two lines

        screen.text('Lorem ipsum dolor sit amet, consectetur adipiscing elit!', color='black', max_width=300, max_lines=2)


.. py:function:: screen.rectangle(xy=…, size=…, color=…, align=…)

    Draws a rectangle at position xy, with the specified size and color.

    Align is one of

        topleft, left, bottomleft, top, center, bottom, topright, right, bottomright, 

    .. code-block:: python
        :caption: Example: Drawing a red square

        screen.rectangle(xy=(25,25), size=(100,100), color=(255,0,0))

    .. code-block:: python
        :caption: Example: Drawing centered

        screen.rectangle(xy=(160,120), size=(100,100), color=(255,0,0), align='center')


.. py:function:: screen.image(filename…, xy=…, scale=…, align=…, raise_error=True)

    Draws an image with name filename at position xy. If filename is a URL (e.g. http://example.com/cats.png) then
    it will attempt to download this and display it.

    Images can be animated GIFs. Make sure to draw them in a loop() function to see them animate.

    Scale is a number that changes the size of the image e.g. scale=2 makes the image bigger, scale=0.5 makes the image smaller.

    Align is one of 

        topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
        
    If raise_error is True then any errors encountered while opening or retrieving the image will cause 
    an `exception <https://docs.python.org/2/tutorial/errors.html>`_. If it is False, then if there is an 
    error a "file not found" icon will be displayed instead 

    .. code-block:: python
        :caption: Example: Drawing an Image
        
        screen.image('tingbot.png', xy=(25,25))

.. py:function:: screen.line(start_xy=…, end_xy=…, color=…, width=…)

    Draws a line between ``start_xy`` and ``end_xy``.

Touch
-----

Your Tingbot comes equipped with a resistive touch screen! It's easy to react to touch events.

.. code-block:: python
    :caption: Example: Simple drawing app

    import tingbot
    from tingbot import *

    screen.fill(color='black')

    @touch()
    def on_touch(xy):
        screen.rectangle(xy=xy, size=(5,5), color='blue')

    tingbot.run()

This is a simple drawing app. It uses the ``@touch()`` decorator to receive touch events and draws a
rectangle to the screen at the same place.

.. py:decorator:: touch(xy=…, size=…, align=…)

    This 'decorator' marks the function after it to receive touch events. 

    You can optionally pass an area that you're interested in, using the ``xy``, ``size`` and
    ``align`` arguments. If you specify no area, you will receive all touch events.

    The handler function can optionally take the arguments ``xy`` and ``action``. ``xy`` is the
    location of the touch. ``action`` is one of 'down', 'move', 'up'.

    .. code-block:: python
        :caption: Example: Simple Drawing app code

        @touch()
        def on_touch(xy):
            screen.rectangle(xy=xy, size=(5,5), color='blue')

    .. code-block:: python
        :caption: Example: Making a button do something

        @touch(xy=(0,0), size=(100,50), align='topleft')
        def on_touch(xy, action):
            if action == 'down':
                state['screen_number'] = 2

Buttons
-------

There are four buttons on the top of the Tingbot. These can be used in programs to trigger functions in your code.

.. code-block:: python
    :caption: Example: Score-keeping app.

    import tingbot
    from tingbot import *

    state = {'score': 0}

    @left_button.press
    def on_left():
        state['score'] -= 1

    @right_button.press
    def on_right():
        state['score'] += 1

    def loop():
        screen.fill(
            color='black')
        screen.text(
            state['score'],
            color='white')

    tingbot.run(loop)

This is a simple counter program. Whenever the right button is pressed, the score goes up by one. On
the left button, the score goes down.

.. py:decorator:: button.press

    This 'decorator' marks the function to be called when a button is pressed.

    ``button`` can be one of: left_button, midleft_button, midright_button, right_button.
    
    .. code-block:: python
        :caption: Example: Button handler

        @left_button.press
        def on_left():
            state['score'] -= 1

    .. code-block:: python
        :caption: Example: Button handler for all buttons

        @left_button.press
        @midleft_button.press
        @midright_button.press
        @right_button.press
        def on_button():
            state['score'] -= 1

    Only presses shorter than a second count - anything longer counts as a 'hold' event.

.. py:decorator:: button.hold

    This marks the function to be called when a button is held down for longer than a
    second.

.. py:decorator:: button.down

    This marks the function to be called as soon as a button is pushed down. This could
    be the start of a 'press' or a 'hold' event.

.. py:decorator:: button.up

    This marks the function to be called when a button is released.

Webhooks
--------

You can push data to Tingbot using webhooks.

Here is an example that displays SMS messages using `If This Then That <http://ifttt.com>`_. See
our `tutorial video <https://www.youtube.com/watch?v=yZg8OIzVByM>`_ to see how to set up IFTTT with
webhooks.

.. code-block:: python

    import tingbot
    from tingbot import *

    screen.fill(color='black')
    screen.text('Waiting...')

    @webhook('demo_sms')
    def on_webhook(data):
        screen.fill(color='black')
        screen.text(data, color='green')

    tingbot.run()

.. py:decorator:: webhook(webhook_name…)

    This decorator calls the marked function when a HTTP POST request is made to the URL
    :samp:`http://webhook.tingbot.com/{webhook_name}`. The POST data of the URL is available to the marked
    function as the ``data`` parameter.

    The data is limited to 1kb, and the last value that was POSTed is remembered by the server,
    so you can feed in relatively slow data sources.

You can use webhooks to push data to Tingbot, or to notify Tingbot of an update that happened
elsewhere on the internet.


.. hint::

    `IFTTT <http://ifttt.com>`_ is a great place to start for ideas for webhooks. 
    `Slack <http://slack.com>`_ also has native support for webhooks!
    
    
Settings
--------

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


Run loop
--------

Tingbot has an internal run loop that it uses to schedule events.

.. py:function:: tingbot.run(loop=None)

    This function starts the run loop.

    The optional ``loop`` function is called every 1/30th seconds.

.. py:decorator:: every(hours=0, minutes=0, seconds=0)

    This decorator will call the function marked periodically, according to the time specified.

    .. code-block:: python
        :caption: Example: Refreshing data every 10 minutes

        @every(minutes=10)
        def refresh_data():
            r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=bd82977b86bf27fb59a04b61b657fb6f')
            state['data'] = r.json()

