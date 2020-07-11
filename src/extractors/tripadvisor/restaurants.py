from scrapy import Request

from ..crawler import Crawler
from re import search


class Restaurants(Crawler):
    name = 'TripadvisorReviews'

    _storage = 'reviews.pickle'

    def parse(self, response):
        super(Restaurants, self).parse(response)

        # Extract reviews from current page.
        for review in self._get_restaurants(response):
            yield review

        if next_page := self._get_next_page_url(response):
            yield Request(url=response.urljoin(next_page), callback=self.parse)

    def _get_restaurants(self, response):
        restaurants = response.selector.css('div._1llCuDZj')

        out = [{
            'name': self._get_name(restaurant),
            'url': self._get_url(restaurant),
            'reviewsNumber': self._get_reviews_number(restaurant),
        } for restaurant in restaurants]

        return out

    @staticmethod
    def _get_name(restaurant):
        selector = 'a._15_ydu6b::text'

        name = restaurant.css(selector).getall()
        name = ''.join(name)
        numeration = search(r'^\d+\.', name)
        if numeration:
            name = name[numeration.end():]

        return name

    @staticmethod
    def _get_url(restaurant):
        selector = 'a._15_ydu6b::attr(href)'

        return restaurant.css(selector).get()

    @staticmethod
    def _get_reviews_number(restaurant):
        selector = 'span.w726Ki5B::text'

        return restaurant.css(selector).get()

    @staticmethod
    def _get_next_page_url(response):
        selector = 'a.next::attr(href)'
        next_page_url = response.selector.css(selector).get()

        return next_page_url
