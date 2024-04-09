import sys
from .commands import Commands


def handler(event, context):
    return Commands.process_command(event)
