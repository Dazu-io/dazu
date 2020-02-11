from sanic import Sanic
from sanic.exceptions import abort
from sanic.response import json, text
from sanic_openapi import doc, swagger_blueprint

from david import version
from david.components.engine import Engine
from david.config import DavidConfig
from david.registry import Registry

app = Sanic()
app.blueprint(swagger_blueprint,)

app.config["API_BASEPATH"] = "/api"
app.config["API_TITLE"] = "David"
app.config["API_VERSION"] = version.__version__


@app.route("/")
@doc.exclude(True)
def hi(request):
    text("Hi, am i David!")


@app.post("/api/v1/dialog")
def dialog(request):
    requestData = request.json
    return process_dialog(requestData)


@app.post("/api/v1/dialog/<adapter_name:path>")
def dialogAdopted(request, adapter_name):
    requestData = request.json
    return process_dialog(requestData, adapter_name)


def process_dialog(requestData, adapter_name=None):
    adapter = Registry.getAdapter(Server.config, adapter_name)

    if not adapter:
        abort(404, "Invalid adapter")

    if not adapter.validade_data(requestData):
        abort(400, "Invalid input")

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
