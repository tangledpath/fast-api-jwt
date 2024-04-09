import json
import uuid
from typing import Dict, Any

import boto3

from fast_api_jwt.commands.mqs.message_queue_facade_base import MessageQueueFacadeBase


class SQSMQFacade(MessageQueueFacadeBase):
    """ Facade for AWS SQS MQ; containing the proper implementation of
        send_message to send the message to the AWS SQS Queue """

    def __init__(self, queue_name: str) -> None:
        """ Constructor for SQSMQFacade """

        # Construct base class:
        super().__init__()

        # Setup SQS to prepare for sending a mecsssage:
        self.queue_name = queue_name
        self.sqsBotoClient = boto3.client('sqs')

        # Get URL for our message queue:
        response = self.sqsBotoClient.get_queue_url({'QueueName': self.queue_name})
        self.queue_url = response['QueueUrl']

    def send_message(self, payload: Dict[str, Any]) -> None:
        """ The SQS send_message implementation """
        response = self.sqsBotoClient.send_message(**self.get_message_params(payload))
        return response

    def get_message_params(self, payload: Dict[str, Any]):
        """ Get SQS message params from the payload """
        msg = {
            'MessageAttributes': {
                'command': {
                    'DataType': 'String',
                    'StringValue': payload['command'],
                },
            },
            'MessageDeduplicationId': uuid.uuid4(),
            'MessageGroupId': uuid.uuid4(),
            'QueueUrl': self.queueUrl,
            'MessageBody': json.dumps(payload)
        }

        return msg

        response = self.sqsBotoClient.send_message(
            QueueUrl=self.queue_url,
            MessageBody='string',
            DelaySeconds=123,
            MessageAttributes={
                'string': {
                    'StringValue': 'string',
                    'BinaryValue': b'bytes',
                    'StringListValues': [
                        'string',
                    ],
                    'BinaryListValues': [
                        b'bytes',
                    ],
                    'DataType': 'string'
                }
            },
            MessageSystemAttributes={
                'string': {
                    'StringValue': 'string',
                    'BinaryValue': b'bytes',
                    'StringListValues': [
                        'string',
                    ],
                    'BinaryListValues': [
                        b'bytes',
                    ],
                    'DataType': 'string'
                }
            },
            MessageDeduplicationId='string',
            MessageGroupId='string'
        )
