import json
import os

import david.util as util
from david.components.nlu.simplenlu import SimpleNLU
from david.config import DavidConfig
from david.training_data.formats.json import JsonReader
from david.typing import Message, TrainingData

MODEL_DIR = "./models/"
MODEL_FILE = "intent_model.json"

# def persist_stopwords(data):
#     with open('./data/stopwords.json', 'w') as outfile:
#         json.dump(data, outfile)


class Brain:
    def __init__(self, config: DavidConfig):
        self.config = config
        self.train()

    def train(self) -> None:
        training_data = JsonReader.load(self.config)
        self.nlu = SimpleNLU.create({}, self.config)
        self.nlu.train(training_data, self.config)
        self.nlu.persist(file_name=MODEL_FILE, model_dir=MODEL_DIR)

    def process(self, text) -> Message:
        message = Message.build(text)
        self.nlu.process(message)
        return message

    def nlp(self, input):
        return []
