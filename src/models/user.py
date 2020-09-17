"""User module to access DB. """

from enum import Enum

from pyframework.models.mysql_model import MySQLModel


class Column(Enum):
    """Columns of table. """

    ID = 'id'
    NAME = 'name'
    LAST_NAME = 'last_name'
    EMAIL = 'email'
    CITY = 'city'
    GENDER = 'gender'
    DESCRIPTION = 'description'


class User(MySQLModel):
    """User model to access DB. """

    _columns = [column.value for column in Column]
    """List with all columns of table. """

    _database = 'tourism'

    _table = 'user'

    def __init__(self):
        super(User, self).__init__()

        self._use_db()

    def get_user(self, id_: int) -> dict:
        """Find the user with restaurant ID equals id_.

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
