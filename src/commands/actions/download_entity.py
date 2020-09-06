from pyframework.commands.action import Action
from pyframework.exceptions.custom_exceptions import ArgumentException

from ...triggers.place_trigger import AbstractTrigger, PlaceTrigger


class DownloadEntity(Action):
    """Concrete action to download entities (restaurants) from place. """

    _name = 'download.place.ready.action'

    _entity_id = None
    """Place id to be scrapped. """

    def set_up(self):
        super(DownloadEntity, self).set_up()

        self._entity_id = self._payload.get('entoty_id')
        if not self._entity_id:
            raise ArgumentException("No city to be scrapped.")

    def _generate_tasks(self) -> list:
        task = {
            'id': '0',  # Unique task. Is not important.
            'guid': self._guid,
            'entity_id': self._entity_id,
        }

        return [task]

    def _get_trigger(self) -> AbstractTrigger:
        return PlaceTrigger()
