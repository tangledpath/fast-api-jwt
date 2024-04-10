import json
import os
import time
import uuid
from threading import Thread
from typing import Dict, Any

import boto3
from loguru import logger


class AppMessageQueue:
    """
    A thin layer over the AWS SQS (Simple Queue Service)
    """
    fast_api_env = os.getenv('FAST_API_ENV', 'development')
    queue_name = os.getenv('AWS_SQS_QUEUE_NAME')
    print("queue_name", queue_name)
    endpoint_url = os.getenv("AWS_ENDPOINT_URL", None)
    queue_url = None
    sqs_boto_client = None
    mq_thread = None
    stopping = False

    @classmethod
    def initialize(cls):
        """ Initialize AppMessageQueue """
        print(f"Initializing AppMessageQueue")
        if not cls.queue_name:
            raise ValueError('Queue name is required (set on AWS_SQS_QUEUE_NAME env variable)')
        cls.sqs_boto_client = boto3.client('sqs', endpoint_url=cls.endpoint_url)
        logger.info(f"Created boto client[{type(cls.sqs_boto_client)}]: {cls.sqs_boto_client}")

        # Get URL for our message queue:
        cls.__start_queue()

    @classmethod
    def send_message(cls, command: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """ The SQS send_message implementation """
        message = cls.__build_message_params(command, payload)
        response = cls.sqs_boto_client.send_message(**message)
        return response

    @classmethod
    def shutdown(cls) -> None:
        """
        Shut down gracefully.
        """
        if not cls.stopping and cls.fast_api_env != 'production' and cls.mq_thread:
            cls.stopping = True
            if cls.queue_url:
                for i in range(5):
                    response = cls.sqs_boto_client.get_queue_attributes(
                        QueueUrl=cls.queue_url,
                        AttributeNames=[
                            'ApproximateNumberOfMessages',
                        ]
                    )
                    msg_count = response['Attributes']['ApproximateNumberOfMessages']
                    if msg_count == 0:
                        logger.info("No messages remaining; allowing shutdown...")
                        break
                    time.sleep(1.0)
            cls.mq_thread.join(timeout=5)

    @classmethod
    def __build_message_params(cls, command: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get SQS message params from the message; using the command and message parameters.

        return: The message params as a dictionary
        """
        msg = {
            'MessageAttributes': {
                'command': {
                    'DataType': 'String',
                    'StringValue': command,
                },
                'message': {
                    'DataType': 'String',
                    'StringValue': json.dumps(payload),
                },
            },
            'MessageBody': command,
            'MessageDeduplicationId': str(uuid.uuid4()),
            'MessageGroupId': str(uuid.uuid4()),
            'QueueUrl': cls.queue_url,
        }

        return msg

    @classmethod
    def __start_queue(cls):

        # In production, SQS messages will automatically invoke our lambda function.
        # In other environments, we will have to receive them and forward to our lambda fn:
        cls.__create_queue()
        response = cls.sqs_boto_client.get_queue_url(QueueName=cls.queue_name)
        cls.queue_url = response['QueueUrl']
        if not cls.queue_url:
            raise RuntimeError(f"No Queue URL found for {cls.queue_name}.")
        logger.info(f"Using SQS Queue URL: {cls.queue_url}")
        cls.mq_thread = Thread(target=cls.__process_queue)
        cls.mq_thread.start()

    @classmethod
    def __process_queue(cls):
        from fast_api_jwt.commands.lambda_handler import command_handler

        while not cls.stopping:
            # Get message:
            response = cls.sqs_boto_client.receive_message(
                QueueUrl=cls.queue_url,
                MessageAttributeNames=['All'],
                MaxNumberOfMessages=1,
                VisibilityTimeout=0,
                WaitTimeSeconds=0
            )
            if 'Messages' in response:
                logger.info(f"Received response from receive_message: {response['Messages']}")
                message = response['Messages'][0]
                receipt_handle = message['ReceiptHandle']
                if message:
                    logger.info(f"Invoking lambda function with: {message}")
                    command_handler(message=message, context=None)

                # Remove message:
                cls.sqs_boto_client.delete_message(
                    QueueUrl=cls.queue_url,
                    ReceiptHandle=receipt_handle
                )
                print('Received and deleted message: %s' % message)
            else:
                time.sleep(1.0)

    @classmethod
    def __create_queue(cls):
        if cls.fast_api_env != 'production':
            try:
                cls.sqs_boto_client.create_queue(
                    QueueName=cls.queue_name,
                    Attributes={
                        "ContentBasedDeduplication": 'true',
                        'VisibilityTimeout': '360',
                        'MessageRetentionPeriod': '300',
                        "FifoQueue": 'true'
                    })
            except BaseException as err:
                logger.error(
                    f"[{type(err)}] Error creating queue:{cls.queue_name} endpoint:{cls.endpoint_url}.  Error: {err}")
