from abc import ABCMeta, abstractmethod
from typing import Dict

from david.config import DavidConfig
from david.registry import Module
from david.typing import TrainingData


class Reader(Module):
    @classmethod
    @abstractmethod
    def load(cls, config: DavidConfig) -> TrainingData:
        pass

    @classmethod
    def validate_data(cls, config: DavidConfig, data: Dict) -> bool:
        return True
