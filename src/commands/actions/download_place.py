from pyframework.commands.action import Action
from pyframework.exceptions.custom_exceptions import ArgumentException

from ...triggers.place_trigger import AbstractTrigger, PlaceTrigger


class DownloadPlace(Action):
    """Concrete action to download entities (restaurants) from place. """

    _place_id = None
    """Place id to be scrapped. """

    def set_up(self):
        super(DownloadPlace, self).set_up()

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
        return PlaceTrigger()
