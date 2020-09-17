from pathlib import Path

import matplotlib.pyplot as plt
import nltk
from pyframework.container import Container
from pyframework.helpers.lists import array_column
from wordcloud import WordCloud

from ..models.review import Review

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

stopwords_list = set(stopwords.words('spanish'))


class WordCloudGenerator:

    @staticmethod
    def generate(restaurant_id: int):
        """Generates and save it a plot with wordcloud from
        reviews of restaurant.

        :param restaurant_id:
        :return:
        """
        reviews = Review().get_from_restaurants([restaurant_id])
        text = array_column(reviews, 'text')
        text = ' '.join(text)

        if not text:
            return

        wordcloud = WordCloud(
            stopwords=stopwords_list,
            background_color="white",
            colormap="Dark2",
            max_font_size=150,
            random_state=42
        )

        plt.rcParams['figure.figsize'] = [16, 12]

        # Create plot.
        wordcloud.generate(text)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")

        WordCloudGenerator._storage(wordcloud, restaurant_id)

        plt.clf()
        plt.close('all')

    @staticmethod
    def _storage(wordcloud, restaurant_id: int):
        """Storage current plot in storage directory.

        :param wordcloud:
        :param restaurant_id:
        :return:
        """
        file = '{}/{}/{}.png'.format(
            Container().data_path(),
            'restaurants',
            restaurant_id
        )

        Path(file).parents[0].mkdir(exist_ok=True)

        wordcloud.to_file(file)
