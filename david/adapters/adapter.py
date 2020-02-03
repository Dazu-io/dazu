import json
from typing import Dict, List, Text

from david.typing import Message


class Adapter:
    @property
    def name(self):
        """The name property is a function of the class - its __name__."""

        return self.__class__.__name__

    def validade_data(self, payload: Dict) -> bool:
        raise NotImplementedError

    def input(self, payload: Dict) -> Message:
        raise NotImplementedError

    def output(self, message: Message) -> Dict:
        raise NotImplementedError


class MessageAdapter(Adapter):
    @property
    def name(self):
        return "message"

    def validade_data(self, payload: Dict) -> bool:
        return "input" in payload and "text" in payload["input"]

    def input(self, payload: Dict) -> Message:
        return Message.build(payload=payload)

    def output(self, message: Message) -> Dict:
        return message.__dict__


# [TODO] create a component registry and migrate this code
class AdaptEngine:
    adapters = {}

    def __init__(self, defaultAdapter=None):

        messageAdapter = MessageAdapter()
        self.registryAdapter(messageAdapter)

        if defaultAdapter:
            self.defaultAdapter = defaultAdapter
        else:
            self.defaultAdapter = messageAdapter.name

    def registryAdapter(self, adapter: Adapter):
        self.adapters[adapter.name] = adapter

    def getAdapter(self, adapterName=None):

        if not adapterName:
            adapterName = self.defaultAdapter

        return self.adapters[adapterName]
