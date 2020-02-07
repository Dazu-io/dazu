from abc import ABCMeta
from typing import Type

from david.config import DavidConfig
from david.constants import CONFIG_DEFAULT_ADAPTER

ADAPTER_PREFIX = "adapter_"


class Module(type, metaclass=ABCMeta):
    """Metaclass with `name` class property"""

    @classmethod
    def name(cls):
        """The name property is a function of the class - its __name__."""

        return cls.__name__


# [TODO] refactory as generic registry
class Registry:

    _instance = None

    modules = {}

    @classmethod
    def registry(cls, module: Module, prefix: str = ""):
        cls.modules[prefix + module.name()] = module

    @classmethod
    def get(cls, moduleName: str, prefix: str = "", default=None) -> Module:
        name = prefix + moduleName

        if name in cls.modules:
            return cls.modules[name]

        return default

    @classmethod
    def registryAdapter(cls, adapter: Type[Module]):
        cls.registry(adapter, ADAPTER_PREFIX)

    @classmethod
    def getAdapter(cls, config: DavidConfig, adapterName=None):

        if not adapterName:
            adapterName = config.get(CONFIG_DEFAULT_ADAPTER)

        return cls.get(adapterName, ADAPTER_PREFIX)
