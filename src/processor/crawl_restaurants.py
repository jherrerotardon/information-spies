"""Module with all classes necessaty to get all restaurants from city. """

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ..extractors.tripadvisor.reviews import Reviews
from ..extractors.tripadvisor.restaurants import Restaurants
from pyframework.exceptions.custom_exceptions import ArgumentException
from ..extractors.tripadvisor.city_code import CityCode
from pyframework.container import Container
from pathlib import Path
import pickle


class CrawlRestaurants:
    _city_id = ''

    _city = {}

    def __init__(self, city_id: int):
        if not isinstance(city_id, int) or city_id < 0:
            raise ArgumentException('City id is required and must be positive.')

        self._city_id = city_id

        city_id

    def run(self):
        restaurant_url = 'https://www.tripadvisor.es/Restaurant_Review-g187514-d777072-Reviews-La_Castela-Madrid.html'
        city_url = 'https://www.tripadvisor.es/Restaurants-g187514-Madrid.html'
        search = 'https://www.tripadvisor.es/Search?q=madrid&blockRedirect=true'
        search = 'https://www.tripadvisor.es/Search?q=madrid&searchSessionId' \
                 '=2613B4BDB243229C3A21B003659C62091591742967628ssid&sid' \
                 '=729A3B5B7FAB7B6EBB6E72BAA11CA07E1591742968674&blockRedirect=true '
        info = None
        reviews_file = (Container()).data_path() + '/reviews.pickle'
        cities_file = (Container()).data_path() + '/cities.pickle'

        file_test = cities_file
        if (Path(file_test)).is_file():
            with open(file_test, 'rb') as file:
                info = pickle.load(file)
        else:
            process = CrawlerProcess(get_project_settings())
            # process.crawl(Reviews, [restaurant_url])
            # process.crawl(Restaurants, [city_url])
            process.crawl(CityCode, [search])
            process.start()

        stop = 1
