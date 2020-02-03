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
    def validade_data(self, payload: Dict) -> bool:
        return "input" in payload and "text" in payload["input"]

    def input(self, payload: Dict) -> Message:
        return Message.build(payload=payload)

    def output(self, message: Message) -> Dict:
        return message.__dict__


class AdaptEngine:
    def __init__(self, adapter: Adapter = MessageAdapter()):
        self.adapter = adapter

    def input(self, payload: Dict) -> Message:

        if not self.adapter.validade_data(payload):
            raise InvalidInputError(self.adapter.name)

        return self.adapter.input(payload)

    def output(self, message: Message) -> Dict:
        return self.adapter.output(message)
