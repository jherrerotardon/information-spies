from pyframework.models.mysql_model import MySQLModel
from pyframework.helpers.lists import array_merge
from enum import Enum


class Column(Enum):
    """Columns of table. """
    ID = 'id'
    NAME = 'name'
    ADDRESS = 'address'
    POSTAL_CODE = 'postal_code'
    STARS = 'starts'
    URL = 'url'
    RANKING = 'ranking'
    CITY = 'city_id'
    ENDPOINT = 'endpoint_id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'


class Restaurant(MySQLModel):
    """List with all columns of table. """
    _columns = [column.value for column in Column]

    _database = 'tourism'

    _table = 'restaurant'

    def __init__(self):
        super(Restaurant, self).__init__()

        self._use_db()

    def get_restaurant(self, id_: int):
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

    def insert_or_update(self, restaurant: dict):
        sql = 'SELECT {} FROM {} WHERE {}=%s LIMIT 1'.format(
            Column.ID.value,
            self._table,
            Column.NAME.value
        )

        restaurant_stored = self.select_one(sql, (restaurant['name'],))

        if restaurant_stored:
            restaurant_id = restaurant_stored[0]  # Get ID.
            sql = 'UPDATE {} SET {} WHERE {}'.format(
                self._table,
                ', '.join(['{0}=%({0})s'.format(column) for column in restaurant]),
                '{0}=%({0})s'.format(Column.ID.value)
            )

            data = array_merge({Column.ID.value: restaurant_id}, restaurant)
            self.execute(sql, data)
        else:
            sql = 'INSERT INTO {} ( {} ) VALUES ( {} )'.format(
                self._table,
                ', '.join(restaurant),
                ', '.join(['%({})s'.format(column) for column in restaurant]),
            )

            self.execute(sql, restaurant)
