import os
from flask import Flask, jsonify, request

app = Flask(__name__)

def msx_data():
    stream_url = os.environ.get("STREAM_URL", "")
    partido = os.environ.get("PARTIDO", "Partido en Vivo")
    return {
        "name": "Fútbol en Vivo",
        "version": "1.0",
        "type": "list",
        "items": [
            {
                "label": partido,
                "type": "video",
                "action": f"video:{stream_url}"
            }
        ]
    }

def make_response(data):
    response = jsonify(data)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/")
def root():
    return make_response(msx_data())

@app.route("/msx.json")
def msx_json():
    return make_response(msx_data())

@app.route("/msx/start.json")   # <-- esto es lo que MSX busca
def msx_start():
    return make_response(msx_data())
