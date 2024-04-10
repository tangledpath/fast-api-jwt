import os

from fast_api_jwt.commands.mqs.message_queue_facade_base import MessageQueueFacadeBase
from fast_api_jwt.commands.mqs.message_queue_facade_bunny import BunnyMQFacade
from fast_api_jwt.commands.mqs.message_queue_facade_sqs import SQSMQFacade


class MessageQueue:
    """
    This class controls the usage of different message queues (depending on environment).
    Simply instantiate the MessageQueue and call mq_facade to obtain the appropriate
    message queue for your environment.
    """

    def __init__(self):
        fast_api_env = os.getenv('FAST_API_ENV', 'development')
        if fast_api_env == 'production':
            sqs_queue_name = os.getenv('AWS_SQS_QUEUE_NAME')
            self.mq = SQSMQFacade(sqs_queue_name)
        else:
            self.mq = BunnyMQFacade(name=fast_api_env)

    def mq_facade(self) -> MessageQueueFacadeBase:
        return self.mq
