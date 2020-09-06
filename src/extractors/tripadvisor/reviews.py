from datetime import datetime

from pyframework.helpers.dates import ymd_str
from scrapy import Request

from ..crawler import Crawler


class Reviews(Crawler):
    name = 'TripadvisorReviews'

    _storage = 'reviews.pickle'

    def parse(self, response, **kwargs):
        super(Reviews, self).parse(response)

        # Extract reviews from current page.
        for review in self._processor.get_reviews(response):
            yield review

        if next_page := self._processor.get_next_page_url(response):
            yield Request(url=response.urljoin(next_page), callback=self.parse)