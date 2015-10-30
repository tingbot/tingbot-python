Reference
=========

``screen``
----------

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

        screen.text(xy=(160,120), size=(100,100), color=(255,0,0), align='center')


.. py:function:: screen.image(filename…, xy=…, scale=…, align=…)

    Draws an image with name filename at position xy.

    Images can be animated GIFs. Make sure to draw them in a loop() function to see them animate.

    Scale is a number that changes the size of the image e.g. scale=2 makes the image bigger, scale=0.5 makes the image smaller.

    Align is one of 

        topleft, left, bottomleft, top, center, bottom, topright, right, bottomright

    .. code-block:: python
        :caption: Example: Drawing an Image
        
        screen.image('tingbot.png', xy=(25,25))
