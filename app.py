from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    # Estructura mínima que Media Station X exige
    return jsonify({
        "name": "Mi Futbol",
        "version": "1.1",
        "parameter": "menu:start",
        "pages": [
            {
                "type": "menu",
                "id": "start",
                "title": "Partidos",
                "items": []
            }
        ]
    })

if __name__ == '__main__':
    app.run()
