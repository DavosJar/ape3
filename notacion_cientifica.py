from enum import Enum

#estados de q0 iniacial a q7 de aceptación
class Estados(Enum):
    q0 = 0
    q1 = 1
    q2 = 2
    q3 = 3
    q4 = 4
    q5 = 5
    q6 = 6
    q7 = 7
    fallo = -1 


#transiciones del automata
#dos patrones numericos de 1 a 9 y de 0 a 9 respectivamente

x = '0123456789'
d = '123456789'
signos = '+-'
punto = '.'
e = 'eE'


transiciones = {
    Estados.q0: {signos: Estados.q1, d: Estados.q2},
    Estados.q1: {d: Estados.q2},
    Estados.q2: {punto: Estados.q3, e: Estados.q5},
    Estados.q3: {x: Estados.q4},
    Estados.q4: {x: Estados.q4, e: Estados.q5},
    Estados.q5: {signos: Estados.q6, x: Estados.q7},
    Estados.q6: {x: Estados.q7},
    Estados.q7: {x: Estados.q7, e: Estados.fallo, punto: Estados.fallo}
}

def es_valido(cadena):
    estado_actual = Estados.q0

    for caracter in cadena:
        estado_siguiente = Estados.fallo
        for patron, siguiente_estado in transiciones.get(estado_actual, {}).items():
            if caracter in patron:
                estado_siguiente = siguiente_estado
        estado_actual = estado_siguiente

    return estado_actual == Estados.q7

# Pruebas
def main():
    ## solo son validas las cadenas que teminen en q7, es decir, que terminen con un numero despues de la e o E
    pruebas = [
        "123",          # No válido
        "-123.45",      # No válido
        "+0.99e-10",    # No válido
        "1e10",         # Válido
        "12.34.56",     # No válido
        "1e0",           # Válido
        ".5",           # No válido
        "1E-5.3"        # No válido
    ]

    for prueba in pruebas:
        resultado = es_valido(prueba)
        print(f"{prueba}: {'Válido' if resultado else 'No válido'}")
        
if __name__ == "__main__":
    main()