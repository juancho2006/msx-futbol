import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/msx.json')
def home_msx():
    url = "https://futbol-libres.su/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    msx_json = {
        "name": "Fútbol Libre Auto",
        "version": "1.1",
        "parameter": "menu:start",
        "pages": [
            {
                "id": "start",
                "title": "Partidos de Hoy ⚽",
                "items": []
            }
        ]
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        partidos_encontrados = soup.find_all('tr')
        
        if not partidos_encontrados:
            msx_json["pages"][0]["items"].append({
                "type": "button",
                "title": "No se detectaron partidos activos",
                "description": "Revisar la web directamente",
                "icon": "https://img.icons8.com/color/96/info.png"
            })
            return jsonify(msx_json)

        for i, fila in enumerate(partidos_encontrados):
            texto_partido = fila.get_text(strip=True)
            link_elemento = fila.find('a')
            
            if len(texto_partido) > 5 and link_elemento:
                id_pagina_partido = f"partido_{i}"
                
                msx_json["pages"][0]["items"].append({
                    "type": "button",
                    "title": texto_partido,
                    "icon": "https://img.icons8.com/color/96/football.png",
                    "action": f"page:{id_pagina_partido}"
                })
                
                msx_json["pages"].append({
                    "id": id_pagina_partido,
                    "title": f"Canales: {texto_partido[:20]}...",
                    "items": [
                        {
                            "type": "video",
                            "title": "Transmisión Auto (HLS Stream)",
                            "description": "Clic para intentar reproducir flujo HLS",
                            "action": "video:https://emprw.vivolatamz.org/disney1/index.m3u8" 
                        }
                    ]
                })

    except Exception as e:
        msx_json["pages"][0]["items"].append({
            "type": "button",
            "title": "Error al conectar con la agenda",
            "description": str(e),
            "icon": "https://img.icons8.com/color/96/error.png"
        })

    return jsonify(msx_json)

# Permiso CORS para que la tele no bloquee la conexión
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run()
