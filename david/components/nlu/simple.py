import json
import os
import re
from typing import Any, Dict, List, Optional, Text

import unidecode
from Levenshtein import distance

from david.components import Component
from david.config import DavidConfig
from david.constants import INTENTS_ATTRIBUTE, TEXT_ATTRIBUTE
from david.registry import Registry
from david.typing import Message, TrainingData
from david.typing.model import Metadata

SIMMILARITY_ERROR_ACCEPTED = 0.3


NON_CONTENT = r"[^\w\d\s]"


def tokenize(stopwords: List[str], sentence: str):
    # print "sentence",sentence
    # remove accents
    sentence = unidecode.unidecode(sentence)
    # print "sentence1",sentence
    # remove non content
    sentence = re.sub(NON_CONTENT, "", sentence)
    # print "sentence2",sentence
    # lower
    sentence = sentence.lower()
    # print "sentence3",sentence
    # split
    tokens = sentence.split(" ")

    tokens = list(filter(lambda t: t not in stopwords, tokens))

    tokens = list(filter(lambda t: len(t) > 0, tokens))

    # print("tokens", tokens)

    return tokens


def simmilarity(a, b):
    d = distance(a, b)
    t = float(len(a) + len(b)) / 2
    if d / t <= SIMMILARITY_ERROR_ACCEPTED:
        return (t - d) / t
    return 0


class SimpleNLU(Component):
    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
        intent_model: Dict = None,
    ) -> None:

        super().__init__(component_config)

        self.intent_model = intent_model

    @classmethod
    def name(cls):
        return "nlu_simple"

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any,
    ) -> "Component":
        """Load this component from file.
        After a component has been trained, it will be persisted by
        calling `persist`. When the pipeline gets loaded again,
        this component needs to be able to restore itself.
        Components can rely on any context attributes that are
        created by :meth:`components.Component.create`
        calls to components previous
        to this one."""

        file_name = meta.get("file")
        model_file = os.path.join(model_dir, file_name)

        if os.path.exists(model_file):
            with open(model_file) as f:
                intent_model = json.load(f)
                return cls(meta, intent_model)
        else:
            return cls(meta)

    def train(
        self, training_data: TrainingData, cfg: DavidConfig, **kwargs: Any
    ) -> None:

        self.intent_model = {"stopwords": training_data.data["nlu"]["stopwords"]}

        intents = {}

        for intent, samples in training_data.data["nlu"]["intents"].items():
            intents[intent] = {}
            for sample in samples:
                intents[intent][sample] = {"total": 0, "tokens": {}}
                for t in tokenize(self.intent_model["stopwords"], sample):
                    intents[intent][sample]["total"] += 1
                    if t in intents[intent][sample]["tokens"]:
                        intents[intent][sample]["tokens"][t] += 1
                    else:
                        intents[intent][sample]["tokens"][t] = 1

        self.intent_model["intents"] = intents

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        model_file = os.path.join(model_dir, file_name)
        with open(model_file, "w") as outfile:
            json.dump(self.intent_model, outfile)

    def process(self, message: Message, **kwargs: Any) -> None:

        input = message.get(TEXT_ATTRIBUTE)

        tokens = tokenize(self.intent_model["stopwords"], input)
        # print ("tokens", tokens)
        intents = {}
        for intent, samples in self.intent_model["intents"].items():
            intents[intent] = 0
            for s, smeta in samples.items():
                brutal_score = 0
                stokens = smeta["tokens"]
                for t in tokens:
                    for st, value in stokens.items():
                        # print t, st, simmilarity(t, st), value
                        brutal_score += simmilarity(t, st) * value
                score = float(brutal_score) / smeta["total"]
                # print("brutal_score", s, brutal_score, smeta, intents[intent], score)
                if intents[intent] < score:
                    intents[intent] = score

        intents = [
            {"intent": intent, "confidence": intents[intent]}
            for intent in sorted(intents, key=intents.__getitem__, reverse=True)
        ]

        intents = list(filter(lambda i: i["confidence"] > 0, intents))

        message.set(INTENTS_ATTRIBUTE, intents[:10])


Registry.registry(SimpleNLU)
