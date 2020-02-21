from abc import abstractmethod
from typing import Dict

from david.registry import Module, Registry
from david.typing import Message


class Adapter(Module):
    """
    Adapter Class documentation
    """

    @classmethod
    def validate_data(self, payload: Dict) -> bool:
        """
        validate_data method documentation
        """
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
    def validate_data(cls, payload: Dict) -> bool:
        return "input" in payload and "text" in payload["input"]

    @classmethod
    def input(cls, payload: Dict) -> Message:
        return Message.build(payload=payload)

    @classmethod
    def output(cls, message: Message) -> Dict:
        return message.__dict__


Registry.registryAdapter(MessageAdapter)
