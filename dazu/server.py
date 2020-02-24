from sanic import Sanic

from dazu import version
from dazu.components.engine import Engine
from dazu.config import DazuConfig
from dazu.routes import router


class Server:

    config: DazuConfig

    engine: Engine

    @classmethod
    def start(cls, config: DazuConfig, engine: Engine):

        cls.config = config

        cls.engine = engine

        app = Sanic()

        # app.config['DAVID_CONFIG', config]
        # app.config['DAVID_ENGINE', engine]

        app.config["API_BASEPATH"] = "/api"
        app.config["API_TITLE"] = "Dazu"
        app.config["API_VERSION"] = version.__version__

        app.blueprint(router)

        app.run(host="0.0.0.0", port=5000)
