from typing import Any, Dict, Text

from david.constants import (
    CONTEXT_ATTRIBUTE,
    ENTITIES_ATTRIBUTE,
    INTENTS_ATTRIBUTE,
    TEXT_ATTRIBUTE,
)


class Message:
    def __init__(self, text: Text, context=None, data={}, time=None):
        self.input = {}
        self.input["text"] = text
        self.context = context
        self.time = time
        self.data = data
        self.output = None

        # if context is not None:
        # self.set(CONTEXT_ATTRIBUTE, context)

    def set(self, prop, info, add_to_output=False) -> None:
        self.data[prop] = info
        # if add_to_output:
        #     self.output_properties.add(prop)

    def get(self, prop, default=None) -> Any:
        if prop == TEXT_ATTRIBUTE:
            return self.input["text"]
        return self.data.get(prop, default)

    @classmethod
    def build(
        cls, text=None, intents=None, entities=None, context=None, payload=None
    ) -> "Message":
        data = {}

        if intents:
            # split_intent, response_key = cls.separate_intent_response_key(intent)
            data[INTENTS_ATTRIBUTE] = intents
            # if response_key:
            # data[RESPONSE_KEY_ATTRIBUTE] = response_key

        if entities:
            data[ENTITIES_ATTRIBUTE] = entities

        if context:
            data[CONTEXT_ATTRIBUTE] = context

        if not text:
            text = payload["input"]["text"]

        return cls(text, data)
