from pyframework.exceptions.custom_exceptions import ArgumentException
from pyframework.helpers.lists import array_column

from .base_fire import BaseFire, Event
from ...models.city_endpoint import CityEndpoint
from ...models.restaurant import Restaurant


class FireRestaurantsInfoDownload(BaseFire):
    _name = 'fire:restaurantsInfoDownload'

    _description = 'Launch an event to download entity information.'

    _arguments = [
        ['-e', '--endpoint', 'Endpoint ID to be fired.'],
        ['-c', '--city', 'City ID to be fired.'],
    ]

    _city_id = int
    """City to be downloaded. """

    _restaurants = []
    """Restaurants to be downloaded. """

    _endpoint_id = int
    """Endpoint to be downloaded. """

    def set_up(self):
        self._city_id = self.get_argument('city')
        if not self._city_id:
            raise ArgumentException('City ID is required.')

        self._city_id = int(self._city_id)

        self._endpoint_id = self.get_argument('endpoint')
        if self._endpoint_id is None:
            raise ArgumentException('Endpoint ID is required.')

        self._endpoint_id = int(self._endpoint_id)

        download = CityEndpoint().get_downloads(self._city_id)
        if not any([self._endpoint_id == task['endpoint_id'] for task in download]):
            raise ArgumentException('Endpoint {} not enabled on city {}.'.format(self._endpoint_id, self._city_id))

        self._restaurants = Restaurant().get_restaurants_on_city(self._city_id)

    def handle(self) -> int:
        info = {
            'restaurants_ids': array_column(self._restaurants, 'id'),
            'endpoint_id': self._endpoint_id,
        }

        self._fire_event(Event.RESTAURANTS_INFO_DOWNLOAD_ACTION, info)

        return self.RETURN_SUCCESS
