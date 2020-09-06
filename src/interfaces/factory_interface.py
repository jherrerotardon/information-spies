from pyframework.exceptions.custom_exceptions import ConfigurationException
from pyframework.helpers.configuration import get_module


class FactoryAbstract:
    """Abstract factory class to instantiate object on inside levels of current module. """

    _module_path = ''

    _module_name = ''

    @classmethod
    def get_class(cls, **kwargs):
        """Returns the class definition found by factory.

        :param kwargs:
        :return:
        """
        if not (from_module := cls.get_module(**kwargs)):
            raise ConfigurationException('From module import not configured.')

        if not (class_name := cls.get_class_name(**kwargs)):
            raise ConfigurationException('From module import not configured.')

        module = get_module(
            from_module,
            '.'.join(cls.__module__.split('.')[:-1])
        )
        if not module:
            raise Exception('Module <{}> is not available.'.format(
                '.'.join(cls.__module__.split('.')[:-1]) + from_module
            ))

        metaclass = getattr(module, class_name)

        return metaclass

    @classmethod
    def instance(cls, **kwargs):
        """Create dynamic instance of an object from next level.

        :param kwargs:
        :return:
        """
        instance = cls.get_class(**kwargs)(**kwargs)

        return instance

    @classmethod
    def get_module(cls, **kwargs) -> str:
        module = '.{}.{}'.format(
            cls._get_module_path(**kwargs),
            cls._get_module_name(**kwargs)
        )

        return module

    @classmethod
    def _get_module_path(cls, product: dict, **kwargs) -> str:
        return cls._module_name

    @classmethod
    def _get_module_name(cls, **kwargs) -> str:
        return cls._module_name

    @classmethod
    def get_class_name(cls, **kwargs) -> str:
        return cls._get_module_name(**kwargs).capitalize()
