from abc import abstractmethod
from typing import Dict

from dazu.config import DazuConfig
from dazu.registry import Module
from dazu.typing import TrainingData


class Reader(Module):
    @classmethod
    @abstractmethod
    def load(cls, config: DazuConfig) -> TrainingData:
        pass

    @classmethod
    def validate_data(cls, config: DazuConfig, data: Dict) -> bool:
        return True
