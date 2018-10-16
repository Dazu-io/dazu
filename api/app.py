from flask import Flask, jsonify, request
from assistant import Assistant

import dialog
import brain

from google import GoogleWebHook

app = Flask(__name__)

assistant = Assistant()
googleWH = GoogleWebHook(assistant)

@app.route('/')
def hi():
    return 'Hi, am i David!'

@app.route('/train')
def train():
    assistant.train()
    return "OK"   

@app.route('/dialog', methods=['POST'])
def dialog():
    data = request.get_json()
    return jsonify(assistant.respond(data['input']))    
    
@app.route('/google', methods=['POST'])
def google():
    data = request.get_json()
    return jsonify(googleWH.handle(data))  

@app.route('/data/dialog')
def data_dialog():
    return jsonify(dialog.fetch_dialog())     

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')