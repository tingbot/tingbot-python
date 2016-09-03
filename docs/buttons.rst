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

.. py:decorator:: button.hold

    This marks the function to be called when a button is held down for longer than a
    second.

.. py:decorator:: button.down

    This marks the function to be called as soon as a button is pushed down. This could
    be the start of a 'press' or a 'hold' event.

.. py:decorator:: button.up

    This marks the function to be called when a button is released.
