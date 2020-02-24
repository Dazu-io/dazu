import json
import os

from dazu.config import DazuConfig
from dazu.constants import DEFAULT_DATA_PATH, TRAIN_DATA_FILE
from dazu.training_data import Reader
from dazu.typing import TrainingData


class JsonReader(Reader):
    @classmethod
    def load(cls, config: DazuConfig) -> TrainingData:

        inputFile = os.path.join(".", DEFAULT_DATA_PATH, TRAIN_DATA_FILE)

        with open(inputFile) as f:
            data = json.load(f)
            return TrainingData(data)
