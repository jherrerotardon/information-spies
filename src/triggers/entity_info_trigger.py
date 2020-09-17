from pyframework.triggers.abstract_trigger import AbstractTrigger

from src.commands.fire.base_fire import Event


class EntityInfoTrigger(AbstractTrigger):
    ACTION_KEY_PREFIX = AbstractTrigger.ACTION_KEY_PREFIX + ':' + 'download'
    EVENT_TASK = Event.ENTITY_DOWNLOAD_TASK.value
    EVENT_ACTION = Event.RESTAURANTS_INFO_DOWNLOAD_ACTION.value
