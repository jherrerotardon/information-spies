"""Restaurant model to access DB. """

from enum import Enum

from pyframework.helpers.lists import array_merge
from pyframework.models.mysql_model import MySQLModel


class Column(Enum):
    """Columns of table. """

    ID = 'id'
    NAME = 'name'
    ADDRESS = 'address'
    POSTAL_CODE = 'postal_code'
    STARS = 'stars'
    URL = 'url'
    RANKING = 'ranking'
    CITY = 'city_id'
    ENDPOINT = 'endpoint_id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'


class Restaurant(MySQLModel):
    """Column model to access DB. """

    _columns = [column.value for column in Column]
    """List with all columns of table. """

    _database = 'tourism'

    _table = 'restaurant'

    def __init__(self):
        super(Restaurant, self).__init__()

        self._use_db()

    def get_restaurant(self, id_: int) -> dict:
        """Find the city with restaurant ID equals id_.

        :param id_:
        :return:
        """
        sql = 'SELECT {} FROM {} WHERE {}=%s LIMIT 1'.format(
            ', '.join(self._columns),
            self._table,
            Column.ID.value
        )

        result = self.select_one(sql, [id_])

        return {key: value for key, value in zip(self._columns, result)} if result else {}

    def get_restaurants_on_city(self, city_id: int) -> list:
        """Find the restaurant on a city .

        :param city_id:
        :return:
        """
        columns = [
            Column.ID.value,
        ]

        sql = 'SELECT {} FROM {} WHERE {}=%s'.format(
            ', '.join(columns),
            self._table,
            Column.CITY.value
        )

        cursor = self.execute(sql, (city_id,))
        result = [{key: value for key, value in zip(columns, restaurant)} for restaurant in cursor]

        return result

    def insert_or_update(self, restaurant: dict):
        """Insert new restaurant on DB. If exists restaurant with the same name, update it.

        :param restaurant:
        :return:
        """
        sql = 'SELECT {} FROM {} WHERE {}=%s LIMIT 1'.format(
            Column.ID.value,
            self._table,
            Column.NAME.value
        )

        restaurant_stored = self.select_one(sql, (restaurant['name'],))

        if restaurant_stored:
            restaurant_id = restaurant_stored[0]  # Get ID.
            self.update(restaurant_id, restaurant)
        else:
            self.insert(restaurant)

    def update(self, restaurant_id: int, data: dict):
        """Updates restaurant by id.

        :param restaurant_id:
        :param data:
        :return:
        """
        if Column.ID.value in data:
            del data[Column.ID.value]

        sql = 'UPDATE {} SET {} WHERE {}'.format(
            self._table,
            ', '.join(['{0}=%({0})s'.format(column) for column in data]),
            '{0}=%({0})s'.format(Column.ID.value)
        )

        data = array_merge({Column.ID.value: restaurant_id}, data)
        self.execute(sql, data)

    def insert(self, data: dict):
        """Insert new restaurant in DB.

        :param data:
        :return:
        """
        sql = 'INSERT INTO {} ( {} ) VALUES ( {} )'.format(
            self._table,
            ', '.join(data),
            ', '.join(['%({})s'.format(column) for column in data]),
        )

        self.execute(sql, data)
