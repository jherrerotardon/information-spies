from pyframework.commands.task import Task
from pyframework.components.guid import Guid
from pyframework.container import Container
from pyframework.exceptions.custom_exceptions import InvalidDataException

from ...extractors.crawler import Launcher
from ...models.endpoint import Endpoint
from ...models.restaurant import Restaurant
from ...triggers.entity_info_trigger import AbstractTrigger, EntityInfoTrigger


class DownloadEntity(Task):
    """Concrete task to download entities (restaurants) from place. """

    _name = 'download:entity:ready:task'

    _endpoint = None
    """Endpoint data to be scrapped. """

    _entity = None
    """Entity data to be scrapped. """

    def set_up(self):
        super(DownloadEntity, self).set_up()

        endpoint_id = self._payload.get('endpoint_id')
        if endpoint_id:
            self._endpoint = Endpoint().get_endpoint(endpoint_id)

        if not self._endpoint:
            raise InvalidDataException('Empty endpoint. Nothing to download.')

        entity_id = self._payload.get('entity_id')
        if entity_id:
            self._entity = Restaurant().get_restaurant(entity_id)

        if not self._entity:
            raise InvalidDataException('Empty entity. Nothing to download.')

    def run(self):
        super(DownloadEntity, self).run()

        self.download_reviews()

        return self.RETURN_SUCCESS

    def download_reviews(self):
        """Downloads reviews and hotel info from entity loaded.

        :return:
        """
        url = self._generate_restaurant_url()
        storage_file = Container().data_path() + '/' + Guid.generate()

        kwargs = {
            'endpoint': self._endpoint['name'].lower(),
            'extractor_name': 'entity',
            'storage': storage_file,
            'entity_id': self._entity['id'],
        }

        Launcher.start_crawler([url], **kwargs)

    def _generate_restaurant_url(self) -> str:
        """Generates URL to download restaurant info.

        :return:
        """
        url = '{}{}'.format(
            self._endpoint['url'],
            self._entity['url'],
        )

        url = 'https://www.tripadvisor.es/Restaurant_Review-g187493-d12952582-Reviews-or10-Sibuya_Urban_Sushi_Bar_Salamanca-Salamanca_Province_of_Salamanca_Castile_a.html'

        return url

    def _get_trigger(self) -> AbstractTrigger:
        return EntityInfoTrigger()
