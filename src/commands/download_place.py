from pyframework.providers.cli.command import Command
from pyframework.helpers.configuration import config
from src.models.city import City
from ..processor.crawl_restaurants import CrawlRestaurants


class DownloadPlace(Command):
    _name = 'downloadPlace'

    _description = 'Generate tasks to download entities from a place.'

    _arguments = [
        ['-p', '--place', 'Place name to download entities.']
    ]

    _options = [
        ['-a', '--all', 'Download all places in database.']
    ]

    _download_all = False
    """Flag to download all places or not. """


    def set_up(self):
        self._download_all = self.get_argument('all', False)

    def handle(self) -> int:
        self.info_time("Finding places...")

        config('queue.params')

        cities = City().get_city(2)
        # processor = CrawlRestaurants().run()

        return Command.RETURN_SUCCESS
