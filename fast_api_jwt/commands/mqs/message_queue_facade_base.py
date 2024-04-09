from abc import ABC
from typing import Any, Dict


class MessageQueueFacadeBase(ABC):
    """
    Generic "interface" for a single command of a message queue
    implementation, namely the sendMessage implementation.  This
    allows use to use different queues for different environments.

    For example, in production, you might use the SQSMQFacade to invoke lambda functions
    via an SQS event.  In development in test, you would probably use the BunnyMQFacade
    as it has no dependencies and no separate runtime environment.
    """

    def send_message(self, payload: Dict[str, Any]) -> None:
        """
             Derived clases should implement this method to send a message
             for the represented Message Queue
        """
        self.bunny_mq.send_message(payload)
