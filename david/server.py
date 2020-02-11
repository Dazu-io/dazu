from flask import Flask, abort, jsonify, request
from flask_cors import CORS

from david.components.engine import Engine
from david.config import DavidConfig
from david.registry import Registry

# from david.brain import fetch_model, fetch_know

app = Flask(__name__)
CORS(app)


@app.route("/")
def hi():
    return "Hi, am i David!"


# @app.route("/train")
# def train():
#     Server.engine.train()
#     return "OK"


@app.route("/dialog", methods=["POST"])
def dialog():
    requestData = request.get_json()

    adapterName = request.args.get("adapter")
    adapter = Registry.getAdapter(Server.config, adapterName)

    if not adapter:
        abort(400, "Invalid adapter")

    if not adapter.validade_data(requestData):
        abort(400, "Invalid input")

    messageIn = adapter.input(requestData)
    messageOut = Server.engine.respond(messageIn)
    responseData = adapter.output(messageOut)
    return jsonify(responseData)


class Server:

    config: DavidConfig = None

    engine: Engine = None

    @classmethod
    def prepare(cls, config: DavidConfig, engine: Engine):
        cls.config = config
        cls.engine = engine

    @classmethod
    def start(cls) -> None:
        app.run(host="0.0.0.0")
