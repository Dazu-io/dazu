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
