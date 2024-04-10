import json
import sys

from loguru import logger

from .commands import Commands


def command_handler(message, context):
    attrs = message['MessageAttributes']
    print(f"attrs: {attrs}")
    msg = {
        'command': attrs['command']['StringValue'],
        'payload': json.loads(attrs['payload']['StringValue']),
    }
    logger.info(f"Handling message in lambda function: {msg}")
    return Commands.process_command(message=msg)
