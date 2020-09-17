from pyframework.commands.action import Action
from pyframework.exceptions.custom_exceptions import ArgumentException

from ...triggers.recommendation_trigger import RecommendationTrigger, AbstractTrigger


class Recommend(Action):
    """Concrete action to do recommendations. """

    _name = 'recommendation.ready.action'

    _user_id = None
    """User ID id to do recommendation. """

    def set_up(self):
        super(Recommend, self).set_up()

        self._place_id = self._payload.get('place_id')
        if not self._place_id:
            raise ArgumentException("No city to be scrapped.")

    def _generate_tasks(self) -> list:
        task = {
            'id': '0',  # Unique task. Is not important.
            'guid': self._guid,
            'place_id': self._place_id,
        }

        return [task]

    def _get_trigger(self) -> AbstractTrigger:
        return RecommendationTrigger()
