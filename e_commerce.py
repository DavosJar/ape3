from flask import Flask, request, jsonify
from enum import Enum

app = Flask(__name__)

class Estados(Enum):
    q0 = "INICIO"
    q1 = "HOME_VISITADO"
    q2 = "BUSQUEDA_REALIZADA"
    q3 = "CARRITO_LLENO"
    q_error = "ERROR"

ALFABETO = {"HOME", "SEARCH", "CART"}

TRANSICIONES = {
    Estados.q0: {"HOME": Estados.q1, "SEARCH": Estados.q_error, "CART": Estados.q_error},
    Estados.q1: {"HOME": Estados.q_error, "SEARCH": Estados.q2, "CART": Estados.q_error},
    Estados.q2: {"HOME": Estados.q_error, "SEARCH": Estados.q2, "CART": Estados.q3},
    Estados.q3: {"HOME": Estados.q_error, "SEARCH": Estados.q_error, "CART": Estados.q_error},
    Estados.q_error: {"HOME": Estados.q_error, "SEARCH": Estados.q_error, "CART": Estados.q_error},
}

ESTADO_INICIAL = Estados.q0
ESTADOS_FINALES = {Estados.q3}

def simular_afd(tokens):
    estado_actual = ESTADO_INICIAL
    recorrido = [estado_actual.name]

    if len(tokens) == 0:
        return {
            "aceptada": False,
            "estado_final": Estados.q0.name,
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
        recorrido.append(estado_actual.name)

    if estado_actual in ESTADOS_FINALES:
        return {
            "aceptada": True,
            "estado_final": estado_actual.name,
            "mensaje": "Usuario identificado como comprador potencial",
            "recorrido": recorrido
        }

    return {
        "aceptada": False,
        "estado_final": estado_actual.name,
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