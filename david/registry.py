from abc import ABCMeta

from david.adapters.adapter import Adapter, MessageAdapter
from david.config import DavidConfig


class Module(type, metaclass=ABCMeta):
    """Metaclass with `name` class property"""

    @property
    def name(cls):
        """The name property is a function of the class - its __name__."""

        return cls.__name__


# [TODO] refactory as generic registry
class Registry:

    _instance = None

    modules = {}

    @classmethod
    def registry(cls, module: Module, prefix: str = ""):
        cls.modules[prefix + module.name] = module

    @classmethod
    def get(cls, moduleName: str, prefix: str = "", default=None) -> Module:
        name = prefix + moduleName

        if name in cls.modules:
            return cls.modules[name]

        return default

    @classmethod
    def registryAdapter(cls, adapter: Adapter):
        cls.registry(adapter, "adapter_")

    @classmethod
    def getAdapter(cls, config: DavidConfig, adapterName=None):

        if not adapterName:
            adapterName = config.get("default_adapter")

        return cls.get(adapterName, "adapter_")
