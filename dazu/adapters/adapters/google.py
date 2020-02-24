from typing import Dict

from dazu.adapters.adapter import Adapter
from dazu.constants import OUTPUT_TEXT_ATTRIBUTE
from dazu.registry import Registry
from dazu.typing import Message


class GoogleAdapter(Adapter):
    @classmethod
    def name(cls):
        return "google"

    @classmethod
    def validate_data(cls, payload: Dict) -> bool:
        return "queryResult" in payload and "queryText" in payload["queryResult"]

    @classmethod
    def input(cls, payload: Dict) -> Message:
        inputData = payload["queryResult"]["queryText"]
        return Message.build(inputData)

    @classmethod
    def output(cls, message: Message) -> Dict:
        text = message.get(OUTPUT_TEXT_ATTRIBUTE)
        return {"fulfillmentText": text}


Registry.registryAdapter(GoogleAdapter)
