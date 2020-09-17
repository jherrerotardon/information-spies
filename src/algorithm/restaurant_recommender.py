"""Module to do recommendations by user. """

import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from pyframework.container import Container
from pyframework.helpers.configuration import is_production_env
from pyframework.helpers.lists import array_column
from tensorflow import keras
from tensorflow.keras import layers

from .sentimental_analyser import SentimentalAnalyser
from ..models.restaurant import Restaurant
from ..models.review import Review


def normalize(x, stats):
    return (x - stats['mean']) / stats['std']


def stats_from_dataset(train_dataset):
    """Returns information from dataset,.

    :param train_dataset:
    :return:
    """
    train_stats = train_dataset.describe()
    train_stats.pop("stars")
    train_stats = train_stats.transpose()

    return train_stats


class PrintDot(keras.callbacks.Callback):
    """ Display training progress by printing a single dot for each completed epoch. """

    def on_batch_end(self, batch, logs=None):
        if batch % 100 == 0:
            print('')

        print('.', end='')


class RestaurantRecommender:
    """Class to do recommendations by user. """

    MODEL_NAME = 'tripadvisor_stars.h5'

    EPOCHS = 1000
    """Number of epoch to train perceptron. """

    _model = None
    """Model with perceptron. """

    def __init__(self):
        self._load_model_from_storage()

    def train(self, cities: list):
        """Train new model with data from cities.

        :param cities:
        :return:
        """
        # Get data.
        reviews = self._get_reviews(cities)
        data_set = self.prepare_data_set(reviews)

        # Split train and test data.
        train_dataset = data_set.sample(frac=0.8, random_state=0)
        test_dataset = data_set.drop(train_dataset.index)

        # Gets stats to can normalize.
        stats = stats_from_dataset(train_dataset)

        # Split objective labels.
        train_labels = train_dataset.pop('stars')
        test_labels = test_dataset.pop('stars')

        # Normalize data.
        normalized_train_dataset = normalize(train_dataset, stats)
        normalized_test_dataset = normalize(test_dataset, stats)

        aa = self.predict(normalized_test_dataset)

        # Create new model.
        self._model = self.build_model(train_dataset)

        # Fit model.
        history = self._model.fit(
            normalized_train_dataset,
            train_labels,
            epochs=self.EPOCHS,
            validation_split=0.2,
            verbose=0,
            callbacks=[PrintDot()]
        )

        # Save model after train it.
        self.save_model()

        # Plot train detail.
        self._plot_train_history(history)

        # Some test to get accuracy data.
        self._test_model(normalized_test_dataset, test_labels)

    def _load_model_from_storage(self):
        """Load model from storage to avoid retrain it.

        :return:
        """
        path = self._model_path()
        self._model = tf.keras.models.load_model(path)

    def save_model(self):
        """ Save the entire model to a HDF5 file.
        The '.h5' extension indicates that the model should be saved to HDF5.

        :return:
        """

        path = self._model_path()
        self._model.save(path)

    def prepare_data_set(self, reviews: list):
        """Prepare data set to be trained.

        :param reviews:
        :return:
        """
        sentimental_analyzer = SentimentalAnalyser()

        # Fill sentiment of each review
        sentiments = [sentimental_analyzer.classify(text)
                      for text in array_column(reviews, 'english')]
        for sentiment, review in zip(sentiments, reviews):
            review['sentiment'] = int(sentiment)

        # Fill subjective qualities of restaurants.
        qualities = self._get_quality_per_restaurant(reviews)
        for review in reviews:
            review['entityStars'] = qualities[str(review['entity_id'])]

        # Format dates.
        for review in reviews:
            visit_date = review['visitDate']
            year = visit_date[0:4]
            month = visit_date[4:6]

            review['year'] = int(year)
            review['month'] = int(month)

        # Delete unnecessary data.
        for review in reviews:
            del review['_id']
            del review['text']
            del review['english']
            del review['visitDate']

        data_set = pd.DataFrame(reviews)

        return data_set

    def predict(self, normalized_dataset, target_name='target'):
        """Do predictions on dataset. Append new columns in input dataset
        with name target_name.

        Returns new data set.

        :param normalized_dataset:
        :param target_name:
        :return:
        """
        predictions = self._model.predict(normalized_dataset).flatten()

        result = normalized_dataset.copy()
        result[target_name] = predictions

        return result

    @staticmethod
    def build_model(data_set):
        """"Create new empty model.

        :param data_set:
        :return:
        """
        model = keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=[len(data_set.keys())]),
            layers.Dense(64, activation='relu'),
            layers.Dense(1),
        ])

        optimizer = tf.keras.optimizers.RMSprop(0.001)

        model.compile(
            loss='mse',
            optimizer=optimizer,
            metrics=['mae', 'mse']
        )

        return model

    @staticmethod
    def _get_quality_per_restaurant(reviews: list):
        """Calculate subjective quality for each restaurant using sentiments.

        :param reviews:
        :return:
        """
        result = {}
        restaurants = {doc['entity_id'] for doc in reviews}
        for restaurant in restaurants:
            selected = [item for item in reviews if item['entity_id'] == restaurant]
            positive = [item for item in selected if str(item['sentiment']) == SentimentalAnalyser.POSITIVE]

            # Over 5.
            quality = 5 * (len(positive) / len(selected))

            result[str(restaurant)] = quality

        return result

    @staticmethod
    def _get_reviews(cities: list):
        """Return all reviews from a city.

        :param cities:
        :return:
        """
        restaurants = []

        restaurant_obj = Restaurant()
        reviews_obj = Review()
        # reviews_obj.translate()

        for city in cities:
            restaurants += restaurant_obj.get_restaurants_on_city(city)

        restaurants_ids = array_column(restaurants, 'id')
        reviews = reviews_obj.get_from_restaurants(restaurants_ids)

        return reviews

    def _test_model(self, normalized_test_dataset, test_labels):
        """Check model accuracy.

        :param normalized_test_dataset:
        :return:
        """
        loss, mae, mse = self._model.evaluate(normalized_test_dataset, test_labels, verbose=2)

    @staticmethod
    def _plot_train_history(history):
        """Plot evolution of error in each epoch of train.

        :param history:
        :return:
        """
        if not is_production_env():
            hist = pd.DataFrame(history.history)
            hist['epoch'] = history.epoch

            plt.figure()
            plt.xlabel('Epoch')
            plt.ylabel('Mean Abs Error [stars]')
            plt.plot(hist['epoch'], hist['mae'], label='Train Error')
            plt.plot(hist['epoch'], hist['val_mae'], label='Val Error')
            plt.ylim([0, 5])
            plt.legend()

            plt.figure()
            plt.xlabel('Epoch')
            plt.ylabel('Mean Square Error [$stars^2$]')
            plt.plot(hist['epoch'], hist['mse'], label='Train Error')
            plt.plot(hist['epoch'], hist['val_mse'], label='Val Error')
            plt.ylim([0, 5])
            plt.legend()
            plt.show()

    def _model_path(self) -> str:
        """Returns the path where model must be stored.

        :return:
        """
        return Container().data_path() + '/' + self.MODEL_NAME
