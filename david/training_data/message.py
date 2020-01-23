
from typing import Dict, Text, Any

from david.constants import (
    ENTITIES_ATTRIBUTE,
    INTENTS_ATTRIBUTE,
    TEXT_ATTRIBUTE,
    CONTEXT_ATTRIBUTE
)

class Message():
    def __init__(self, text: Text, context=None, data={}, time=None):
        self.text = text
        self.context = context
        self.time = time
        self.data = data

        #if context is not None:
           #self.set(CONTEXT_ATTRIBUTE, context)

    def set(self, prop, info, add_to_output=False) -> None:
        self.data[prop] = info
        if add_to_output:
            self.output_properties.add(prop)

    def get(self, prop, default=None) -> Any:
        if prop == TEXT_ATTRIBUTE:
            return self.text
        return self.data.get(prop, default)

    @classmethod
    def build(cls, text, intents=None, entities=None, context=None) -> "Message":
        data = {}
        if intents:
            #split_intent, response_key = cls.separate_intent_response_key(intent)
            data[INTENTS_ATTRIBUTE] = intents
            #if response_key:
                #data[RESPONSE_KEY_ATTRIBUTE] = response_key
        if entities:
            data[ENTITIES_ATTRIBUTE] = entities
        if context:
            data[CONTEXT_ATTRIBUTE] = context    
        return cls(text, data)    
