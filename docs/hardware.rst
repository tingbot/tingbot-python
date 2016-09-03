📟 Hardware
-----------

There are several useful functions that can be used to see if hardware is connected to the tingbot.

.. py:function:: get_ip_address()

    Returns the IP address of the tingbot or None if it is not connected.

.. py:function:: get_wifi_cell()

    Returns a WifiCell object (or None if there is no wifi adapter).

    A WifiCell object has the following attributes:

    * ssid
    * link_quality
    * signal_level
        
.. py:function:: mouse_attached()
    
    Returns True if a mouse is attached
    
.. py:function:: keyboard_attached()
    
    Returns True if a keyboard is attached
    
.. py:function:: joystick_attached()
    
    Returns True if a joystick is attached
