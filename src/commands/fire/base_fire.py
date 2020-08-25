import json
from enum import Enum

from pyframework.providers.cli.command import Command
from pyframework.providers.rabbitmq.amqp_queue import AMQPQueue


class Event(Enum):
    # Actions.
    PLACE_DOWNLOAD_ACTION = "download.place.ready.action"
    INFO_DOWNLOAD_ACTION = "download.info.ready.action"

    # Tasks.
    PLACE_DOWNLOAD_TASK = "download.place.ready.task"
    INFO_DOWNLOAD_TASK = "download.info.ready.task"


class BaseFire(Command):
    """Base class interface to fire events from commands. """

    @staticmethod
    def _fire_event(event: Event, body: dict):
        """Fire an event with the params 'body'. """
        amqp = AMQPQueue()

        # Format data.
        event_name = event.value

        # Print Info.
        Command.info_time('Fire event:\"' + event_name + '\".')
        Command.info_time('Body:\"' + json.dumps(body) + '\".')

        # Fire event.
        amqp.fire(event_name, body)
