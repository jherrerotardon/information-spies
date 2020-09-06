"""
|--------------------------------------------------------------------------
| Databases connection template file.
|--------------------------------------------------------------------------
|
| Here are each of the database connections setup for your application.
| Below are some example configurations.
|
"""
from pyframework.helpers.configuration import env

connections = {
    'redis': {
        'host': env('REDIS_HOST', 'localhost'),
        'port': env('REDIS_PORT', '6379'),
        'db': env('REDIS_DB', 1),
        'password': env('REDIS_PASS', 'password'),
    },
    'mongodb': {
        'uri': env('MONGO_URI', 'mongodb://localhost:27017/admin?connectTimeoutMS=5000&socketTimeoutMS=60000&w=1'),
        'driver': 'mongodb',
    },
    'mysql': {
        'host': env('MYSQL_HOST', 'localhost'),
        'user': env('MYSQL_USER', 'username'),
        'password': env('MYSQL_PASS', 'password'),
        'port': env('MYSQL_PORT', '3306'),
    },
}
