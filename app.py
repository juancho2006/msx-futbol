from flask import Flask, jsonify

app = Flask(__name__)

def get_msx_content():
    return {
        "name": "Fútbol MSX",
        "version": "1.0",
        "parameter": "menu:http://msx-futbol.onrender.com/menu",
        "menu": {
            # tu contenido aquí
        }
    }

# Ruta raíz — MSX puede acceder solo con el dominio
@app.route("/")
def root():
    return jsonify(get_msx_content())

# Mantén la ruta original también
@app.route("/msx.json")
def msx_json():
    return jsonify(get_msx_content())
