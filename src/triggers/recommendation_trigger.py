from pyframework.triggers.abstract_trigger import AbstractTrigger

from src.commands.fire.base_fire import Event


class RecommendationTrigger(AbstractTrigger):
    ACTION_KEY_PREFIX = AbstractTrigger.ACTION_KEY_PREFIX + ':' + 'download'
    EVENT_TASK = Event.RECOMMENDATION_DOWNLOAD_TASK.value
    EVENT_ACTION = Event.RECOMMENDATION_DOWNLOAD_ACTION.value
