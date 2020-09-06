from pyframework.exceptions.custom_exceptions import ArgumentException

from .base_fire import BaseFire, Event
from ...models.restaurant import Restaurant


class FireEntityDownload(BaseFire):
    _name = 'fire:cityDownload'

    _description = 'Launch an event to download entity information.'

    _arguments = [
        ['-e', '--entity', 'Entity ID to be fired.']
    ]

    _restaurant = {}

    def set_up(self):
        entity_id = self.get_argument('entity')
        if not entity_id:
            raise ArgumentException('Entity ID is required.')

        self._restaurant = Restaurant().get_restaurant(entity_id)
        if not self._restaurant:
            raise ArgumentException('No valid entity ID.')

    def handle(self) -> int:
        info = {
            'place_id': self._restaurant['id']
        }

        self._fire_event(Event.ENTITY_DOWNLOAD_ACTION, info)

        return self.RETURN_SUCCESS
