import json
from typing import Dict, List, Text

from abc import abstractmethod

from david.registry import Module
from david.typing import Message


class Adapter(Module):
    @classmethod
    def validade_data(self, payload: Dict) -> bool:
        return True

    @classmethod
    @abstractmethod
    def input(cls, payload: Dict) -> Message:
        pass

    @classmethod
    @abstractmethod
    def output(cls, message: Message) -> Dict:
        pass


class MessageAdapter(Adapter):
    @classmethod
    def name(cls):
        return "message"

    @classmethod
    def validade_data(cls, payload: Dict) -> bool:
        return "input" in payload and "text" in payload["input"]

    @classmethod
    def input(cls, payload: Dict) -> Message:
        return Message.build(payload=payload)

    @classmethod
    def output(cls, message: Message) -> Dict:
        return message.__dict__
