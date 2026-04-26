from enum import Enum

class Estados(Enum):
    q0 = "INICIO"
    q1 = "AUTORIZADO"
    q2 = "CAPTURADO"
    q3 = "LIQUIDADO"
    q4 = "COMPLETADO"
    q_error = "CANCELADO"

TRANSICIONES = {
    Estados.q0: {"Autorizar": Estados.q1},
    Estados.q1: {"Capturar": Estados.q2, "Cancelar": Estados.q_error},
    Estados.q2: {"Liquidar": Estados.q3, "Cancelar": Estados.q_error},
    Estados.q3: {"Completar": Estados.q4, "Cancelar": Estados.q_error},
    Estados.q4: {},
    Estados.q_error: {}
}

ESTADO_INICIAL = Estados.q0
ESTADOS_FINALES = {Estados.q4}


def validar_transaccion(eventos):
    estado_actual = ESTADO_INICIAL
    recorrido = [estado_actual.name]

    for evento in eventos:
        if evento in TRANSICIONES[estado_actual]:
            estado_actual = TRANSICIONES[estado_actual][evento]
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