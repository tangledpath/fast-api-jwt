from typing import Any, Dict

from python_bunny_mq.bunny_mq import BunnyMQ

from .message_queue_facade_base import MessageQueueFacadeBase
from ..commands import Commands


class BunnyMQFacade(MessageQueueFacadeBase):
    """
    Lightweight, no-dependency, intraprocess, multithreaded message queue.
    """

    def __init__(
            self,
            name: str = BunnyMQ.DEFAULT_NAME,
            timeout: float = 1.0,
            interval: float = 1.0,
            grace_period: float = 15.0
    ):
        """ Initializes bunny message queue facade """
        # Construct base class:
        super().__init__()

        self.commands = Commands()

        # Construct bunny message queue:
        self.bunny = BunnyMQ(
            name=name,
            timeout=timeout,
            interval=interval,
            grace_period=grace_period
        )
        self.bunny.register_handler(BunnyMQ.WILDCARD_HANDLER, self.message_handler)
        self.bunny.execute()

    def send_message(self, command: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """ send_message interface for BunnyMQ """
        return self.bunny.send_message(command, message)

    def message_handler(self, payload: Dict[str, Any]) -> Any:
        """
        The Bunny MQ message_handler implementation; forwards message
        to the lambda handler for this app
        """
        return self.commands.process_command(payload)
