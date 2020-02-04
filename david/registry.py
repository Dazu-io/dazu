from david.adapters.adapter import Adapter, MessageAdapter


# [TODO] refactory as generic registry
class Registry:

    _instance = None

    adapters = {}

    def __init__(self, defaultAdapter=None):

        messageAdapter = MessageAdapter()
        self.registryAdapter(messageAdapter)

        if defaultAdapter:
            self.defaultAdapter = defaultAdapter
        else:
            self.defaultAdapter = messageAdapter.name

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Registry()
        return cls._instance

    def registryAdapter(self, adapter: Adapter):
        self.adapters[adapter.name] = adapter

    def getAdapter(self, adapterName=None):

        if not adapterName:
            adapterName = self.defaultAdapter

        return self.adapters[adapterName]
