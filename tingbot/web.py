import zmq

class webhook(object):
    def __init__(self, hook_name, hook_domain = None):
        # Default to Tingbot's public hook domain
        self.hook_domain = hook_domain if hook_domain is not None else "webhook.tingbot.com"
        self.hook_name = hook_name

        ensure_setup(self.hook_domain)

    def __call__(self, f):
        register_webhook(self.hook_name, f)
        return f

is_setup = False
zmq_subscriber = None
registered_webhooks = {}

def ensure_setup(hook_domain):
    global is_setup
    if not is_setup:
        setup(hook_domain)
        is_setup = True

def setup(hook_domain):
    global zmq_subscriber

    ctx = zmq.Context.instance()
    zmq_subscriber = ctx.socket(zmq.SUB)
    zmq_subscriber.connect("tcp://%s:20452" % (hook_domain))

    from tingbot.run_loop import main_run_loop
    main_run_loop.add_wait_callback(run_loop_wait)

def register_webhook(hook_name, callback):
    registered_webhooks[hook_name] = callback
    zmq_subscriber.setsockopt(zmq.SUBSCRIBE, hook_name)

def run_loop_wait():
    try:
        topic, data = zmq_subscriber.recv_multipart(flags=zmq.NOBLOCK)
    except zmq.ZMQError, e:
        if e.errno == zmq.EAGAIN:
            pass  # no message was ready
        else:
            raise
    else:
        from tingbot.utils import call_with_optional_arguments

        if topic in registered_webhooks:
            callback = registered_webhooks[topic]
            call_with_optional_arguments(callback, data=data)
