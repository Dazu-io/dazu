from sanic import Sanic

from david import version
from david.components.engine import Engine
from david.config import DavidConfig
from david.routes import router


class Server:

    config: DavidConfig

    engine: Engine

    @classmethod
    def start(cls, config: DavidConfig, engine: Engine):

        cls.config = config

        cls.engine = engine

        app = Sanic()

        # app.config['DAVID_CONFIG', config]
        # app.config['DAVID_ENGINE', engine]

        app.config["API_BASEPATH"] = "/api"
        app.config["API_TITLE"] = "David"
        app.config["API_VERSION"] = version.__version__

        app.blueprint(router)

        app.run(host="0.0.0.0", port=5000)
