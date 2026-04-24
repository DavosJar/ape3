ESTADO_INICIAL = "q0"
ESTADOS_FINALES = {"q4"}

TRANSICIONES = {
    "q0": { "Autorizar": "q1"},
    "q1": { "Capturar": "q2", "Cancelar": "q_error" },
    "q2": { "Liquidar": "q3", "Cancelar": "q_error" },
    "q3": { "Completar": "q4", "Cancelar": "q_error" },
    "q4": {},
    "q_error": {}
}


def validar_transaccion(eventos):
    estado_actual = ESTADO_INICIAL
    recorrido = [estado_actual]

    for evento in eventos:
        if evento in TRANSICIONES[estado_actual]:
            estado_actual = TRANSICIONES[estado_actual][evento]
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

pruebas = [
    ["Autorizar", "Capturar", "Liquidar", "Completar"],   
    ["Autorizar", "Cancelar"],                            
    ["Autorizar", "Capturar", "Cancelar"],                
    ["Autorizar", "Liquidar"],                            
    ["Capturar", "Liquidar"],                             
]

for i, prueba in enumerate(pruebas, start=1):
    resultado = validar_transaccion(prueba)
    print(f"\nPrueba {i}: {prueba}")
    print("Recorrido:", " -> ".join(resultado["recorrido"]))
    print("Estado final:", resultado["estado_final"])
    print("Resultado:", "ACEPTADA" if resultado["valida"] else "RECHAZADA")