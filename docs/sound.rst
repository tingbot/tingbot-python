🔊 Sounds
---------

If you plug in a USB audio device into your Tingbot, you can play sounds.

.. code-block:: python
    :caption: Example: Simple sounds app
    
    import tingbot
    from tingbot import *

    sound = Sound('car_chirp.wav')

    @left_button.press
    def on_press():
        sound.play()

    @every(seconds=1.0/30)
    def draw():
        screen.fill(color='black')
        screen.text('Press the left button to play a sound.')

    tingbot.run()


.. py:class:: Sound(filename)
    
    Loads a sound ready for playing. Currently WAV and OGG files are supported.

    .. py:method:: play(loop=False)
        
        Starts the playback of the sound.

        :param bool loop: Pass ``True`` to loop the sound until ``stop()`` is called.

    .. py:method:: stop()

        Stops the sound.