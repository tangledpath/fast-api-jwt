import sys
from .commands import Commands


def command_handler(message, context):
    return Commands.process_command(message)
