from pyframework.providers.cli.command import Command

from ...algorithm.restaurant_recommender import RestaurantRecommender
from ...models.user import User

class Train(Command):
    _name = 'tools:generateSentimentalAnalyzer'

    _description = "Command to do generate model for analyzer sentient."

    _arguments = [
        ['-c', '--cities', 'Cities IDs separated by commas.'],
        ['-u', '--user', 'User ID to recommend.']
    ]

    _cities = []
    """Cities to do recommendations. """

    _user = []
    """Cities to do recommendations. """

    def set_up(self):
        self._cities = self.get_argument('cities')

        if not self._cities:
            raise Exception('Cities can no be empty')

        self._cities = self._cities.split(',')
        self._user = User().get_user(self.get_argument('user'))

        if not self._user:
            raise Exception('User can no be empty')

    def handle(self) -> int:
        recommender = RestaurantRecommender()
        recommender.train(self._cities)

        return self.RETURN_SUCCESS
