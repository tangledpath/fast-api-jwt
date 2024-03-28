from python_bunny_mq.bunny_mq import BunnyMQ

class BunnyQueue(BunnyMQ):
    def __init__(self):
        super().__init__()

    def setup_handlers(self):
        """ Setup handlers for this queue """
        pass
