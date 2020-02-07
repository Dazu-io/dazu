from typing import Any, Dict, List, Optional, Text, Type

from david.components.dialogue import SimpleDialogue
from david.components.nlu import SimpleNLU
from david.config import DavidConfig
from david.constants import CONFIG_DEFAULT_ADAPTER
from david.typing import Module

ADAPTER_PREFIX = "adapter_"


# To simplify usage, there are a couple of model templates, that already add
# necessary components in the right order. They also implement
# the preexisting `backends`.
registered_pipeline_templates = {"simple": [SimpleNLU, SimpleDialogue,]}


def pipeline_template(s: Text) -> Optional[List[Dict[Text, Any]]]:
    import copy

    # do a deepcopy to avoid changing the template configurations
    return copy.deepcopy(registered_pipeline_templates.get(s))


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
