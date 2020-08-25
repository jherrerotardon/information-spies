from pyframework.models.mysql_model import MySQLModel
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
