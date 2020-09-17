"""Module to analyze sentiments from Restaurants of City. """
import csv
import gzip
import pickle
import re
import string
from io import StringIO
from pathlib import Path

import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from nltk.tokenize import RegexpTokenizer
from pyframework.container import Container

# NLTK requirements.
NLTK_RESOURCES_DIR = Container().root_path() + '/.venv/nltk_data'
NLTK_RESOURCES = [
    'corpora/stopwords'
]

# Tries to load nltk resource if already has not be loaded.
for resource in NLTK_RESOURCES:
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(resource.split('/')[-1], download_dir=NLTK_RESOURCES_DIR)

from nltk.corpus import stopwords

stopwords_list = set(stopwords.words('english'))


def tokenize_clean_text(text) -> list:
    """Clean text and tokenize it.

    Remove @ from tweets, rare characters, remove stopwords, etc.

    :param text:
    :return:
    """
    text = re.sub(r"https?\S+", "", text)
    text = re.sub(r"@\S+", "", text)
    text = re.sub('\[.*?¿\]\%', ' ', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub('\w*\d\w*', '', text)

    text = text.lower()

    # Remove punctuation.
    tokenizer = RegexpTokenizer(r'\w+')
    word_tokens = tokenizer.tokenize(text)

    return [w for w in word_tokens if w not in stopwords_list]


def word_feats(words):
    """Creates the matrix of words.

    :param words:
    :return:
    """
    return dict([(word, True) for word in words])


class SentimentalAnalyser:
    """Naive-Bayes sentiment analyzer. """

    NEGATIVE = '0'
    POSITIVE = '4'
    NEUTRAL = '2'
    UNKNOWN = 'unk'
    """Possible sentiments."""

    DATASET_FILE = 'sentimental_dataset.gz'

    MODEL_FILE = 'sentimental_analyser.pickle'

    _classifier = None
    """Sentimental classifier model. """

    def __init__(self):
        self._load_model()

    def train(self):
        """Trains new sentimental analyzer model.

        :return:
        """
        data = self._get_train_data()

        percentage_to_train = 0.9

        neg_feats = [(word_feats(tokenize_clean_text(tweet[1])), self.NEGATIVE)
                     for tweet in data if tweet[0] == self.NEGATIVE]
        pos_feats = [(word_feats(tokenize_clean_text(tweet[1])), self.POSITIVE)
                     for tweet in data if tweet[0] == self.POSITIVE]

        del data

        neg_cutoff = round(len(neg_feats) * percentage_to_train)
        pos_cutoff = round(len(pos_feats) * percentage_to_train)

        train_feats = neg_feats[:neg_cutoff] + pos_feats[:pos_cutoff]
        test_feats = neg_feats[neg_cutoff:] + pos_feats[pos_cutoff:]

        # Train Classifier.
        print('train on %d instances, test on %d instances' % (len(train_feats), len(test_feats)))
        self._classifier = NaiveBayesClassifier.train(train_feats)
        print('accuracy: ', accuracy(self._classifier, test_feats))

        self._classifier.show_most_informative_features()

    def classify(self, text: str):
        """Classify the list of texts in positive or negative sentiment.

        :param text:
        :return:
        """

        result = self._classifier.classify(word_feats(tokenize_clean_text(text)))

        return result

    def _get_train_data(self) -> list:
        """Returns a list with text and sentiments to train process.

        :return:
        """
        with gzip.open(self._dataset_file_path()) as file:
            content = file.read().decode('latin-1')
            content = [row for row in csv.reader(StringIO(content), delimiter=',')]
            content.pop(0)

        return content

    def _dataset_file_path(self) -> str:
        """Returns path for data to train model.

        :return:
        """
        return Container().data_path() + '/' + self.DATASET_FILE

    def _load_model(self):
        """Tries to load model from storage. If not exists, train new
        and stored it.

        :return:
        """
        model_storage = self._get_model_storage()

        if model_storage.is_file():
            self._classifier = pickle.load(open(str(model_storage), "rb"))
        else:
            self.train()
            self.storage_model()

    def storage_model(self):
        """Storage model in storage dir.

        :return:
        """
        model_storage = self._get_model_storage()

        pickle.dump(self._classifier, open(str(model_storage), "wb"))

    def _get_model_storage(self):
        """Returns file path where model should be stored.

        :return:
        """
        return Path(Container().storage_path() + '/models/' + self.MODEL_FILE)

