import json
from typing import Dict, List, Text

from david.typing import Message


class InvalidInputError(Exception):
    def __init__(self, adapter: Text) -> None:
        self.adapter = adapter

        super().__init__(adapter)

    def __str__(self) -> Text:
        return f"Adapter '{self.adapter}' does not support this input."


class Adapter:
    def validade_data(self, payload: Dict) -> bool:
        raise NotImplementedError

    def input(self, payload: Dict) -> Message:
        raise NotImplementedError

    def output(self, message: Message) -> Dict:
        raise NotImplementedError


class MessageAdapter(Adapter):
    def validade_data(self, payload: Dict) -> bool:
        return True

    def input(self, payload: Dict) -> Message:
        return Message.build(payload=payload)

    def output(self, message: Message) -> Dict:
        return message.__dict__


class AdaptEngine:
    def __init__(self, adapter: Adapter = MessageAdapter()):
        self.adapter = adapter

    @property
    def name(cls):
        """The name property is a function of the class - its __name__."""

        return cls.__name__

    def input(self, payload: Dict) -> Message:

        if not self.adapter.validade_data(payload):
            raise InvalidInputError(type(self).name)

        return self.adapter.input(payload)

    def output(self, message: Message) -> Dict:
        return self.adapter.output(message)
