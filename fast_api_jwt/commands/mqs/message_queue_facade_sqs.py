import json
import os
import uuid
from typing import Dict, Any

import boto3

from fast_api_jwt.commands.mqs.message_queue_facade_base import MessageQueueFacadeBase


class SQSMQFacade(MessageQueueFacadeBase):
    """
    Facade for AWS SQS MQ; containing the proper implementation of
    send_message to send the message to the AWS SQS Queue
    """

    def __init__(self, queue_name: str) -> None:
        """ Constructor for SQSMQFacade """

        # Construct base class:
        super().__init__()

        # Setup SQS to prepare for sending a message:
        self.queue_name = queue_name
        endpoint_url = os.getenv("AWS_ENDPOINT_URL", None)
        self.sqsBotoClient = boto3.client('sqs', endpoint_url=endpoint_url)

        # Get URL for our message queue:
        response = self.sqsBotoClient.get_queue_url({'QueueName': self.queue_name})
        self.queue_url = response['QueueUrl']

    def send_message(self, command: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """ The SQS send_message implementation """
        message = self.build_message_params(command, payload)
        response = self.sqsBotoClient.send_message(**message)
        return response

    def build_message_params(self, command: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """ Get SQS message params from the payload """
        msg = {
            'MessageAttributes': {
                'command': {
                    'DataType': 'String',
                    'StringValue': command,
                },
            },
            'MessageDeduplicationId': uuid.uuid4(),
            'MessageGroupId': uuid.uuid4(),
            'QueueUrl': self.queueUrl,
            'MessageBody': json.dumps(payload)
        }

        return msg
