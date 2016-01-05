Graphical user interface
========================

:mod:`tingbot.gui` -- Graphical user interface for tingbot

.. _styles:

Styles
------

The appearance of many of the gui components (also known as widgets) are highly configurable.
There are two ways to alter the style of the interface

1. Use the default style. This will affect every single widget, even ones that have already
been created.
    
    .. code-block:: python    
        :caption: Example: alter the background color to blue for every widget
        
        style = gui.get_style_default()
        style.bg_color = "blue"

2. Use a custom style. This allows you to customize individual widgets or groups of widgets

   .. code-block:: python
        :caption: Example: create two buttons with a smaller font size 
        
        custom_style = gui.Style(button_text_font_size = 12)
        button1 = gui.Button((50,50),(80,80),but_text="Small text",style=custom_style)
        button2 = gui.Button((150,50),(80,80),but_text="Small again",style=custom_style)
        button3 = gui.Button((250,50),(80,80),but_text="Normal")
        
   Custom made styles will all inherit the default settings, so you only need to specify
   those items that need to be altered
    
Styles can be updated dynamically, even after the widget has been created

.. py:class:: Style(**kwargs)

    :param \*\*kwargs: specify style attributes as required 
    :returns: A new Style with attributes set as per kwargs, all others are as per default settings

.. py:function:: get_default_style()

    :returns: The default style.

Widgets
-------

There are several different elements that can be used in an interface, known as widgets

.. py:class:: Button(xy, size, align="center", parent=None, style=None, but_text="OK", callback=None)

    Base: Widget

    A simple button control

    :param xy: position that the widget will be drawn
    :param size: size of the widget
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this widget. If None, widget will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this widget. If None, the widget will have the default style
    :param but_text: Text to display on button
    :param callable callback: function to call when the button is pressed. It should not take any arguments
    
    
    .. py:attribute:: but_text
    
        Text to be displayed on the button.
        
    .. py:attribute:: callback
    
        Function to be called when button is clicked. No arguments passed. See `Callbacks`_ for more information
        
    :Style Attributes:
        - *bg_color* -- background color
        - *button_color* -- color of this button when not pressed
        - *button_pressed_color* -- color to use when button pressed
        - *button_rounding* -- rounding in pixels of button corners. use 0 for square corners
        - *button_text_color* -- color to use for text
        - *button_text_font* -- font to use (default)
        - *button_text_font_size* -- font size to use
    
.. py:class:: ToggleButton(xy, size, align="center", parent=None, style=None, but_text="OK", callback=None)

    Base: Widget

    A button which can be in an on or off state
    
    :param xy: position that the widget will be drawn
    :param size: size of the widget
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this widget. If None, widget will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this widget. If None, the widget will have the default style
    :param but_text: Text to display on button
    :param callable callback: function to call when the button is pressed. It should accept a single boolean value
    
    
    .. py:attribute:: but_text
    
        Text to be displayed on the button.
        
    .. py:attribute:: pressed
    
        Current state of the button. True if pressed, False if not
        
    .. py:attribute:: callback
    
        Function to be called when button is clicked. A boolean value is passed which is the current state of the button.
        See `Callbacks`_ for more information
        
    :Style Attributes:
        - *bg_color* -- background color
        - *button_color* -- color of this button when not pressed
        - *button_pressed_color* -- color to use when button pressed
        - *button_rounding* -- rounding in pixels of button corners. use 0 for square corners
        - *button_text_color* -- color to use for text
        - *button_text_font* -- font to use (default)
        - *button_text_font_size* -- font size to use
    
    
        
.. py:class:: Slider(xy, size, align = "center", parent = None, style = None, max_val=1.0, min_val=0.0, step = None, change_callback=None)

    Base: Widget
    
    A sliding control to allow selection from a range of values
    
    :param xy: position that the widget will be drawn
    :param size: size of the widget
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this widget. If None, widget will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this widget. If None, the widget will have the default style
    :param float max_val: maximum value for the slider
    :param float min_val: minimum value for the slider
    :param step: amount to jump by when clicked outside the slider handle. Defaults to 1/10 of ``max_val-min_val``
    :param callable change_callback: function called when the slider is moved. Passed a float which is the sliders new value
    
    .. py:attribute:: value
    
        Current value of the slider
        
    .. py:attribute:: change_callback
        
        Function to be called when the slider is moved. A single float is passed. See `Callbacks`_ for more information

    :Style Attributes:
        - *bg_color* -- background color
        - *slider_line_color* -- color of the line
        - *slider_handle_color* -- color of the handle

.. py:class:: Widget(xy, size, align = "center", parent = None)

    This is the base class for all other widgets, but should not be directly used. All other widgets
    will have the methods listed below. You can make your own widgets by sub-classing this one. You
    will need to override the draw method, and possibly the on_touch method
        
    :param xy: position that the widget will be drawn
    :param size: size of the widget
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this widget. If None, widget will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this widget. If None, the widget will have the default style
    
    .. py:attribute:: visible
    
        True if the widget is to be displayed. Widget will be hidden if false
    
    .. py:method:: on_touch(self,xy,action)
        
        Override this method for any widgets that respond to touch events
        
        :param xy: position of the touch
        :param action: one of "up","down","move"
        
    .. py:method:: update(self,upwards=True,downwards=False)
    
        Call this method to redraw the widget. The widget will only be drawn if visible
        
        :param upwards: set to True to ask any parents (and their parents) to redraw themselves
        :param downwards: set to True to make any children  redraw themselves
        
    .. py:method:: draw(self)
    
        Called when the widget needs to draw itself. Override this method for all derived widgets

    .. py:attribute:: surface
    
        A pygame surface that corresponds to the widgets area - use this in the draw method
        
Containers
----------

Containers can be used to group widgets together. ScrollAreas can be used to access more widgets than can fit
on the screen otherwise. 

.. py:class:: Container

    A base class for ScrollAreas
    
.. py:class:: Panel

    Base: Container

    Panel class, allows you to collect together various widgets and turn on or off as needed

.. py:class:: ScrollArea(xy,size,align="center",parent=None,style = None,canvas_size=None)

    Base: Container
    
    ScrollArea gives a viewing area into another, usually larger area. This allows the user to access more
    widgets than will fit on the display. Scrollbars will be added to either edge as needed

    :param xy: position that the widget will be drawn
    :param size: size of the widget
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this widget. If None, widget will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this widget. If None, the widget will have the default style
    :param canvas_size: size of the scrollable area (required)
    
    .. py:attribute:: scrolled_area
    
        Use this as the parent for any widgets you wish to place within this container
        
Callbacks
---------

Basic usage
+++++++++++

Several classes use callbacks to respond to user events. The simplest of these take no arguments

    .. code-block:: python    
        :caption: Example: respond to a button press
        
        def button_callback():
            screen.text("Button pressed")

        but = Button((40,40),(80,80),but_text="Button",callback = button_callback)
        
Notice that ``button_callback`` has no brackets when passed to the Button. Other callbacks will take a value dependent on the state of the widget.
For example, the callback for a slider will pass it's current value as a float

    .. code-block:: python    
        :caption: Example: display the value of a slider
        
        def slider_callback(value):
            screen.text("%d" % int(value))

        slider = Slider((0,200),(320,20),align="topleft",max_val = 200,change_callback = slider_callback)
    
Passing extra arguments to callbacks
++++++++++++++++++++++++++++++++++++

Sometimes it is useful to pass an extra value to the callback, if you have several widgets, where you want to use
the same callback. This can be done using ``lambda``.

    .. code-block:: python    
        :caption: Example: display which button was pressed

        def button_callback(name):
            screen.text("Button %s pressed" % name)

        but1 = Button((40,40),(80,80),but_text="1",callback = lambda : button_callback("One")
        but2 = Button((130,40),(80,80),but_text="2",callback = lambda : button_callback("Two")
        but3 = Button((220,40),(80,80),but_text="3",callback = lambda : button_callback("Three")

If the callback should be passed a value from the widget, then you need to use the form ``lambda x:`` as below.

    .. code-block:: python    
        :caption: Example: display which slider has changed

        def slider_callback(value,name):
            screen.text((160,50),"Slider %s: %d" % (name,int(value))

        sld1 = Slider((0,100),(200,20),max_val=200,change_callback = lambda x: slider_callback(x,"1"))
        sld2 = Slider((0,140),(200,20),max_val=200,change_callback = lambda x: slider_callback(x,"2"))
        sld3 = Slider((0,180),(200,20),max_val=200,change_callback = lambda x: slider_callback(x,"3"))

For more information about ``lambda`` the `Mouse vs Python blog <http://www.blog.pythonlibrary.org/2010/07/19/the-python-lambda/>`_ is a good summary of the subject.



