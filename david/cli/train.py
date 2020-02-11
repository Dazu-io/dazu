from david.components.engine import Engine
from david.config import DavidConfig


def train(config: DavidConfig):
    engine = Engine(config)
    engine.train()
