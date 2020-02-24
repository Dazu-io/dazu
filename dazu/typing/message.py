from typing import Any, Text

from dazu.constants import (
    CONTEXT_ATTRIBUTE,
    ENTITIES_ATTRIBUTE,
    INTENTS_ATTRIBUTE,
    OUTPUT_TEXT_ATTRIBUTE,
    TEXT_ATTRIBUTE,
)


class Message:
    def __init__(self, text: Text, context=None, data={}, time=None):
        self.input = {"text": text}
        self.context = context
        self.time = time
        self.data = data
        self.output = {"text": None}

        # if context is not None:
        # self.set(CONTEXT_ATTRIBUTE, context)

    def set(self, prop, info) -> None:
        if prop == OUTPUT_TEXT_ATTRIBUTE:
            self.output["text"] = info
            return
        self.data[prop] = info

    def get(self, prop, default=None) -> Any:
        if prop == TEXT_ATTRIBUTE:
            return self.input["text"]
        if prop == OUTPUT_TEXT_ATTRIBUTE:
            return self.output["text"]
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
