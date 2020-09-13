"""Review module to access DB. """

from pyframework.models.mongodb_model import MongoDBModel
from pymongo import ASCENDING


class Review(MongoDBModel):
    """Review model to access DB.

     doc = {
        'title': str,
        'text': str,
        'stars': float,
        'reviewDate': Date,
        'visitDate': Date,
        'country': str,
        'city': str,
     }
     """

    _database = 'tourism'

    _collection = 'Review'

    def get_params_to_update_documents(self, doc):
        params = super(Review, self).get_params_to_update_documents(doc)

        params['filter'] = {
            '_id': doc['_id'],
        }

        return params

    def check_indexes(self, indexes=None, options=None):
        if not indexes:
            indexes = [
                {
                    'name': 'byEntity',
                    'keys': [
                        ('entity_id', ASCENDING),
                    ],
                },
            ]

        super(Review, self).check_indexes(indexes)
