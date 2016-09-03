⚡️ Webhooks
----------

You can push data to Tingbot using webhooks.

Here is an example that displays SMS messages using `If This Then That <http://ifttt.com>`_. See
our `tutorial video <https://www.youtube.com/watch?v=yZg8OIzVByM>`_ to see how to set up IFTTT with
webhooks.

.. code-block:: python

    import tingbot
    from tingbot import *

    screen.fill(color='black')
    screen.text('Waiting...')

    @webhook('demo_sms')
    def on_webhook(data):
        screen.fill(color='black')
        screen.text(data, color='green')

    tingbot.run()

.. py:decorator:: webhook(webhook_name…)

    This decorator calls the marked function when a HTTP POST request is made to the URL
    :samp:`http://webhook.tingbot.com/{webhook_name}`. The POST data of the URL is available to the marked
    function as the ``data`` parameter.

    The data is limited to 1kb, and the last value that was POSTed is remembered by the server,
    so you can feed in relatively slow data sources.

You can use webhooks to push data to Tingbot, or to notify Tingbot of an update that happened
elsewhere on the internet.


.. hint::

    `IFTTT <http://ifttt.com>`_ is a great place to start for ideas for webhooks. 
    `Slack <http://slack.com>`_ also has native support for webhooks!
