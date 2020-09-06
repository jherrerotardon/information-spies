"""Module to extract info from restaurants from city. """

from re import search

from ..abstract_processor import AbstractProcessor


class Restaurants(AbstractProcessor):
    """Class to extract info from restaurants from city. """

    @staticmethod
    def get_restaurants(response):
        """Returns a list with restaurants in web page.

        :param response:
        :return:
        """
        restaurants = response.selector.css('div._1llCuDZj')

        out = []
        for restaurant in restaurants:
            try:
                out.append({
                    'name': Restaurants.get_name(restaurant),
                    'address': None,
                    'postal_code': None,
                    'stars': Restaurants.get_stars(restaurant),
                    'url': Restaurants.get_url(restaurant),
                    'ranking': None,
                })
            except Exception as exception:
                continue

        return out

    @staticmethod
    def get_name(restaurant) -> str:
        """Extracts the name of restaurant in block.

        :param restaurant:
        :return:
        """
        selector = 'a._15_ydu6b::text'

        name = restaurant.css(selector).getall()
        name = ''.join(name)
        numeration = search(r'^\d+\.', name)
        if numeration:
            name = name[numeration.end():]

        return name

    @staticmethod
    def get_url(restaurant):
        """Returns restaurant URL access.

        :param restaurant:
        :return:
        """
        selector = 'a._15_ydu6b::attr(href)'

        return restaurant.css(selector).get()

    @staticmethod
    def get_next_page_url(response):
        """If exists more pages with restaurants, then returns it.

        :param response:
        :return:
        """
        selector = 'a.next::attr(href)'
        next_page_url = response.selector.css(selector).get()

        return next_page_url

    @staticmethod
    def get_stars(restaurant) -> float:
        """Returns stars numbers associated with restaurant.

        :param restaurant:
        :return:
        """
        selector = 'span._3KcXyP0F::attr(title)'
        stars = float(restaurant.css(selector).get().split(' ')[0].replace(',', '.'))

        return stars
