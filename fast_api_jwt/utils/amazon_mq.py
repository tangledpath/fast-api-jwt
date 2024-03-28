import json
import os
from typing import Dict, Any

import boto3
from loguru import logger

# Load dotenv (not in production):
if os.getenv('PYTHON_ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()


class AmazonMQ:
    """Facade class for sending messages via AWS SQS"""
    def __init__(self):
        self.sqs = boto3.resource('sqs')
        queue_name = os.getenv('AWS_SQS_QUEUE_NAME')
        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        self.queue_url = self.queue.url
        logger.info(f'Using queue url: {self.queue_url}')

    def send_message(self, message:Dict[str, Any]):
        msg = self.__prepare_message(message)
        self.queue.send_message(**msg)
    def __prepare_message(self, message:Dict[str, Any]):
        return dict(
            Id=str(message['id']),
            MessageAttributes=dict(
                type={
                    'DataType': 'String',
                    'StringValue': message['action'],
                }
            ),
            MessageBody=json.stringify(message),
        )
