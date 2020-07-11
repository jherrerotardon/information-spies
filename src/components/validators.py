"""Module with some utils validators. """

from urllib.parse import urlparse


class URLValidator:
    """Self URLValidator based using urllib. """
    @staticmethod
    def is_valid(url: str):
        info = urlparse(url)

        is_valid = all([info.scheme, info.netloc])

        return is_valid
