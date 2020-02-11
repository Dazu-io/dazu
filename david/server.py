from sanic import Sanic
from sanic.exceptions import abort
from sanic.response import json, text

from david.components.engine import Engine
from david.config import DavidConfig
from david.registry import Registry

app = Sanic()


@app.route("/")
def hi(request):
    text("Hi, am i David!")


@app.route("/dialog", methods=["POST"])
def dialog(request):
    requestData = request.json

    adapterName = request.get_args().get("adapter")
    adapter = Registry.getAdapter(Server.config, adapterName)

    if not adapter:
        abort(400)
        text("Invalid adapter")
        return

    if not adapter.validade_data(requestData):
        abort(400)
        text("Invalid input")
        return

    messageIn = adapter.input(requestData)
    messageOut = Server.engine.respond(messageIn)
    responseData = adapter.output(messageOut)
    return json(responseData)


class Server:

    config: DavidConfig = None

    engine: Engine = None

    @classmethod
    def prepare(cls, config: DavidConfig, engine: Engine):
        cls.config = config
        cls.engine = engine

    @classmethod
    def start(cls) -> None:
        app.run(host="0.0.0.0", port=5000)
