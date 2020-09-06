from scrapy import Request

from ..crawler import Crawler


class Restaurants(Crawler):
    name = 'TripadvisorReviews'

    _storage = 'reviews.pickle'

    def parse(self, response, **kwargs):

        super(Restaurants, self).parse(response)

        # Extract reviews from current page.
        for restaurants in self._processor.get_restaurants(response):
            yield restaurants

        if next_page := self._processor.get_next_page_url(response):
            yield Request(url=response.urljoin(next_page), callback=self.parse)
