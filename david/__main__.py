from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

from david.assistant import Assistant
from david.dialog import fetch_dialog
from david.googleadap import GoogleWebHook
from david.registry import Registry

# from david.brain import fetch_model, fetch_know

app = Flask(__name__)
CORS(app)

assistant = Assistant()
googleWH = GoogleWebHook(assistant)

registry = Registry.get_instance()


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

    # [TODO] receive adapter from query string
    adapter = registry.getAdapter()

    if not adapter.validade_data(requestData):
        # [TODO] send status code 400
        return jsonify(error="invalid input")

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
