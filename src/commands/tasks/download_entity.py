from pyframework.commands.task import Task
from pyframework.exceptions.custom_exceptions import InvalidDataException

from ...models.city import City
from ...triggers.place_trigger import AbstractTrigger, PlaceTrigger


class DownloadEntity(Task):
    """Concrete task to download entities (restaurants) from place. """

    _name = 'download:place:ready:task'

    _place = None
    """Place data to be scrapped. """

    def set_up(self):
        super(DownloadEntity, self).set_up()

        place_id = self._payload.get('place_id')
        if place_id:
            self._place = City().get_city(place_id)

        if not self._place:
            raise InvalidDataException('Empty place. Nothing to download.')

    def run(self):
        super(DownloadEntity, self).run()

        self.download_reviews({})

        return self.RETURN_SUCCESS

    def download_reviews(self, data: dict):
        """Downloads reviews using downloads configurations received.

        :param data:
        :return:
        """
        pass

    @staticmethod
    def _generate_restaurant_url(data: dict) -> str:
        """Generates URL to download restaurants.

        :param data:
        :return:
        """
        url = ''

        return url

    def _get_trigger(self) -> AbstractTrigger:
        return PlaceTrigger()
