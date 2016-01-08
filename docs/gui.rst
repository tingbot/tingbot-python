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
        
        style = gui.get_default_style()
        style.bg_color = "blue"

2. Use a custom style. This allows you to customize individual widgets or groups of widgets

   .. code-block:: python
        :caption: Example: create two buttons with a smaller font size 
        
        custom_style = gui.Style(button_text_font_size = 12)
        button1 = gui.Button((50,50),(80,80),label="Small text",style=custom_style)
        button2 = gui.Button((150,50),(80,80),label="Small again",style=custom_style)
        button3 = gui.Button((250,50),(80,80),label="OK")
        
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

.. py:class:: Button(xy, size, align="center", parent=None, style=None, label="OK", callback=None)

    Base: :class:`Widget`

    A simple button control

    :param xy: position that the button will be drawn
    :param size: size of the button
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this button. If None, button will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this button. If None, the button will have the default style
    :param label: Text to display on button
    :param callable callback: function to call when the button is pressed. It should not take any arguments
    
    :Attributes:
        - *label* -- Text to be displayed on the button.
        - *callback* -- Function to be called when button is clicked. No arguments passed. 
          See `Callbacks`_ for more information
        
    :Style Attributes:
        - *bg_color* -- background color
        - *button_color* -- color of this button when not pressed
        - *button_pressed_color* -- color to use when button pressed
        - *button_rounding* -- rounding in pixels of button corners. use 0 for square corners
        - *button_text_color* -- color to use for text
        - *button_text_font* -- font to use (default)
        - *button_text_font_size* -- font size to use
    
.. py:class:: ToggleButton(xy, size, align="center", parent=None, style=None, label="OK", callback=None)

    Base: :class:`Widget`

    A button which can be in an on or off state
    
    :param xy: position that the button will be drawn
    :param size: size of the button
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this button. If None, button will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this button. If None, the button will have the default style
    :param label: Text to display on button
    :param callable callback: function to call when the button is pressed. It should accept a single boolean value
    
    :Attributes:
        - *label* -- Text to be displayed on the button.
        - *pressed* -- Current state of the button. True if pressed, False if not
        - *callback* -- Function to be called when button is clicked. A boolean value is passed which is the current state of the button.
          See `Callbacks`_ for more information
        
    :Style Attributes:
        - *bg_color* -- background color
        - *button_color* -- color of this button when not pressed
        - *button_pressed_color* -- color to use when button pressed
        - *button_rounding* -- rounding in pixels of button corners. use 0 for square corners
        - *button_text_color* -- color to use for text
        - *button_text_font* -- font to use (default)
        - *button_text_font_size* -- font size to use

.. py:class:: StaticText(xy, size, align="center", parent=None, style=None, label="", text_align="center")

    Base: :class:`Widget`

    A static text control

    :param xy: position that the text widget will be drawn
    :param size: size of the area for text
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this text. If None, text will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this text. If None, the text will have the default style
    :param label: Text to display
    :param text_align: alignment of text within the widget
    
    :Attributes:
         - *label* -- text
         - *text_align* -- alignment of the text

    :Style Attributes:
        - *bg_color* -- background color
        - *statictext_color* -- color to use for text
        - *statictext_font* -- font to use (default)
        - *statictext_font_size* -- font size to use
        
       
.. py:class:: CheckBox(xy, size, align="center", parent=None, style=None, label="OK", callback=None)

    Base: :class:`Widget`

    A checkbox control

    :param xy: position that the checkbox will be drawn
    :param size: size of the checkbox
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this checkbox. If None, checkbox will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this checkbox. If None, the checkbox will have the default style
    :param label: Text to display
    :param callable callback: function to call when the button is pressed. Is passed True if checkbox ticked, False otherwise
    
    :Attributes:
        - *label* -- Text to be displayed.
        - *value* -- Current status of the checkbox - True for checked, False for unchecked
        - *callback* -- Function to be called when the checkbox is clicked. 
          Is passed True if checkbox ticked, False otherwise
          See `Callbacks`_ for more information
        
    :Style Attributes:
        - *bg_color* -- background color
        - *checkbox_color* -- color of the checkbox
        - *checkbox_text_color* -- color to use for text
        - *checkbox_text_font* -- font to use (default)
        - *checkbox_text_font_size* -- font size to use

        
Radio Buttons
-------------

Radio buttons are similar to checkboxes, but only one in a group can be selected at any
one time. As they need to be part of a group, a :class:`RadioButton` cannot exist by itself - it
needs to be part of a :class:`RadioGroup`.
        
.. code-block:: python
    :caption: Example: create a set of radiobuttons
    
    group = gui.RadioGroup()
    radio1 = gui.RadioButton((100,80),(200,20),label="Radio 1",value=1,group=group)
    radio2 = gui.RadioButton((100,110),(200,20),label="Radio 2",value=2,group=group)
    radio3 = gui.RadioButton((100,140),(200,20),label="Radio 3",value=3,group=group)

.. py:class:: RadioGroup(callback = None)

    Base: object
    
    A group of RadioButtons
    
    :param callable callback: function to call when one of the radio buttons is pressed. Will be passed
                              two arguments - first is the buttons label, second is it's value
                              
    :Attributes:
        - *selected* -- Currently selected RadioButton
                                  
.. py:class:: RadioButton(xy, size, align="center", parent=None, style=None, label="", value=None, group=None, callback=None)

    Base: :class:`Widget`

    A radio button control

    :param xy: position that the radio button will be drawn
    :param size: size of the radio button
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this radio button. If None, radio button will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this radio button. If None, the radio button will have the default style
    :param label: Text to display
    :param value: Value for this RadioButton, set to label if not specified
    :param RadioGroup group: RadioGroup that this Button will be part of.
    :param callable callback: function to call when the button is pressed. It should not take any arguments
    
    :Attributes:
        - *label* -- text to displayed
        - *value* -- data associated with this radio button
        - *pressed* -- whether this radio button is pressed or not
        - *callback* -- function to call when the radio button is pressed. It should not take any arguments
          See `Callbacks`_ for more information
                        
    :Style Attributes:
        - *bg_color* -- background color
        - *radiobutton_color* -- color of the RadioButton
        - *radiobutton_text_color* -- color to use for text
        - *radiobutton_text_font* -- font to use (default)
        - *radiobutton_text_font_size* -- font size to use
       
.. py:class:: Slider(xy, size, align = "center", parent = None, style = None, max_val=1.0, min_val=0.0, step = None, change_callback=None)

    Base: :class:`Widget`
    
    A sliding control to allow selection from a range of values
    
    :param xy: position that the slider will be drawn
    :param size: size of the slider
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this slider. If None, slider will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this slider. If None, the slider will have the default style
    :param float max_val: maximum value for the slider
    :param float min_val: minimum value for the slider
    :param step: amount to jump by when clicked outside the slider handle. Defaults to one tenth of ``max_val-min_val``
    :param callable change_callback: function called when the slider is moved. Passed a float which is the sliders new value
    
    :Attributes:
        - *value* -- Current value of the slider
        - *change_callback* -- Function to be called when the slider is moved. A single float is passed. 
          See `Callbacks`_ for more information

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
    
    :Attributes:
        - *visible* -- True if the widget is to be displayed. Widget will be hidden if false
        - *surface* -- A pygame surface that corresponds to the widgets area - use this in the draw method
    
    .. py:method:: on_touch(self,xy,action)
        
        Override this method for any widgets that respond to touch events
        
        :param xy: position of the touch
        :param action: one of "up", "down", "move"
        
    .. py:method:: update(self,upwards=True,downwards=False)
    
        Call this method to redraw the widget. The widget will only be drawn if visible
        
        :param upwards: set to True to ask any parents (and their parents) to redraw themselves
        :param downwards: set to True to make any children  redraw themselves
        
    .. py:method:: draw(self)
    
        Called when the widget needs to draw itself. Override this method for all derived widgets    
        
        
Containers
----------

Containers can be used to group widgets together. ScrollAreas can be used to access more widgets than can fit
on the screen otherwise. 

.. py:class:: Container

    A base class for ScrollAreas
    
    .. py:method: add_child(self,widget)
    
        :param Widget widget: The widget to be added to this container
    
        Adds a widget to this container. This should rarely be called as the widget will call this itself 
        on initiation
        
    .. py:method: remove_child(self,widget)
    
        :param Widget widget: The widget to be added to this container
        
        Remove a widget from this container
        
    .. py:method: remove_all(self)
    
        Removes all widgets from the container
        
.. py:class:: Panel

    Base: :class:`Container`

    Panel class, allows you to collect together various widgets and turn on or off as needed

.. py:class:: ScrollArea(xy,size,align="center",parent=None,style = None,canvas_size=None)

    Base: :class:`Container`
    
    ScrollArea gives a viewing area into another, usually larger area. This allows the user to access more
    widgets than will fit on the display. Scrollbars will be added to the bottom or right edges as needed.

    :param xy: position that the widget will be drawn
    :param size: size of the widget
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this widget. If None, widget will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this widget. If None, the widget will have the default style
    :param canvas_size: size of the scrollable area (required)
    
    :Attributes:
        - *scrolled_area* -- Use this as the parent for any widgets you wish to place within this container
        
Callbacks
---------

Basic usage
+++++++++++

Several classes use callbacks to respond to user events. The simplest of these take no arguments

.. code-block:: python    
    :caption: Example: respond to a button press
    
    def button_callback():
        screen.text("Button pressed")

    but = gui.Button((40,40),(80,80),label="Button",callback = button_callback)
        
Notice that ``button_callback`` has no brackets when passed to the Button. Other callbacks will take a value dependent on the state of the widget.
For example, the callback for a slider will pass it's current value as a float

.. code-block:: python    
    :caption: Example: display the value of a slider
    
    def slider_callback(value):
        screen.rectangle((0,0),(320,200),"black","topleft")
        screen.text("%d" % int(value))

    slider = gui.Slider((0,200),(320,20),align="topleft",
                        max_val = 200,change_callback = slider_callback)
    
Passing extra arguments to callbacks
++++++++++++++++++++++++++++++++++++

Sometimes it is useful to pass an extra value to the callback, if you have several widgets, where you want to use
the same callback. This can be done using ``lambda``.

.. code-block:: python    
    :caption: Example: display which button was pressed

    def button_callback(name):
        screen.rectangle((0,80),(320,240),"black","topleft")
        screen.text("Button %s pressed" % name)

    but1 = gui.Button((40,40),(80,80),label="1",callback = lambda : button_callback("1"))
    but2 = gui.Button((130,40),(80,80),label="2",callback = lambda : button_callback("2"))
    but3 = gui.Button((220,40),(80,80),label="3",callback = lambda : button_callback("3"))

If the callback should be passed a value from the widget, then you need to use the form ``lambda x:`` as below.

.. code-block:: python    
    :caption: Example: display which slider has changed

    def slider_callback(value,name):
        screen.rectangle((0,0),(320,100),"black","topleft")
        screen.text("Slider %s: %d" % (name,int(value)),(160,50))

    sld1 = gui.Slider((120,110),(230,20),max_val=200,
                      change_callback = lambda x: slider_callback(x,"1"))
    sld2 = gui.Slider((120,150),(230,20),max_val=200,
                      change_callback = lambda x: slider_callback(x,"2"))
    sld3 = gui.Slider((120,190),(230,20),max_val=200,
                      change_callback = lambda x: slider_callback(x,"3"))

For more information about ``lambda`` the `Mouse vs Python blog <http://www.blog.pythonlibrary.org/2010/07/19/the-python-lambda/>`_ is a good summary of the subject.

Full example
------------

Here is a fully worked example with a Button, a ToggleButton, and a ScrollArea containing a slider, 
two checkboxes and three radio buttons

.. code-block:: python    
    :caption: Example: Full worked example
    
    from tingbot import screen,gui,run

        
    def loop():
        pass    
           
    def print_text(text):       
        screen.rectangle((160,230),(320,20),'black')
        screen.text(text,(160,230),font_size=16)
           
    def slider_cb(value):
        print_text("Slider value: %d" % int(value))

    def value_callback(name,value):
        print_text(name + " value: " + str(value))

    def pressed(name=""):
        print_text("%s pressed" % name)
        

    style = gui.get_default_style()
    style.slider_handle_color="aqua"
    screen.fill(color="black")

    but1 = gui.Button((50,30),(90,50),label="Button",callback=lambda: pressed("Button"))
    but1.update()
    but2 = gui.ToggleButton((150,30),(90,50),label="Toggle",
                            callback = lambda x: value_callback("Toggle Button",x))
    but2.update()

    panel = gui.ScrollArea((0,60),(320,160),align="topleft",canvas_size=(640,240))

    slider = gui.Slider((0,0),(200,20),align="topleft",
                        min_val=100,
                        max_val=200,
                        change_callback=slider_cb,parent=panel.scrolled_area)

    chk1 = gui.CheckBox((0,30),(200,20),align="topleft",
                        parent=panel.scrolled_area, 
                        label="Checkbox 1", 
                        callback = lambda x: value_callback("Checkbox 1",x))
    chk2 = gui.CheckBox((0,60),(200,20),align="topleft",
                        parent=panel.scrolled_area, 
                        label="Checkbox 2", 
                        callback = lambda x: value_callback("Checkbox 2",x))

    group = gui.RadioGroup(callback=value_callback)
    radio1 = gui.RadioButton((0,90),(200,20),align="topleft",
                             parent=panel.scrolled_area,
                             label="Radiobutton 1",
                             value=1,
                             group=group)
    radio2 = gui.RadioButton((0,120),(200,20),align="topleft",
                             parent=panel.scrolled_area,
                             label="Radiobutton 2",
                             value=2,
                             group=group)
    radio3 = gui.RadioButton((0,150),(200,20),align="topleft",
                             parent=panel.scrolled_area,
                             label="Radiobutton 3",
                             value=3,
                             group=group)
                             
    panel.update(downwards=True)
    run(loop)    

