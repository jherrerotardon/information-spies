"""Module to extract reviews from restaurant. """

from datetime import datetime

from pyframework.helpers.dates import ymd_str

from ..abstract_processor import AbstractProcessor


class Reviews(AbstractProcessor):
    """Class to extract reviews from restaurant. """

    def get_reviews(self, response):
        """Returns the reviews from restaurant fom page.

        :param response:
        :return:
        """
        reviews = response.selector.css('div.review-container')

        out = [{
            'date': self.get_review_date(review),
            'title': self.get_review_title(review),
            'text': self.get_review_content(review),
        } for review in reviews]

        return out

    @staticmethod
    def get_review_date(review) -> str:
        """Returns the date that review was written.

        :param review:
        :return:
        """
        date = review.css('span.ratingDate::attr(title)').get()
        parts = [element.strip() for element in date.split('de')]
        date = datetime.strptime(
            '{}{}{}'.format(
                parts[2],
                Reviews.number_of_month(parts[1]),
                parts[0]),
            '%Y%m%d')

        return ymd_str(date)

    @staticmethod
    def get_review_title(review) -> str:
        """Returns the title of a review.

        :param review:
        :return:
        """
        return review.css('span.noQuotes::text').get()

    @staticmethod
    def get_review_content(review) -> str:
        """Returns the raw content from review.

        :param review:
        :return:
        """
        return review.css('div.entry > p::text').get()

    @staticmethod
    def get_next_page_url(response):
        """If exists more pages with restaurants, then returns it.

        :param response:
        :return:
        """
        selector = 'div.ui_pagination > a.next::attr(href)'
        next_page_url = response.selector.css(selector).get()

        return next_page_url

    @staticmethod
    def number_of_month(month: str):
        """Returns the number associated from a month in calendar.

        :param month:
        :return:
        """
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
