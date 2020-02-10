from david.components.engine import Engine
from david.config import DavidConfig
from david.server import Server


def run(config):
    engine = Engine(config)

    Server.prepare(config, engine)
    Server.start()
