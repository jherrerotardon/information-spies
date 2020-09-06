from pyframework.commands.task import Task
from pyframework.components.guid import Guid
from pyframework.container import Container
from pyframework.exceptions.custom_exceptions import InvalidDataException

from ...extractors.crawler import Launcher
from ...models.city import City
from ...models.city_endpoint import CityEndpoint
from ...triggers.place_trigger import AbstractTrigger, PlaceTrigger


class DownloadPlace(Task):
    """Concrete task to download entities (restaurants) from place. """

    _name = 'download:place:ready:task'

    _place = None
    """Place data to be scrapped. """

    def set_up(self):
        super(DownloadPlace, self).set_up()

        place_id = self._payload.get('place_id')
        if place_id:
            self._place = City().get_city(place_id)

        if not self._place:
            raise InvalidDataException('Empty place. Nothing to download.')

    def run(self):
        super(DownloadPlace, self).run()

        downloads = CityEndpoint().get_downloads(self._place['id'])

        self.download_restaurants(downloads)

        return self.RETURN_SUCCESS

    def download_restaurants(self, downloads: list):
        """Downloads restaurants using downloads configurations received.

        :param downloads:
        :return:
        """
        for download in downloads:
            url = self._generate_restaurants_url(download)
            storage_file = Container().data_path() + '/' + Guid.generate()

            kwargs = {
                'endpoint': download['name'].lower(),
                'extractor_name': 'restaurants',
                'storage': storage_file,
                'endpoint_id': download['endpoint_id'],
                'city_id': download['city_id'],
            }

            Launcher.start_crawler([url], **kwargs)

    @staticmethod
    def _generate_restaurants_url(data: dict) -> str:
        """Generates URL to download restaurants.

        :param data:
        :return:
        """
        url = '{}/Restaurants-{}-{}.html'.format(
            data['url'],
            data['endpoint_code'],
            data['endpoint_name'],
        )

        return url

    def _get_trigger(self) -> AbstractTrigger:
        return PlaceTrigger()
