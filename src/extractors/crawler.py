import pickle
from logging import getLogger, INFO

from pyframework.components.validators import URLValidator
from pyframework.container import Container
from scrapy import Spider, Request, signals


class Crawler(Spider):
    name = 'Crawler'

    _storage = 'storage.pickle'

    _urls = []
    """Urls to parse."""

    _items = []
    """List where temporal save extraction data while
    crawler is running."""

    _max_items = 0
    """Secure flag to limit number of items to try extract. """

    _page = 0
    """Counter for crawlers with some pages to need visit. """

    _save_evidences = False
    """Flag to storage raw extracted evidences."""

    def __init__(self, urls: list):
        super(Crawler, self).__init__()

        self._urls += urls

        self.logger.setLevel(INFO)
        getLogger('scrapy').setLevel(INFO)

    def item_scraped(self, item):
        self._items.append(item)

        self.logger.debug('Item extracted => {:d}.'.format(len(self._items)))

    def engine_stopped(self):
        with open((Container()).data_path() + '/' + self._storage, 'w') as file:
            pickle.dump(self._items, file=file)

    def start_requests(self):
        # Do something with urls if is necessary.
        for url in self._urls:
            if not URLValidator.is_valid(url):
                self.logger.error('Invalid url -> ({}). Do nothing for this.')
                continue

            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        if self._save_evidences:
            self._storage_evidence(response.text)

    def _storage_evidence(self, content):
        path = '{}/{}_{}.html'.format((Container()
                                       ).data_path(), self.name, self._page)

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
