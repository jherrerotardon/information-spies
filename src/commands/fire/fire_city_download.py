from pyframework.exceptions.custom_exceptions import ArgumentException

from .base_fire import BaseFire, Event
from ...models.city import City


class FireCityDownload(BaseFire):
    _name = 'fire:cityDownload'

    _description = 'Launch an event to download entities info from city.'

    _arguments = [
        ['-c', '--city', 'City ID to be fired.']
    ]

    _city = {}

    def set_up(self):
        city_id = self.get_argument('city')
        if not city_id:
            raise ArgumentException('City ID is required.')

        self._city = City().get_city(city_id)
        if not self._city:
            raise ArgumentException('No valid city ID.')

    def handle(self) -> int:
        info = {
            'place_id': self._city['id']
        }

        self._fire_event(Event.PLACE_DOWNLOAD_ACTION, info)

        return self.RETURN_SUCCESS
