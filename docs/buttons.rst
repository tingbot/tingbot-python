◽️ ️Buttons
---------

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

.. py:decorator:: left_button.press
.. py:decorator:: midleft_button.press
.. py:decorator:: midright_button.press
.. py:decorator:: right_button.press

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

.. py:decorator:: Button.hold

    This marks the function to be called when a button is held down for longer than a
    second.
    
    .. code-block:: python
        :caption: Example: Reset button handler

        @left_button.hold
        def reset_score():
            state['score'] = 0

.. py:decorator:: Button.down

    This marks the function to be called as soon as a button is pushed down. This could
    be the start of a 'press' or a 'hold' event.

    This one is useful for games or when you want the button to be as responsive as possible.

    .. code-block:: python
        :caption: Example: Reset button handler

        @right_button.down
        def jump():
            dude.jump()

.. py:decorator:: Button.up

    This marks the function to be called when a button is released.

    .. code-block:: python
        :caption: Example: Down/up handler pair

        @right_button.down
        def down():
            state['button_is_down'] = True

        @right_button.up
        def up():
            state['button_is_down'] = False

.. py:decorator:: button.combo(buttons...)

    This marks the function to be called when some buttons are pressed at the same time.

    You can give it as many buttons as you like and ``combo`` will call the function when all
    the buttons are pressed together.

    .. code-block:: python
        :caption: Example: Combo to dim/wake the screen

        @button.combo(left_button, right_button)
        def screen_dim():
            if screen.brightness == 100:
                screen.brightness = 0
            else:
                screen.brightness = 100

