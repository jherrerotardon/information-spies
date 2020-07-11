from pyframework.providers.cli.command import Command


class DownloadReviews(Command):
    _name = 'downloadReviews'

    _description = 'Command to test Crawlers.'

    def handle(self) -> int:
        self.info_time("Init crawling...")

        # crawler = Crawler()
        # crawler.run()

        return Command.RETURN_SUCCESS
