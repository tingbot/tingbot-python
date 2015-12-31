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

.. py:function:: screen.text(string…, xy=…, color=…, align=…, font=…, font_size=…)

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


.. py:function:: screen.image(filename…, xy=…, scale=…, align=…)

    Draws an image with name filename at position xy.

    Images can be animated GIFs. Make sure to draw them in a loop() function to see them animate.

    Scale is a number that changes the size of the image e.g. scale=2 makes the image bigger, scale=0.5 makes the image smaller.

    Align is one of 

        topleft, left, bottomleft, top, center, bottom, topright, right, bottomright

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
        :caption: Example: Simple Drawing app

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

    @button.press('left')
    def on_left():
        state['score'] -= 1

    @button.press('right')
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

.. py:decorator:: button.press(button_name…)

    This 'decorator' marks the function to be called when a button is pressed.

    ``button_name`` can be one of: left, midleft, midright, right.
        
    The function is called when the button is pressed. Nothing happens when the button is released.

    .. code-block:: python
        :caption: Example: Button handler

        @button.press('left')
        def on_left():
            state['score'] -= 1

    .. code-block:: python
        :caption: Example: Button handler for all buttons

        @button.press('left')
        @button.press('midleft')
        @button.press('midright')
        @button.press('right')
        def on_button():
            state['score'] -= 1

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

