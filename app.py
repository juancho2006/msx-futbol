from flask import Flask, jsonify

app = Flask(__name__)

def msx_data():
    return {
        "name": "Fútbol en Vivo",
        "version": "1.0",
        "type": "list",
        # ... tu contenido actual de msx.json
    }

@app.route("/")          # <-- esto es lo que falta
def root():
    response = jsonify(msx_data())
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/msx.json")  # mantén la ruta original
def msx_json():
    response = jsonify(msx_data())
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
