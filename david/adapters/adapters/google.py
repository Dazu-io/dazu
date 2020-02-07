from typing import Dict

from david.adapters.adapter import Adapter
from david.registry import Registry
from david.typing import Message


class GoogleAdapter(Adapter):
    @classmethod
    def name(cls):
        return "google"

    @classmethod
    def validade_data(cls, payload: Dict) -> bool:
        return "queryResult" in payload and "queryText" in payload["queryResult"]

    @classmethod
    def input(cls, payload: Dict) -> Message:
        input = payload["queryResult"]["queryText"]
        return Message.build(input)

    @classmethod
    def output(cls, message: Message) -> Dict:
        return {"fulfillmentText": message.output["text"]}


Registry.registryAdapter(GoogleAdapter)
