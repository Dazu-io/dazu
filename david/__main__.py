from flask import Flask, abort, jsonify, make_response, request
from flask_cors import CORS

import david.config
from david.adapters.adapter import MessageAdapter
from david.assistant import Assistant
from david.dialog import fetch_dialog
from david.googleadap import GoogleWebHook
from david.registry import Registry

# from david.brain import fetch_model, fetch_know

app = Flask(__name__)
CORS(app)

messageAdapter = MessageAdapter()

# [TODO] This kwargs must from CLI args
kwargs = {"default_adapter": messageAdapter.name}

config = david.config.load(None, **kwargs)

Registry.registryAdapter(messageAdapter)

assistant = Assistant(config)
googleWH = GoogleWebHook(assistant)


@app.route("/")
def hi():
    return "Hi, am i David!"


@app.route("/train")
def train():
    assistant.train()
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
    messageOut = assistant.respond(messageIn)
    responseData = adapter.output(messageOut)
    return jsonify(responseData)


@app.route("/google", methods=["POST"])
def google():
    data = request.get_json()
    return jsonify(googleWH.handle(data))


# @app.route('/data/dialog')
# def data_dialog():
# return jsonify(fetch_dialog())

# @app.route('/data/know')
# def data_know():
# return jsonify(fetch_know())


def main() -> None:
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
