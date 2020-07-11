from datetime import datetime

from pyframework.helpers.dates import ymd_str
from scrapy import Request

from ..crawler import Crawler


class Reviews(Crawler):
    name = 'TripadvisorReviews'

    _storage = 'reviews.pickle'

    def parse(self, response):
        super(Reviews, self).parse(response)

        # Extract reviews from current page.
        for review in self._get_reviews(response):
            yield review

        if next_page := self._get_next_page_url(response):
            yield Request(url=response.urljoin(next_page), callback=self.parse)

    def _get_reviews(self, response):
        reviews = response.selector.css('div.review-container')

        out = [{
            'date': self._get_review_date(review),
            'title': self._get_review_title(review),
            'text': self._get_review_content(review),
        } for review in reviews]

        return out

    @staticmethod
    def _get_review_date(review) -> str:
        date = review.css('span.ratingDate::attr(title)').get()
        parts = [element.strip() for element in date.split('de')]
        date = datetime.strptime(
            '{}{}{}'.format(
                parts[2],
                Reviews._number_of_month(parts[1]),
                parts[0]),
            '%Y%m%d')

        return ymd_str(date)

    @staticmethod
    def _get_review_title(review) -> str:
        return review.css('span.noQuotes::text').get()

    @staticmethod
    def _get_review_content(review) -> str:
        return review.css('div.entry > p::text').get()

    @staticmethod
    def _get_next_page_url(response):
        selector = 'div.ui_pagination > a.next::attr(href)'
        next_page_url = response.selector.css(selector).get()

        return next_page_url

    @staticmethod
    def _number_of_month(month: str):
        dict_ = {
            'enero': '01',
            'febrero': '02',
            'marzo': '03',
            'abril': '04',
            'mayo': '05',
            'junio': '06',
            'julio': '07',
            'agosto': '01',
            'septiembre': '09',
            'octubre': '10',
            'noviembre': '11',
            'diciembre': '12',
        }

        return dict_[month]
