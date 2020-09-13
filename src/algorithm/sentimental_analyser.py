"""Module to analyze sentiments from Restaurants of City. """
import csv
import gzip
import re
from io import StringIO
import string

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
    """Tokenize

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

    _classifier = None

    def train(self):
        """Trains new sentimental analyzer model.

        :return:
        """
        data = self._get_train_data()

        percentage_to_train = 0.85

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

        # Get data to test.
        result = self.test_classifier(self._classifier, tweets_for_test)

        print('There are ' + str(result[self.NEGATIVE]) + ' negatives tweets.')
        print('There are ' + str(result[self.POSITIVE]) + ' positives tweets.')

        self._classifier.show_most_informative_features()

    def classify(self, texts: list):
        """Classify the list of texts in positive or negative sentiment.

        :param texts:
        :return:
        """
        result = [self._classifier.classify(word_feats(tokenize_clean_text(text))) for text in texts]

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
