"""Module to implements Crawlers. """

import pickle
from logging import getLogger, INFO

from pyframework.components.validators import URLValidator
from pyframework.container import Container
from scrapy import Spider, Request, signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from .factory import Factory as ExtractorFactory
from ..processor.factory import Factory as ProcessorFactory


class Launcher:
    """Class to launch crawlers dynamically. """

    @staticmethod
    def start_crawler(urls: list, **kwargs):
        """Instance and launches an extractor.

        :param urls:
        :param kwargs:
        :return:
        """
        extractor = ExtractorFactory.get_class(**kwargs)

        process = CrawlerProcess(get_project_settings())
        process.crawl(extractor, urls, **kwargs)
        process.start()


class Crawler(Spider):
    name = 'Crawler'

    _storage = 'storage.pickle'

    _urls = []
    """Urls to parse."""

    _items = []
    """List where temporal save extraction data while
    crawler is running."""

    _batch = 100
    """Number of items to keep in memory before be stored. """

    _page = 0
    """Counter for crawlers with some pages to need visit. """

    _save_evidences = False
    """Flag to storage raw extracted evidences."""

    _processor = None
    """Specific processor to extract info from raw data. """

    def __init__(self, urls: list, **kwargs):
        super(Crawler, self).__init__()

        self._urls += urls
        self._storage = kwargs.get('storage', self._storage)

        self.logger.setLevel(INFO)
        getLogger('scrapy').setLevel(INFO)

        self._instance_processor()

    def _instance_processor(self):
        # Instance processor
        current_module = self.__module__.split('.')
        self._processor = ProcessorFactory.get_class(**{
            'endpoint': current_module[-2],
            'extractor_name': current_module[-1]
        })

    def item_scraped(self, item):
        self._items.append(item)

        self.logger.debug('Item extracted => {:d}.'.format(len(self._items)))

        if len(self._items) >= self._batch:
            self._storage_items()

    def _storage_items(self):
        """Storage and release memory.

        Save in secure storage items scrapped and
        release self._items list.
        By default, items will be storage in self._storage.

        :return:
        """
        with open((Container()).data_path() + '/' + self._storage, 'w') as file:
            pickle.dump(self._items, file=file)

    def engine_stopped(self):
        self._storage_items()

    def start_requests(self):
        # Do something with urls if is necessary.
        for url in self._urls:
            if not URLValidator.is_valid(url):
                self.logger.error('Invalid url -> ({}). Do nothing for this.')
                continue

            yield Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        if self._save_evidences:
            self._storage_evidence(response.text)

    def _storage_evidence(self, content):
        path = '{}/{}_{}.html'.format((Container()).data_path(), self.name, self._page)

        with open(path, 'wb') as file:
            file.write(content)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(Crawler, cls).from_crawler(crawler, *args, **kwargs)

        crawler.signals.connect(
            spider.item_scraped,
            signal=signals.item_scraped)
        crawler.signals.connect(
            spider.engine_stopped,
            signal=signals.engine_stopped)

        return spider
