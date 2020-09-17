from pyframework.providers.cli.command import Command
from ...models.restaurant import Restaurant

from ...algorithm.word_cloud_generator import WordCloudGenerator


class GenerateWordsCloud(Command):
    _name = 'tools:generateSentimentalAnalyzer'

    _description = "Command to generate the wordloud from all restaurants."

    def handle(self) -> int:
        restaurant_obj = Restaurant()
        for restaurant in restaurant_obj.get():
            WordCloudGenerator.generate(restaurant[0])

        return self.RETURN_SUCCESS
