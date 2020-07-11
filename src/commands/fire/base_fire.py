import json
from enum import Enum

from pyframework.providers.cli.command import Command
from pyframework.providers.rabbitmq.amqp_queue import AMQPQueue


class Event(Enum):
    CITY_DOWNLOAD = "city.download"


class BaseFire(Command):

    @staticmethod
    def _fire_event(event: Event, body: dict):
        amqp = AMQPQueue()

        # Format data.
        event_name = event.value
        body = json.dumps(body)

        # Print Info.
        Command.info_time('Fire event:\"' + event_name + '\".')
        Command.info_time('Body:\"' + body + '\".')

        # Fire event.
        amqp.fire(event_name, body)
