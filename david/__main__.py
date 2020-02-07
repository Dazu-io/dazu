from flask import Flask, abort, jsonify, make_response, request
from flask_cors import CORS

import david.config
from david.adapters.adapter import MessageAdapter
from david.components.dialogue import WatsonAlternative
from david.components.engine import Engine
from david.components.nlu import SimpleNLU
from david.constants import CONFIG_DEFAULT_ADAPTER
from david.registry import Registry

# from david.brain import fetch_model, fetch_know

app = Flask(__name__)
CORS(app)

# [TODO] This kwargs must from CLI args
kwargs = {CONFIG_DEFAULT_ADAPTER: MessageAdapter.name()}

config = david.config.load(None, **kwargs)

config.pipeline = [
    SimpleNLU,
    WatsonAlternative,
]

engine = Engine(config)


@app.route("/")
def hi():
    return "Hi, am i David!"


@app.route("/train")
def train():
    engine.train()
    return "OK"


@app.route("/dialog", methods=["POST"])
def dialog():
    requestData = request.get_json()

    adapterName = request.args.get("adapter")
    adapter = Registry.getAdapter(config, adapterName)

    if not adapter:
        abort(400, "Invalid adapter")

    if not adapter.validade_data(requestData):
        abort(400, "Invalid input")

    messageIn = adapter.input(requestData)
    messageOut = engine.respond(messageIn)
    responseData = adapter.output(messageOut)
    return jsonify(responseData)


def main() -> None:
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
