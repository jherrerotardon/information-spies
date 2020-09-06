"""Module to instantiate crawlers dynamically. """

from pyframework.exceptions.custom_exceptions import ArgumentException

from ..interfaces.factory_interface import FactoryAbstract


class Factory(FactoryAbstract):
    """Class to instantiate crawlers dynamically. """

    @classmethod
    def _get_module_path(cls, **kwargs) -> str:
        if 'endpoint' not in kwargs:
            raise ArgumentException('Endpoint required.')

        return kwargs['endpoint']

    @classmethod
    def _get_module_name(cls, **kwargs) -> str:
        if 'extractor_name' not in kwargs:
            raise ArgumentException('Extrator name to download is required.')

        return kwargs['extractor_name'].lower()
