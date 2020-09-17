from pyframework.commands.action import Action
from pyframework.exceptions.custom_exceptions import ArgumentException

from ...triggers.entity_info_trigger import EntityInfoTrigger, AbstractTrigger


class DownloadEntity(Action):
    """Concrete action to download entities (restaurants) from place. """

    _name = 'download.info.ready.action'

    _entities_ids = []
    """Entities ids to be scrapped. """

    _endpoint_id = int
    """Endpoint to be downloaded. """

    def set_up(self):
        super(DownloadEntity, self).set_up()

        if 'endpoint_id' not in self._payload:
            raise ArgumentException('Endpoint ID is required.')

        self._entities_ids = self._payload.get('restaurants_ids', [])

    def _generate_tasks(self) -> list:
        tasks = [{
            'id': entity_id,
            'guid': self._guid,
            'entity_id': entity_id,
            'endpoint_id': self._payload['endpoint_id'],
        } for entity_id in self._entities_ids]

        return tasks

    def _get_trigger(self) -> AbstractTrigger:
        return EntityInfoTrigger()
