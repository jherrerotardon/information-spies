from scrapy import Request

from ..crawler import Crawler
from re import search


class CityCode(Crawler):
    name = 'TripadvisorCityCode'

    _storage = 'cities.pickle'

    def parse(self, response):
        super(CityCode, self).parse(response)

        # Extract reviews from current page.
        for review in self._get_restaurants(response):
            yield review

        if next_page := self._get_next_page_url(response):
            yield Request(url=response.urljoin(next_page), callback=self.parse)
