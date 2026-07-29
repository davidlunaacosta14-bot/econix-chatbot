import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Lee la clave API que pusiste en las variables de entorno de Render
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

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
- Preguntas frecuentes: Sirven para papel, cartón y cartulina.
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

    if not client:
        return jsonify({"error": "No se configuró la GROQ_API_KEY en Render."}), 500

    consulta = OPCIONES_MENU.get(mensaje_usuario, mensaje_usuario)

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": consulta}
            ],
            temperature=0.6,
        )
        
        texto_respuesta = completion.choices[0].message.content
        return jsonify({"response": texto_respuesta.strip()})

    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
