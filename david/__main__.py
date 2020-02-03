from flask import Flask, jsonify, request
from flask_cors import CORS

from david.adapters.adapter import AdaptEngine
from david.assistant import Assistant
from david.dialog import fetch_dialog
from david.googleadap import GoogleWebHook

# from david.brain import fetch_model, fetch_know

app = Flask(__name__)
CORS(app)

assistant = Assistant()
googleWH = GoogleWebHook(assistant)

adapt_engine = AdaptEngine()


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
    messageIn = adapt_engine.input(requestData)
    messageOut = assistant.respond(messageIn)
    responseData = adapt_engine.output(messageOut)
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
