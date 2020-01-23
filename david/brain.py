import json
import david.util as util
import os


from david.components.nlu.simplenlu import SimpleNLU

from david.config import DavidConfig

from david.training_data import Message


MODEL_DIR = './models/'
MODEL_FILE = 'intent_model.json'
KNOW_FILE = './data/know.json'


def fetch_know():
    with open(KNOW_FILE) as f:
        return json.load(f)

def persist_know(data):
    with open(KNOW_FILE, 'w') as outfile:
        json.dump(data, outfile)



# def persist_stopwords(data):
#     with open('./data/stopwords.json', 'w') as outfile:
#         json.dump(data, outfile)


class Brain:

    def __init__(self):
        # print("brain inited")
        self.train()

    def train(self) -> None:
        from david.training_data import TrainingData
        
        know = fetch_know()

        training_data = TrainingData(know)
        config = DavidConfig()
        self.nlu = SimpleNLU.create({}, config)
        self.nlu.train(training_data, config)
        self.nlu.persist(file_name=MODEL_FILE, model_dir=MODEL_DIR)

    def process(self, text) -> Message:
        message = Message.build(text)
        self.nlu.process(message)
        return message


    def nlp(self, input):
        return []