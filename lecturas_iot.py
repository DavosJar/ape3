from enum import Enum
#alfabeto {"HDR", "TEMP", "HUM", "CRC"}
#Expresiones regulares HDR (TEMP | HUM)* CRC

class Estados(Enum):
    q0 = 0
    q1 = 1
    q2 = 2
    q3 = 3
    q_fallo = -1
    
transiciones = {
    Estados.q0: {
        "HDR": [Estados.q1],
        "TEMP": [Estados.q_fallo],
        "HUM": [Estados.q_fallo],
        "CRC": [Estados.q_fallo]
    },
    Estados.q1: {
        "HDR": [Estados.q_fallo],
        "TEMP": [Estados.q1, Estados.q2],  # no determinismo
        "HUM": [Estados.q1, Estados.q2],  # no determinismo
        "CRC": [Estados.q2]
    },
    Estados.q2: {
        "HDR": [Estados.q_fallo],
        "TEMP": [Estados.q_fallo],
        "HUM": [Estados.q_fallo],
        "CRC": [Estados.q3]
    },
    Estados.q3: {
        "HDR": [Estados.q_fallo],
        "TEMP": [Estados.q_fallo],
        "HUM": [Estados.q_fallo],
        "CRC": [Estados.q_fallo]
    },
    Estados.q_fallo: {}
        
}

def procesar_afn(tabla, estado_inicial, estados_aceptacion, cadena):
    estados_actuales = {estado_inicial}  # conjunto de estados activos

    for simbolo in cadena:
        siguientes = set()
        for estado in estados_actuales:
            destinos = tabla[estado].get(simbolo, [])
            siguientes.update(destinos) 
        estados_actuales = siguientes

    return bool(estados_actuales & estados_aceptacion)

def main():
    estado_inicial = Estados.q0
    estados_aceptacion = {Estados.q3}
    cadenas = [["HDR", "TEMP", "HUM", "CRC"], ## Aceptada
               ["HDR", "TEMP", "TEMP", "HUM", "CRC"], ## Aceptada
               ["HDR", "CRC"], ## Rechazada
               ["TEMP", "HUM", "CRC"], ## Rechazada
               ["HDR", "HUM", "HUM", "CRC"]## Aceptada
               ] 
            

    for cadena in cadenas:
        resultado = procesar_afn(transiciones, estado_inicial, estados_aceptacion, cadena)
        print(f"Cadena: {cadena} -> {'Aceptada' if resultado else 'Rechazada'}")

if __name__ == "__main__":
    main()