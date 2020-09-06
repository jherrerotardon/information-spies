from pathlib import Path

from pyframework.container import Container
from pyframework.models.mysql_model import MySQLModel

from enum import Enum


class Column(Enum):
    """Columns of table. """
    ID = 'id'
    NAME = 'name'
    CODE = 'code'
    POPULATION = 'population'
    PROVINCE = 'province_id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'


class City(MySQLModel):
    _columns = [column.value for column in Column]

    _database = 'tourism'

    _table = 'city'

    def __init__(self):
        super(City, self).__init__()

        self._use_db()

    def get_city(self, id_: int):
        """Find the city with citi ID equals id_.

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

    def from_csv(self) -> list:
        """Read all csv files from city table in databases dir and
        returns it as list of dicts.

        :return:
        """
        databases_path = Container('').root_path() + '/databases'
        databases_path = Path(databases_path)

        data = []
        if databases_path.is_dir():
            files = databases_path.glob('{}_*.csv'.format(self._table))
            for file_path in files:
                with open(str(file_path), 'r') as file:
                    lines = file.readlines()

                columns = lines.pop(0).replace('\n', '').split(',')
                for line in lines:
                    split = line.replace('\n', '').split(',')
                    dict_ = {}
                    for index, column in enumerate(columns):
                        dict_[column] = split[index]

                    data.append(dict_)

        return data
