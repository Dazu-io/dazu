import json

from david.config import DavidConfig
from david.training_data import Reader
from david.typing import TrainingData

KNOW_FILE = "./data/know.json"


class JsonReader(Reader):
    @classmethod
    def load(cls, config: DavidConfig) -> TrainingData:
        with open(KNOW_FILE) as f:
            data = json.load(f)
            return TrainingData(data)
