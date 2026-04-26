from flask import Flask, request, jsonify

app = Flask(__name__)

ESTADO_INICIAL = "q0"
ESTADOS_FINALES = {"q3"}
ALFABETO = {"HOME", "SEARCH", "CART"}

TRANSICIONES = {
    "q0": {"HOME": "q1", "SEARCH": "q_error", "CART": "q_error"},
    "q1": {"HOME": "q_error", "SEARCH": "q2", "CART": "q_error"},
    "q2": {"HOME": "q_error", "SEARCH": "q2", "CART": "q3"},
    "q3": {"HOME": "q_error", "SEARCH": "q_error", "CART": "q_error"},
    "q_error": {"HOME": "q_error", "SEARCH": "q_error", "CART": "q_error"},
}

def simular_afd(tokens):
    estado_actual = ESTADO_INICIAL
    recorrido = [estado_actual]

    if len(tokens) == 0:
        return {
            "aceptada": False,
            "estado_final": "q0",
            "mensaje": "Secuencia vacía",
            "recorrido": recorrido
        }

    for token in tokens:
        token = token.upper()

        if token not in ALFABETO:
            return {
                "aceptada": False,
                "estado_final": "error",
                "mensaje": f"Evento inválido: {token}",
                "recorrido": recorrido
            }

        estado_actual = TRANSICIONES[estado_actual][token]
        recorrido.append(estado_actual)

    if estado_actual in ESTADOS_FINALES:
        return {
            "aceptada": True,
            "estado_final": estado_actual,
            "mensaje": "Usuario identificado como comprador potencial",
            "recorrido": recorrido
        }

    return {
        "aceptada": False,
        "estado_final": estado_actual,
        "mensaje": "El usuario no cumple el patrón HOME SEARCH+ CART",
        "recorrido": recorrido
    }

@app.route("/validar/comprador-potencial", methods=["POST"])
def validar_comprador_potencial():
    data = request.get_json()
    tokens = data.get("secuencia", [])
    resultado = simular_afd(tokens)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)