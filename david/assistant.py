from david.components.dialogue import WatsonAlternative
from david.components.nlu import SimpleNLU
from david.config import DavidConfig
from david.constants import DEFAULT_DATA_PATH, DEFAULT_MODELS_PATH, TEXT_ATTRIBUTE
from david.training_data.formats import JsonReader
from david.typing import Message

MODEL_FILE = "intent_model.json"
DIALOG_FILE = "dialog.json"


class Assistant:
    def __init__(self, config: DavidConfig):
        self.config = config
        self.dialog = WatsonAlternative.load(
            {"file": DIALOG_FILE}, model_dir=DEFAULT_DATA_PATH
        )
        self.nlu = SimpleNLU.create({}, self.config)
        self.train()

    def train(self):
        training_data = JsonReader.load(self.config)
        self.nlu.train(training_data, self.config)
        self.nlu.persist(file_name=MODEL_FILE, model_dir=DEFAULT_MODELS_PATH)

    def respond(self, message, context={}):
        text = message.get(TEXT_ATTRIBUTE)
        message = Message.build(text)

        self.nlu.process(message)
        self.dialog.process(message)

        return message
