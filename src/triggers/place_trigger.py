from pyframework.triggers.abstract_trigger import AbstractTrigger

from src.commands.fire.base_fire import Event


class PlaceTrigger(AbstractTrigger):
    ACTION_KEY_PREFIX = AbstractTrigger.ACTION_KEY_PREFIX + ':' + 'download'
    EVENT_TASK = Event.PLACE_DOWNLOAD_TASK.value
    EVENT_ACTION = Event.PLACE_DOWNLOAD_ACTION.value
