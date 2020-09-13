"""Module to analyze sentiments from Restaurants of City. """
import csv
import gzip
import re
from io import StringIO

import nltk
import pandas as pd
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
    text = re.sub(r"https?\S+", "", text)
    text = re.sub(r"@\S+", "", text)

    text = text.lower()

    # Remove punctuation.
    tokenizer = RegexpTokenizer(r'\w+')
    word_tokens = tokenizer.tokenize(text)

    return [w for w in word_tokens if w not in stopwords_list]


def word_feats(words):
    return dict([(word, True) for word in words])


class SentimentalAnalyser:
    """Naive-Bayes sentiment analyzer. """

    NEGATIVE = 'negative'
    POSITIVE = 'positive'
    NEUTRAL = 'neutral'
    UNKNOWN = 'unk'
    """Possible sentiments."""

    DATASET_FILE = 'sentimental_dataset.gz'

    _classifier = None

    def train(self):
        percentage_to_train = 0.85
        headers = []
        train_data = []

        neg_feats = [(word_feats(tokenize_clean_text(tweet[headers.index('text')])), self.NEGATIVE)
                     for tweet in train_data if tweet[headers.index('airline_sentiment')] == self.NEGATIVE]
        pos_feats = [(word_feats(tokenize_clean_text(tweet[headers.index('text')])), self.POSITIVE) for tweet in
                     train_data if tweet[headers.index('airline_sentiment')] == self.POSITIVE]

        neg_cutoff = round(len(neg_feats) * percentage_to_train)
        pos_cutoff = round(len(pos_feats) * percentage_to_train)

        train_feats = neg_feats[:neg_cutoff] + pos_feats[:pos_cutoff]
        test_feats = neg_feats[neg_cutoff:] + pos_feats[pos_cutoff:]

        # Train Classifier.
        print('train on %d instances, test on %d instances' % (len(train_feats), len(test_feats)))
        classifier = NaiveBayesClassifier.train(train_feats)
        print('accuracy: ', accuracy(classifier, test_feats))

        # Get data to test.
        headers, tweets_for_test = [], []
        test_data = [(word_feats(tokenize_clean_text(tweet[headers.index('text')])), self.UNKNOWN) for tweet in
                     tweets_for_test]
        result = self.test_classifier(classifier, tweets_for_test)

        print('There are ' + str(result[self.NEGATIVE]) + ' negatives tweets.')
        print('There are ' + str(result[self.POSITIVE]) + ' positives tweets.')

        classifier.show_most_informative_features()

    def test_classifier(self, classifier_, tweets):
        result_ = {
            self.POSITIVE: 0,
            self.NEUTRAL: 0,
            self.NEGATIVE: 0,
        }

        headers = []

        with open('/result.csv', mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for tweet in tweets:
                corpus = word_feats(tokenize_clean_text(tweet[headers.index('text')]))
                sentiment = classifier_.classify(corpus)
                result_[sentiment] += 1

                writer.writerow([tweet[headers.index('text')], sentiment])

        return result_

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
