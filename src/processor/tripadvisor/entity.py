"""Module to extract reviews from restaurant. """

from datetime import datetime

from pyframework.helpers.dates import ymd_str

from ..abstract_processor import AbstractProcessor


class Entity(AbstractProcessor):
    """Class to extract reviews from restaurant. """

    @staticmethod
    def get_reviews(response):
        """Returns the reviews from entity web page.

        :param response:
        :return:
        """
        reviews = response.selector.css('div.review-container')

        out = [{
            'title': Entity.get_review_title(review),
            'text': Entity.get_review_text(review),
            'stars': Entity.get_stars(review),
            'reviewDate': Entity.get_review_date(review),
            'visitDate': Entity.get_visit_date(review),
            'country': Entity.get_country(review),
            'city': Entity.get_city(review),
        } for review in reviews]

        return out

    @staticmethod
    def get_entity_info(response):
        """Returns the entity information from entity web page.

        :param response:
        :return:
        """
        info_section = response.selector.css('div.bk7Uv0cc')

        out = {
            'address': Entity.get_entity_address(info_section),
            'postal_code': Entity.get_entity_postal_code(info_section),
            'ranking': Entity.get_entity_ranking(info_section),
            'phone': Entity.get_entity_phone(info_section),
        }

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
                Entity._number_of_month(parts[1]),
                parts[0]),
            '%Y%m%d')

        return ymd_str(date)

    @staticmethod
    def get_visit_date(review) -> str:
        """Returns the date when user visited restaurant.

        :param review:
        :return:
        """
        date = review.css('div.prw_reviews_stay_date_hsx::text').get().strip()

        parts = [element.strip() for element in date.split('de')]
        date_str = parts[1] + Entity._number_of_month(parts[0])

        return date_str

    @staticmethod
    def get_review_title(review) -> str:
        """Returns the title of a review.

        :param review:
        :return:
        """
        return review.css('span.noQuotes::text').get()

    @staticmethod
    def get_review_text(review) -> str:
        """Returns the review text from review.

        :param review:
        :return:
        """
        return review.css('div.entry > p::text').get()

    @staticmethod
    def get_stars(review) -> float:
        """Returns the stars of the review.

        :param review:
        :return:
        """
        classes = review.css('span.ui_bubble_rating::attr(class)').get()
        text = classes.split(' ')[-1].split('_')[-1]

        stars = float(text) / 10

        return stars

    @staticmethod
    def get_country(review) -> str:
        """Returns the country of the user review.

        :param review:
        :return:
        """
        country = None

        location = review.css('div.userLoc').get()
        if location is not None:
            data = location.split(',')
            if len(data) > 1:
                country = data[1].strip()

        return country

    @staticmethod
    def get_city(review) -> str:
        """Returns the city of the user review.

        :param review:
        :return:
        """
        city = None

        location = review.css('div.userLoc').get()
        if location is not None:
            city = location.split(',')[0].strip()

        return city

    @staticmethod
    def get_entity_address(info_section) -> str:
        """Returns the address of the entity.

        :param info_section:
        :return:
        """
        full_address = info_section.css('a._15QfMZ2L::text').get()
        address = full_address.split(',')[0]

        return address

    @staticmethod
    def get_entity_postal_code(info_section) -> str:
        """Returns the postal code of the entity.

        :param info_section:
        :return:
        """
        full_address = info_section.css('a._15QfMZ2L::text').get()
        city_info = full_address.split(',')[1]
        postal_code = city_info.strip().split(' ')[0]

        return postal_code

    @staticmethod
    def get_entity_ranking(info_section) -> int:
        """Returns the ranking of the entity.

        :param info_section:
        :return:
        """
        ranking = info_section.css('span._13OzAOXO._2VxaSjVD > a > span > b > span::text').get()
        ranking = ranking.replace('#', '')
        ranking = int(ranking)

        return ranking

    @staticmethod
    def get_entity_phone(info_section) -> str:
        """Returns the phone number of the entity.

        :param info_section:
        :return:
        """
        phone = info_section.css('a._3S6pHEQs::text').get()
        phone = phone.split(' ')
        phone = phone[0] + ' ' + ''.join(phone[1:])

        return phone

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
    def _number_of_month(month: str):
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
