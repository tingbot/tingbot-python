👈 Touch
--------

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
