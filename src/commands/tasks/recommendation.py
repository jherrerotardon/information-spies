import pandas as df
from pyframework.commands.task import Task
from pyframework.exceptions.custom_exceptions import InvalidDataException

from ...algorithm.restaurant_recommender import RestaurantRecommender
from ...triggers.recommendation_trigger import RecommendationTrigger, AbstractTrigger


class Recommend(Task):
    """Concrete task to do recommendations. """

    _name = 'recommendation:ready:task'

    _user_id = None
    """User ID id to do recommendation. """

    def set_up(self):
        super(Recommend, self).set_up()

        self._user_id = self._payload.get('user_id')

        if not self._user_id:
            raise InvalidDataException('Empty place. Nothing to download.')

    def run(self):
        super(Recommend, self).run()

        recommender = RestaurantRecommender()
        prediction = recommender.predict(df.DataFrame(), 'stars')
        prediction = prediction.sort_values(by=['stars'], ascending=False)

        # The restaurant with more stars will be most likely for user.
        entity_recommended = prediction.iloc[0]['entity_id']

        return self.RETURN_SUCCESS

    def _get_trigger(self) -> AbstractTrigger:
        return RecommendationTrigger()
