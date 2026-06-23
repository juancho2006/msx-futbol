import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

# Agregamos soporte explícito para peticiones GET y OPTIONS (las que manda la TV)
@app.route('/', methods=['GET', 'OPTIONS'])
@app.route('/msx.json', methods=['GET', 'OPTIONS'])
@app.route('/msx/start.json', methods=['GET', 'OPTIONS'])
def home_msx():
    # Si la TV pregunta si el servidor acepta conexiones (Preflight), le decimos que sí inmediatamente
    if request.method == 'OPTIONS':
        return '', 200

    url = "https://futbol-libres.su/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    msx_json = {
        "name": "Fútbol Libre Auto",
        "version": "1.1",
       "parameter": "menu:http://localhost/start",  # CORREGIDO: Ahora le dice a MSX que abra la PÁGINA inicial directamente
        "pages": [
            {
                "type": "menu",
                "id": "http://localhost/start"
                "title": "Partidos de Hoy ⚽",
                "items": []
            }
        ]
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        elementos = soup.find_all('tr')
        if not elementos:
            elementos = soup.find_all('div', class_='event') or soup.find_all('li')
        if not elementos:
            elementos = soup.find_all('a')
            
        partidos_agregados = 0

        for fila in elementos:
            texto_partido = fila.get_text(strip=True)
            link_elemento = fila if fila.name == 'a' else fila.find('a')
            
            palabras_basura = ["inicio", "contacto", "dmca", "canales", "en vivo", "política", "privacy", "copyright"]
            if any(basura in texto_partido.lower() for basura in palabras_basura):
                continue
                
            if len(texto_partido) > 6 and link_elemento:
                href_partido = link_elemento.get('href', '')
                if not href_partido.startswith('http'):
                    href_partido = "https://futbol-libres.su" + href_partido
                    
                id_pagina_partido = f"partido_{partidos_agregados}"
                
                msx_json["pages"][0]["items"].append({
                    "type": "button",
                    "title": texto_partido,
                    "icon": "https://img.icons8.com/color/96/football.png",
                    "action": f"page:{id_pagina_partido}"
                })
                
                msx_json["pages"].append({
                    "id": id_pagina_partido,
                    "title": f"Opciones: {texto_partido[:20]}",
                    "items": [
                        {
                            "type": "video",
                            "title": "Reproducir Transmisión Principal",
                            "description": "Se conecta de forma automática",
                            "action": f"video:https://emprw.vivolatamz.org/disney1/index.m3u8"
                        }
                    ]
                })
                partidos_agregados += 1

        if partidos_agregados == 0:
            msx_json["pages"][0]["items"].append({
                "type": "button",
                "title": "Sin partidos en este momento",
                "description": "La agenda de la web está vacía. Intenta más tarde.",
                "icon": "https://img.icons8.com/color/96/info.png"
            })

    except Exception as e:
        msx_json["pages"][0]["items"].append({
            "type": "button",
            "title": "Error al conectar con la agenda",
            "description": str(e),
            "icon": "https://img.icons8.com/color/96/error.png"
        })

    return jsonify(msx_json)

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run()
