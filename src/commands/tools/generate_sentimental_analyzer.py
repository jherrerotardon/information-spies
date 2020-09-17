from pyframework.providers.cli.command import Command

from ...algorithm.sentimental_analyser import SentimentalAnalyser


class GenerateSentimentalAnalyzer(Command):
    _name = 'tools:generateSentimentalAnalyzer'

    _description = "Command to do generate model for analyzer sentient."

    def handle(self) -> int:
        analyzer = SentimentalAnalyser()

        # analyzer.train()
        # analyzer.storage_model()

        return self.RETURN_SUCCESS
