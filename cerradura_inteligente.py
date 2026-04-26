from enum import Enum

class Estados(Enum):
    q0 = "INICIO"
    q1 = "ACEPTACION"
    q2 = "ESPERA"
    q3 = "FALLO_PARCIAL"
    q_error = "FALLO"

TRANSICIONES = {
    Estados.q0: {"C": Estados.q1, "F": Estados.q2},
    Estados.q1: {},
    Estados.q2: {"C": Estados.q1, "F": Estados.q3},
    Estados.q3: {"C": Estados.q1, "F": Estados.q_error},
    Estados.q_error: {"C": Estados.q_error, "F": Estados.q_error}
}

ESTADO_INICIAL = Estados.q0
ESTADOS_FINALES = {Estados.q1}

def validar_cerradura(cadena):
    estado_actual = ESTADO_INICIAL
    recorrido = [estado_actual.name]

    for simbolo in cadena:
        if simbolo not in {"C", "F"}:
            return {
                "valida": False,
                "estado_final": estado_actual.name,
                "recorrido": recorrido
            }

        if simbolo in TRANSICIONES[estado_actual]:
            estado_actual = TRANSICIONES[estado_actual][simbolo]
            recorrido.append(estado_actual.name)
        else:
            return {
                "valida": False,
                "estado_final": estado_actual.name,
                "recorrido": recorrido
            }

    if estado_actual in ESTADOS_FINALES:
        return {
            "valida": True,
            "estado_final": estado_actual.name,
            "recorrido": recorrido
        }
    elif estado_actual == Estados.q_error:
        return {
            "valida": False,
            "estado_final": estado_actual.name,
            "recorrido": recorrido
        }
    else:
        return {
            "valida": False,
            "estado_final": estado_actual.name,
            "recorrido": recorrido
        }

# Pruebas
pruebas = ["C", "CCC", "FFFFFFFF", "FCF", "FC", "FFC", "FFFC"]

for prueba in pruebas:
    resultado = validar_cerradura(prueba)
    print(f"\nCadena: {prueba}")
    print("Recorrido:", " -> ".join(resultado["recorrido"]))
    print("Estado final:", resultado["estado_final"])
    print("Resultado:", "ACEPTADA" if resultado["valida"] else "RECHAZADA")