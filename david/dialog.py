import json


def fetch_dialog():
    with open("./data/dialog.json") as f:
        dialog = json.load(f)
        f.close()
        return dialog


def persist_dialog(data):
    with open("./data/dialog.json", "w") as outfile:
        json.dump(data, outfile)


def get_dialog_welcome(dialog_nodes):
    return dialog_nodes[0]


def get_dialog_anythinelse(dialog_nodes):
    return dialog_nodes[len(dialog_nodes) - 1]


def evalCondition(condition, context, intent, entities):
    return condition == "#" + intent


class Dialog:
    def __init__(self):
        self.train()

    def train(self):
        self.dialog_nodes = fetch_dialog()

    def dialog(self, input, context, intents, entities):
        if input == "":
            return get_dialog_welcome(self.dialog_nodes)

        if len(intents) > 0:
            intent = intents[0]["intent"]
            for dialog_node in self.dialog_nodes:
                if evalCondition(dialog_node["condition"], context, intent, entities):
                    return dialog_node

        return get_dialog_anythinelse(self.dialog_nodes)
