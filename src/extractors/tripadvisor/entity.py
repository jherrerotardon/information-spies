"""Crawler to extract reviews and data from an entity. """

from pyframework.exceptions.custom_exceptions import ArgumentException
from scrapy import Request

from ..crawler import Crawler
from ...models.restaurant import Restaurant
from ...models.review import Review


class Entity(Crawler):
    """Crawler to extract reviews and data from an entity. """

    name = 'TripadvisorReviews'

    _storage = 'reviews.pickle'

    _entity_id = None
    """Entity ID where data will be scrapped. """

    _entity_info = {}
    """Information from entity extracted from entity web. """

    _review_obj = None
    """Reviews model instance to connect to DB. """

    _data_cleaned = False
    """Flag to make sure that reviews are removed from DB before download news. """

    def __init__(self, urls: list, **kwargs):
        super(Entity, self).__init__(urls, **kwargs)

        if 'entity_id' not in kwargs:
            raise ArgumentException('entity_id is mandatory.')

        self._entity_id = kwargs['entity_id']

        self._review_obj = Review()

    def parse(self, response, **kwargs):
        super(Entity, self).parse(response)

        if not self._data_cleaned:
            self._clean_data_on_db()
            self._data_cleaned = True

        if not self._entity_info:
            self._entity_info = self._processor.get_entity_info(response)
            self._update_restaurant_info()

        # Extract reviews from current page.
        reviews = self._processor.get_reviews(response)
        for review in reviews:
            yield review

        if next_page := self._processor.get_next_page_url(response):
            yield Request(url=response.urljoin(next_page), callback=self.parse)

    def _clean_data_on_db(self):
        """Remove reviews in BD from entity ID.

        :return:
        """
        self._review_obj.delete_many({
            'entity_id': self._entity_id,
        })

    def _storage_items(self):
        for review in self._items:
            review['entity_id'] = self._entity_id

        # Insert data on DB.
        self._review_obj.insert_many(self._items)

        self._items = []

    def _update_restaurant_info(self):
        """Update info in DB of restaurant.

        :return:
        """
        Restaurant().update(self._entity_id, self._entity_info)
