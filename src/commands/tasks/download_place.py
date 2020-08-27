from pyframework.commands.task import Task
from pyframework.exceptions.custom_exceptions import InvalidDataException

from ...models.city import City
from ...triggers.place_trigger import AbstractTrigger, PlaceTrigger


class DownloadPlace(Task):
    """Concrete task to download entities (restaurants) from place. """

    _name = 'download.place.ready.task'

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

        url = self._generate_place_url()

    def _generate_place_url(self) -> str:
        code = self._place['code']

        return ''

    def _get_trigger(self) -> AbstractTrigger:
        return PlaceTrigger()
