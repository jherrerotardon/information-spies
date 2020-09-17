"""Review module to access DB. """

from time import sleep
import sys

from pyframework.models.mongodb_model import MongoDBModel
from pymongo import ASCENDING

from ..algorithm.translator import Translator


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

    def __init__(self, config_=None):
        super(Review, self).__init__(config_)

        self.check_indexes()

    def get_from_restaurants(self, entities_ids: list):
        """Returns restaurants reviews in array of ids.

        :param entities_ids:
        :return:
        """
        match = {
            'entity_id': {'$in': entities_ids},
            'english': {'$exists': True},
        }

        cursor = self.find({
            'filter': match,
            'projection': {
                'text': 1,
                'english': 1,
                'stars': 1,
                'visitDate': 1,
                'entity_id': 1,
            }
        })

        return list(cursor)

    def translate(self):
        """If review has no english text, translate it.

        :return:
        """
        translator = Translator()

        cursor = self.find({})
        for doc in cursor:
            if 'english' not in doc:
                doc['english'] = translator.to_english(doc['text'])
                sleep(0.5)

                self.add_document_to_batch(doc)

        self.execute_batch()
        sys.exit(0)

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
                    'name': 'ByEntity',
                    'keys': [
                        ('entity_id', ASCENDING),
                    ],
                },
            ]

        super(Review, self).check_indexes(indexes)
