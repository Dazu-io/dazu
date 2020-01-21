from david.brain import Brain
from david.dialog import Dialog

class Assistant:

    def __init__(self):
        self.brain = Brain()
        self.dialog = Dialog()
        self.train()

    def train(self):
        self.brain.train()
        self.dialog.train()

    def respond(self, input, context = {}):
        intents = self.brain.classify(input)
        entities = self.brain.nlp(input)
        #print("intents", intents)
        dialog_node = self.dialog.dialog(input, context, intents, entities)
        return {
            "context": context,
            "intents": intents,
            "entities": entities,
            "output": dialog_node["output"]
        }   