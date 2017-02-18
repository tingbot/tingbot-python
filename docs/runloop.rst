⏱ Run loop
-----------

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

.. py:decorator:: once(hours=0, minutes=0, seconds=0)

    This decorator will call the function marked once, after the duration specified.
    
.. py:function:: tingbot.RunLoop.call_after(callable)

    Call function ``callable`` at the next possible moment from the run loop. This allows threads
    to communicate with the main run loop in a thread-safe fashion
