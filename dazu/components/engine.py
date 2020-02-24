import os
from typing import List, Type

from dazu.components import Component
from dazu.config import DazuConfig
from dazu.constants import DEFAULT_MODELS_PATH, TEXT_ATTRIBUTE
from dazu.registry import Registry
from dazu.training_data.formats import JsonReader
from dazu.typing import Message


def build_model_filename(idx, componentCls: Type[Component]):
    return "{}_{}".format(idx, componentCls.name())


class Engine:

    pipeline: List[Type[Component]] = []

    components: List[Component] = []

    def __init__(self, config: DazuConfig):
        self.config = config

        self.pipeline = [
            Registry.get(moduleName=componentRef["name"])
            for componentRef in self.config.pipeline
        ]

        self.train()  # TODO(ralphg6) Remove when create 'train' command in CLI

        # self.__load() # TODO(ralphg6) Uncomment when create 'train' command in CLI

    def __load(self):
        self.components = [
            componentCls.load(
                {"file": build_model_filename(idx, componentCls)},
                model_dir=DEFAULT_MODELS_PATH,
            )
            for idx, componentCls in enumerate(self.pipeline, start=1)
        ]

    def train(self):
        models_dir = DEFAULT_MODELS_PATH
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)

        training_data = JsonReader.load(self.config)

        if len(self.components) == 0:
            self.components = [
                componentCls.create({}, self.config) for componentCls in self.pipeline
            ]

        for idx, component in enumerate(self.components, start=1):
            component.train(training_data, self.config)
            component.persist(
                file_name=build_model_filename(idx, type(component)),
                model_dir=models_dir,
            )

    def respond(self, message, context={}):
        text = message.get(TEXT_ATTRIBUTE)
        message = Message.build(text)

        for component in self.components:
            component.process(message)

        return message
