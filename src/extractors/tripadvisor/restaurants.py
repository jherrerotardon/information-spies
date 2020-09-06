from scrapy import Request

from ..crawler import Crawler
from ...models.restaurant import Restaurant
from pyframework.exceptions.custom_exceptions import ArgumentException


class Restaurants(Crawler):
    name = 'TripadvisorReviews'

    _storage = 'reviews.pickle'

    _city_id = None
    """City ID ID where data will be scrapped. """

    _endpoint_id = None
    """Endpoint ID where data will be scrapped. """

    def __init__(self, urls: list, **kwargs):
        super(Restaurants, self).__init__(urls, **kwargs)

        if 'endpoint_id' not in kwargs:
            raise ArgumentException('endpoint_id is mandatory.')

        if 'city_id' not in kwargs:
            raise ArgumentException('city_id is mandatory.')

        self._endpoint_id = kwargs['endpoint_id']
        self._city_id = kwargs['city_id']

    def parse(self, response, **kwargs):

        super(Restaurants, self).parse(response)

        # Extract reviews from current page.
        for restaurants in self._processor.get_restaurants(response):
            yield restaurants

        if next_page := self._processor.get_next_page_url(response):
            yield Request(url=response.urljoin(next_page), callback=self.parse)

    def _storage_items(self):
        restaurant_obj = Restaurant()
        for restaurant in self._items:
            restaurant['endpoint_id'] = self._endpoint_id
            restaurant['city_id'] = self._city_id

            restaurant_obj.insert_or_update(restaurant)

        self._items = []
