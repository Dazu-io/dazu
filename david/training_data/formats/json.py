import json
import os

from david.config import DavidConfig
from david.constants import DEFAULT_DATA_PATH, TRAIN_DATA_FILE
from david.training_data import Reader
from david.typing import TrainingData


class JsonReader(Reader):
    @classmethod
    def load(cls, config: DavidConfig) -> TrainingData:

        inputFile = os.path.join(".", DEFAULT_DATA_PATH, TRAIN_DATA_FILE)

        with open(inputFile) as f:
            data = json.load(f)
            return TrainingData(data)
