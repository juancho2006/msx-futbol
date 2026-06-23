from flask import Flask, jsonify, request

app = Flask(__name__)

# Esta es la parte clave: responde cuando entran a la dirección principal (sin nada más)
@app.route('/', methods=['GET', 'OPTIONS'])
def home_msx():
    if request.method == 'OPTIONS':
        return '', 200
        
    msx_json = {
        "name": "Fútbol Libre Auto",
        "version": "1.1",
        "parameter": "menu:http://localhost/start",
        "pages": [
            {
                "type": "menu",
                "id": "http://localhost/start",
                "title": "Partidos de Hoy ⚽",
                "items": [
                    {
                        "type": "button",
                        "title": "Configuración exitosa",
                        "description": "El servidor está funcionando correctamente."
                    }
                ]
            }
        ]
    }
    return jsonify(msx_json)

if __name__ == '__main__':
    app.run()
