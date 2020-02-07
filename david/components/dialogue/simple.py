import json
import os
from typing import Any, Dict, Optional, Text

from david.components.component import Component
from david.config import DavidConfig
from david.constants import (
    CONTEXT_ATTRIBUTE,
    ENTITIES_ATTRIBUTE,
    INTENTS_ATTRIBUTE,
    OUTPUT_TEXT_ATTRIBUTE,
    TEXT_ATTRIBUTE,
)
from david.registry import Registry
from david.typing import Message, TrainingData
from david.typing.model import Metadata


def get_dialog_welcome(dialog_nodes):
    return dialog_nodes[0]


def get_dialog_anythinelse(dialog_nodes):
    return dialog_nodes[len(dialog_nodes) - 1]


def evalCondition(condition, context, intent, entities):
    return condition == "#" + intent


class SimpleDialogue(Component):
    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
        dialog_nodes: Dict = None,
    ) -> None:
        super().__init__(component_config)

        self.dialog_nodes = dialog_nodes

    @classmethod
    def name(cls):
        return "dialogue_simple"

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
                dialog_nodes = json.load(f)
                return cls(meta, dialog_nodes)
        else:
            return cls(meta)

    def train(
        self, training_data: TrainingData, cfg: DavidConfig, **kwargs: Any
    ) -> None:

        self.dialog_nodes = training_data.data["dialogue"]

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        model_file = os.path.join(model_dir, file_name)
        with open(model_file, "w") as outfile:
            json.dump(self.dialog_nodes, outfile)

    def process(self, message: Message, **kwargs: Any) -> None:

        text = message.get(TEXT_ATTRIBUTE)
        intents = message.get(INTENTS_ATTRIBUTE)
        entities = message.get(ENTITIES_ATTRIBUTE)
        context = message.get(CONTEXT_ATTRIBUTE)

        dialog_node = self.__dialog(text, context, intents, entities)

        message.set(OUTPUT_TEXT_ATTRIBUTE, dialog_node["output"]["text"])

    def __dialog(self, input, context, intents, entities):
        if input == "":
            return get_dialog_welcome(self.dialog_nodes)

        if len(intents) > 0:
            intent = intents[0]["intent"]
            for dialog_node in self.dialog_nodes:
                if evalCondition(dialog_node["condition"], context, intent, entities):
                    return dialog_node

        return get_dialog_anythinelse(self.dialog_nodes)


Registry.registry(SimpleDialogue)
