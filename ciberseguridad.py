from enum import Enum

alfabeto = ["ACK","SYN","DATA","RST"]
class estados(Enum):
    q0 = "INCIAL"
    q1 = "SINCRONIZACION"
    q2 = "ESTABLECIMIENTO"
    q3 = "ACEPTACION"
    q_fallo = "FALLO"

tabla_transiciones = {
    estados.q0: {
        "SYN":  [estados.q1],
        "ACK":  [estados.q_fallo],
        "DATA": [estados.q_fallo],
        "RST":  [estados.q_fallo]
    },
    estados.q1: {
        "SYN":  [estados.q_fallo],
        "ACK":  [estados.q1, estados.q2],  # no determinismo
        "DATA": [estados.q_fallo],
        "RST":  [estados.q_fallo]
    },
    estados.q2: {
        "SYN":  [estados.q_fallo],
        "ACK":  [estados.q_fallo],
        "DATA": [estados.q_fallo],
        "RST":  [estados.q3]      
    },
    estados.q3: {
        "SYN":  [estados.q_fallo],
        "ACK":  [estados.q_fallo],
        "DATA": [estados.q_fallo],
        "RST":  [estados.q_fallo]
    },
    estados.q_fallo: {
        "SYN":  [estados.q_fallo],
        "ACK":  [estados.q_fallo],
        "DATA": [estados.q_fallo],
        "RST":  [estados.q_fallo]
    }
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
    estado_inicial = estados.q0
    estados_aceptacion = {estados.q3}
    cadenas = [["SYN", "ACK", "RST"], 
               ["SYN", "ACK", "ACK","ACK","ACK","ACK","ACK","RST"],
               ["SYN", "ACK"],
               ["SYN", "ACK", "DATA", "RST"]]
    
    for cadena in cadenas:
        resultado = procesar_afn(tabla_transiciones, estado_inicial, estados_aceptacion, cadena)
        print(f"Cadena {cadena} aceptada: {resultado}")
    
if __name__ == "__main__":
    main()