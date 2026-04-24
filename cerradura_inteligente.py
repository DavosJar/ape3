ESTADO_INICIAL = "q0"
ESTADOS_FINALES = {"q1"}

TRANSICIONES = {
    "q0": {"C": "q1", "F": "q2"},
    "q1": {},
    "q2": {"C": "q1", "F": "q3"},
    "q3": {"C": "q1", "F": "q_error"},
    "q_error": {"C": "q_error", "F": "q_error"}
}

def validar_cerradura(cadena):
    estado_actual = ESTADO_INICIAL
    recorrido = [estado_actual]

    for simbolo in cadena:
        if simbolo not in {"C", "F"}:
            return {
                "valida": False,
                "estado_final": estado_actual,
                "recorrido": recorrido
            }

        if simbolo in TRANSICIONES[estado_actual]:
            estado_actual = TRANSICIONES[estado_actual][simbolo]
            recorrido.append(estado_actual)
        else:
            return {
                "valida": False,
                "estado_final": estado_actual,
                "recorrido": recorrido
            }

    if estado_actual in ESTADOS_FINALES:
        return {
            "valida": True,
            "estado_final": estado_actual,
            "recorrido": recorrido
        }
    elif estado_actual == "q_error":
        return {
            "valida": False,
            "estado_final": estado_actual,
            "recorrido": recorrido
        }
    else:
        return {
            "valida": False,
            "estado_final": estado_actual,
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