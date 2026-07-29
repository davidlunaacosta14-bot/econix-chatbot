from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"

# Diccionario para interpretar rápidamente los números
OPCIONES_MENU = {
    "1": "El usuario seleccionó la Opción 1 (Conocer productos). Explícale brevemente sobre las pinturas ecológicas ideales para tareas y manualidades.",
    "2": "El usuario seleccionó la Opción 2 (Beneficios). Explícale brevemente que son fáciles de aplicar y reducen el impacto ambiental.",
    "3": "El usuario seleccionó la Opción 3 (Precios y promociones). Menciónale los envases de 325 ml y sus promociones.",
    "4": "El usuario seleccionó la Opción 4 (Preguntas frecuentes). Confírmale que sirven para papel, cartón y cartulina.",
    "5": "El usuario seleccionó la Opción 5 (Realizar un pedido). Pídele de forma amable su nombre, color deseado y cantidad de envases."
}

SYSTEM_PROMPT = """
Eres EcoBot, el asistente virtual de EcoNix (pinturas ecológicas).
Tu objetivo es responder de forma BREVE, LIMPIA y MUY ORDENADA.

BASE DE CONOCIMIENTO:
- Productos: Pinturas ecológicas para tareas, maquetas y proyectos escolares. Excelente cobertura en papel, cartón y cartulina.
- Beneficios: Fáciles de aplicar, buena cobertura y reducen el impacto ambiental.
- Precios y promociones: Envases de 325 ml a precios accesibles y promociones especiales.
- Preguntas frecuentes: Sirven para papel, cartón y cartulina. Si dudan de su calidad, aclara que ofrecen un acabado increíble siendo ecológicas.
- Pedidos: Solicitar color, cantidad de envases y nombre del cliente.

REGLAS DE FORMATO ESTRICTAS:
- Sé conciso y directo.
- NO vuelvas a mostrar el menú completo si el usuario ya eligió una opción o hizo una pregunta específica.
- Responde SIEMPRE en español.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    datos = request.json
    mensaje_usuario = datos.get("message", "").strip()

    if not mensaje_usuario:
        return jsonify({"error": "El mensaje no puede estar vacío"}), 400

    # Si el usuario escribe un número del 1 al 5, traducimos el mensaje para Ollama
    consulta = OPCIONES_MENU.get(mensaje_usuario, mensaje_usuario)

    prompt_completo = f"{SYSTEM_PROMPT}\n\nCliente: {consulta}\nEcoBot:"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt_completo,
        "stream": False
    }

    try:
        respuesta = requests.post(OLLAMA_URL, json=payload, timeout=60)
        datos_ollama = respuesta.json()
        texto_respuesta = datos_ollama.get("response", "No se obtuvo respuesta.")
        
        return jsonify({"response": texto_respuesta.strip()})

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "No se pudo conectar con Ollama."}), 500
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000)