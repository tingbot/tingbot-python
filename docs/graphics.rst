🌈 Graphics
-----------

Drawing
~~~~~~~

.. py:function:: screen.fill(color)

    Fills the screen with the specified ``color``.

    :ref:`color-option` can be specified using a name (e.g. 'white', 'black'), or an RGB triple.

    .. code-block:: python
       :caption: Example: fill the screen with white

       screen.fill(color='white')

    .. code-block:: python
        :caption: Example: fill the screen with red

        screen.fill(color=(255, 0, 0))

.. py:function:: screen.text(string…, xy=…, color=…, align=…, font=…, font_size=…, max_width=…, max_lines=…, max_height=…)

    Draws text ``string``.

    ``xy`` is the position that the text will be drawn.

    :ref:`align-option` is one of:

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

.. function:: screen.image(filename…, xy=…, scale=…, align=…, max_width=…, max_height=…, raise_error=True)

    Draws an image with name filename at position xy. If filename is a URL (e.g. http://example.com/cats.png) then
    it will attempt to download this and display it.

    Images can be animated GIFs. Make sure to draw them in a loop() function to see them animate.

    Scale is a number that changes the size of the image e.g. scale=2 makes the image bigger, scale=0.5 makes the image smaller. There are also special values 'fit' and 'fill', which will fit or fill the image according to ``max_width`` and ``max_height``.

    Align is one of 

        topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
        
    If raise_error is True then any errors encountered while opening or retrieving the image will cause 
    an `exception <https://docs.python.org/2/tutorial/errors.html>`_. If it is False, then if there is an error a "file not found" icon will be displayed instead 

    .. code-block:: python
        :caption: Example: Drawing an Image
        
        screen.image('tingbot.png', xy=(25,25))

    .. code-block:: python
        :caption: Example: Drawing an Image from a URL
        
        screen.image('http://i.imgur.com/xbT92Gm.png')

.. py:function:: screen.line(start_xy=…, end_xy=…, color=…, width=…)

    Draws a line between ``start_xy`` and ``end_xy``.

Screen
~~~~~~

The screen supports all the methods above, and some extras below.

.. py:function:: screen.update()
    
    After drawing, this method should to be called to refresh the screen. When drawing in a
    ``draw()`` or ``loop()`` function, this is called automatically, but when drawing in a tight
    loop, e.g. during a calculation, it can called manually.

    .. code-block:: python
        :caption: Example: An app without a run loop - calling ``screen.update()`` manually

        import tingbot
        from tingbot import *

        screen.fill(color='black')

        # pump the main run loop just once to make sure the app starts
        tingbot.input.EventHandler().poll()

        frame_count = 0

        while True:
            screen.fill(color='black')
            screen.text(frame_count)
            screen.update()
            frame_count += 1

.. py:attribute:: screen.brightness

    The brightness of the screen, between 0 and 100.

    .. code-block:: python
        :caption: Example: Dimming the screen

        screen.brightness = 25

    .. code-block:: python
        :caption: Example: Brightness test app

        import tingbot
        from tingbot import *

        state = {'brightness': 0}

        def loop():
            screen.brightness = state['brightness']
            
            screen.fill(color='black')
            screen.text('Brightness\n %i' % state['brightness'])
            
            state['brightness'] += 1
            
            if state['brightness'] > 100:
                state['brightness'] = 0

        tingbot.run(loop)

.. _align-option:

The ``align`` option
~~~~~~~~~~~~~~~~~~~~

When used without the ``xy`` parameter, the item is positioned relative to the screen/drawing surface.

===============  =======================================  ========================================================
Setting          Screenshot                               Code
===============  =======================================  ========================================================
**topleft**      .. image:: images/align/topleft.png      ``screen.rectangle(color='green', align='topleft')``
                    :scale: 15%

**top**          .. image:: images/align/top.png          ``screen.rectangle(color='green', align='top')``
                    :scale: 15%

**topright**     .. image:: images/align/topright.png     ``screen.rectangle(color='green', align='topright')``
                    :scale: 15%

**left**         .. image:: images/align/left.png         ``screen.rectangle(color='green', align='left')``
                    :scale: 15%

**center**       .. image:: images/align/center.png       ``screen.rectangle(color='green', align='center')``
                    :scale: 15%

**right**        .. image:: images/align/right.png        ``screen.rectangle(color='green', align='right')``
                    :scale: 15%

**bottomleft**   .. image:: images/align/bottomleft.png   ``screen.rectangle(color='green', align='bottomleft')``
                    :scale: 15%

**bottom**       .. image:: images/align/bottom.png       ``screen.rectangle(color='green', align='bottom')``
                    :scale: 15%

**bottomright**  .. image:: images/align/bottomright.png  ``screen.rectangle(color='green', align='bottomright')``
                    :scale: 15%
===============  =======================================  ========================================================

When used with the ``xy`` parameter, it positions the item relative to the ``xy`` point.

===============  =========================================  ========================================================
Setting          Screenshot                                 Code
===============  =========================================  ========================================================
**topleft**      .. image:: images/alignxy/topleft.png      ``screen.rectangle(xy=(160, 120), align='topleft')``
                    :scale: 15%

**top**          .. image:: images/alignxy/top.png          ``screen.rectangle(xy=(160, 120), align='top')``
                    :scale: 15%

**topright**     .. image:: images/alignxy/topright.png     ``screen.rectangle(xy=(160, 120), align='topright')``
                    :scale: 15%

**left**         .. image:: images/alignxy/left.png         ``screen.rectangle(xy=(160, 120), align='left')``
                    :scale: 15%

**center**       .. image:: images/alignxy/center.png       ``screen.rectangle(xy=(160, 120), align='center')``
                    :scale: 15%

**right**        .. image:: images/alignxy/right.png        ``screen.rectangle(xy=(160, 120), align='right')``
                    :scale: 15%

**bottomleft**   .. image:: images/alignxy/bottomleft.png   ``screen.rectangle(xy=(160, 120), align='bottomleft')``
                    :scale: 15%

**bottom**       .. image:: images/alignxy/bottom.png       ``screen.rectangle(xy=(160, 120), align='bottom')``
                    :scale: 15%

**bottomright**  .. image:: images/alignxy/bottomright.png  ``screen.rectangle(xy=(160, 120), align='bottomright')``
                    :scale: 15%
===============  =========================================  ========================================================

.. _color-option:

The ``color`` option
~~~~~~~~~~~~~~~~~~~~

The color option can be either an RGB value, or predefined color name.

RGB values
''''''''''

RGB values (as a tuple), like ``(255, 128, 0)``.

Predefined colors
'''''''''''''''''

We also have a set of default colors, referred to by their name, as a string.


.. raw:: html

    <style>
        .color-swatches {
            margin-bottom: 30px;
        }
        .color-swatch {
            float: left;
            width: 25%;
            text-align: center;
            padding-top: 12px;
            padding-bottom: 15px;
        }
        .color-swatch.big {
            width: 100%;
            box-sizing: border-box;
        }
        .color-swatch span {
            display: block;
            margin-bottom: 3px;
        }
        .color-swatch code {
            background-color: transparent;
            color: inherit;
            border-color: currentColor;
            border-width: 0;
        }
        .bg-navy { background-color: #001F3F; }
        .bg-blue { background-color: #0074D9; }
        .bg-aqua { background-color: #7FDBFF; }
        .bg-teal { background-color: #39CCCC; }
        .bg-olive { background-color: #3D9970; }
        .bg-green { background-color: #2ECC40; }
        .bg-lime { background-color: #01FF70; }
        .bg-yellow { background-color: #FFDC00; }
        .bg-orange { background-color: #FF851B; }
        .bg-red { background-color: #FF4136; }
        .bg-fuchsia { background-color: #F012BE; }
        .bg-purple { background-color: #B10DC9; }
        .bg-maroon { background-color: #85144B; }
        .bg-white { background-color: #FFFFFF; }
        .bg-gray { background-color: #AAAAAA; }
        .bg-silver { background-color: #DDDDDD; }
        .bg-black { background-color: #000000; }
    </style>
    <div class="color-swatches">
      <div class="color-swatch bg-navy" style="color:hsla(210, 100%, 75%, 1.0)">
          <span>'navy'</span>
          <code>(0, 116, 217)</code>
      </div>
      <div class="color-swatch bg-blue" style="color:hsla(208, 100%, 85%, 1.0)">
          <span>'blue'</span>
          <code>(0, 116, 217)</code>
      </div>
      <div class="color-swatch bg-aqua" style="color:hsla(197, 100%, 20%, 1.0)">
          <span>'aqua'</span>
          <code>(127, 219, 255)</code>
      </div>
      <div class="color-swatch bg-teal">
          <span>'teal'</span>
          <code>(57, 204, 204)</code>
      </div>
      <div class="color-swatch bg-olive" style="color:hsla(153, 43%, 15%, 1.0)">
          <span>'olive'</span>
          <code>(61, 153, 112)</code>
      </div>
      <div class="color-swatch bg-green" style="color:hsla(127, 63%, 15%, 1.0)">
          <span>'green'</span>
          <code>(46, 204, 64)</code>
      </div>
      <div class="color-swatch bg-lime" style="color:hsla(146, 100%, 20%, 1.0)">
          <span>'lime'</span>
          <code>(1, 255, 112)</code>
      </div>
      <div class="color-swatch bg-yellow" style="color:hsla(52, 100%, 20%, 1.0)">
          <span>'yellow'</span>
          <code>(255, 220, 0)</code>
      </div>
      <div class="color-swatch bg-orange" style="color:hsla(28, 100%, 20%, 1.0)">
          <span>'orange'</span>
          <code>(255, 133, 27)</code>
      </div>
      <div class="color-swatch bg-red" style="color: hsla(3, 100%, 25%, 1.0)">
          <span>'red'</span>
          <code>(255, 65, 54)</code>
      </div>
      <div class="color-swatch bg-maroon" style="color:hsla(331, 74%, 70%, 1.0)">
          <span>'maroon'</span>
          <code>(133, 20, 75)</code>
      </div>
      <div class="color-swatch bg-fuchsia" style="color:hsla(314, 88%, 21%, 1.0)">
          <span>'fuchsia'</span>
          <code>(240, 18, 190)</code>
      </div>
      <div class="color-swatch bg-purple" style="color:hsla(292, 88%, 82%, 1.0)">
          <span>'purple'</span>
          <code>(177, 13, 201)</code>
      </div>
      <div class="color-swatch bg-black">
          <span>'black'</span>
          <code>(0, 0, 0)</code>
      </div>
      <div class="color-swatch bg-gray">
          <span>'gray'</span>
          <code>(170, 170, 170)</code>
      </div>
      <div class="color-swatch bg-silver">
          <span>'silver'</span>
          <code>(221, 221, 221)</code>
      </div>
      <div class="color-swatch big" style="color:#444;border:1px solid #ccc;">
          <span>'white'</span>
          <code>(255, 255, 255)</code>
      </div>
      <div style="clear:both"></div>
    </div>

Thanks to http://clrs.cc for the color scheme!
