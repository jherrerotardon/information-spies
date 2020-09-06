from pathlib import Path

from pyframework.container import Container
from pyframework.models.mysql_model import MySQLModel

from enum import Enum


class Column(Enum):
    """Columns of table. """
    CITY_ID = 'city_id'
    ENDPOINT_ID = 'endpoint_id'
    ENDPOINT_CODE = 'endpoint_code'
    ENDPOINT_NAME = 'endpoint_name'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'


class CityEndpoint(MySQLModel):
    _columns = [column.value for column in Column]

    _database = 'tourism'

    _table = 'city_endpoint'

    def __init__(self):
        super(CityEndpoint, self).__init__()

        self._use_db()

    def get_downloads(self, city_id: int):
        """Returns endpoints active info from city.

        :param city_id:
        :return:
        """
        columns = [self._table + '.' + sufix for sufix in [Column.ENDPOINT_CODE.value, Column.ENDPOINT_NAME.value]]
        foreign_columns = ['endpoint.url', 'endpoint.name']

        command = 'SELECT {} FROM {} LEFT JOIN {} ON city_endpoint.{}=endpoint.id WHERE {}=%s AND {}=1'.format(
            ','.join(columns + foreign_columns),
            self._table,
            'endpoint',
            Column.ENDPOINT_ID.value,
            self._table + '.' + Column.CITY_ID.value,
            'endpoint.enabled'
        )

        cursor = self.execute(command, (city_id, ))

        result = []
        for data in cursor:
            result.append({
                'endpoint_code': data[0],
                'endpoint_name': data[1],
                'url': data[2],
                'name': data[3],
            })

        return result
