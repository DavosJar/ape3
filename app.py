from flask import Flask, render_template, request, jsonify, send_from_directory
from cerradura_inteligente import validar_cerradura as _validar_cerradura, TRANSICIONES as TRANS_CERRADURA, ESTADO_INICIAL as INICIAL_CERRADURA, ESTADOS_FINALES as FINALES_CERRADURA
from ciberseguridad import procesar_afn as _procesar_afn_ciberseguridad, tabla_transiciones as TRANS_CIBERSEGURIDAD, estados as Estados_Ciberseguridad
from lecturas_iot import procesar_afn as _procesar_afn_iot, transiciones as TRANS_IOT, Estados as Estados_IOT
from notacion_cientifica import es_valido as _es_valido
from transaccion_bancaria import validar_transaccion as _validar_transaccion, TRANSICIONES as TRANS_TRANSACCION, ESTADO_INICIAL as INICIAL_TRANSACCION, ESTADOS_FINALES as FINALES_TRANSACCION
from e_commerce import simular_afd as _simular_afd, TRANSICIONES as TRANS_ECOMMERCE, ESTADO_INICIAL as INICIAL_ECOMMERCE, ESTADOS_FINALES as FINALES_ECOMMERCE

app = Flask(__name__)


class GeneradorDiagrama:
    @staticmethod
    def generar_tabla_html(transiciones, estados, estados_finales=None, es_afn=False):
        if not estados:
            return "<p>No hay estados disponibles</p>"
        
        simbolos = set()
        for estado in transiciones:
            simbolos.update(transiciones[estado].keys())
        simbolos = sorted(list(simbolos))
        
        html = '<table border="1" cellpadding="8" cellspacing="0" class="tabla-transiciones">'
        html += '<tr><th>Estado</th>'
        for simbolo in simbolos:
            html += f'<th>{simbolo}</th>'
        html += '</tr>'
        
        for estado in estados:
            html += '<tr>'
            color = '#90EE90' if estado in (estados_finales or []) else '#FFFFFF'
            html += f'<td style="background-color: {color}; font-weight: bold;">{estado}</td>'
            for simbolo in simbolos:
                destinos = transiciones.get(estado, {}).get(simbolo, [])
                if es_afn:
                    dest_str = ", ".join(str(d) for d in destinos) if destinos else "-"
                else:
                    dest_str = str(destinos) if destinos else "-"
                html += f'<td>{dest_str}</td>'
            html += '</tr>'
        
        html += '</table>'
        return html


class CerraduraInteligente:
    def __init__(self):
        self.transiciones = TRANS_CERRADURA
        self.estado_inicial = INICIAL_CERRADURA
        self.estados_finales = FINALES_CERRADURA
        self.estados = list(self.transiciones.keys())
    
    def ejecutar(self, cadena):
        return _validar_cerradura(cadena)
    
    def obtener_tabla_html(self):
        return GeneradorDiagrama.generar_tabla_html(
            self.transiciones, 
            self.estados, 
            self.estados_finales
        )
    
    def obtener_diagrama_filename(self):
        return "cerradura.png"
    
    def obtener_ejemplos(self):
        return ["C", "FC", "CCC", "FFC", "FFFC"]


class Ciberseguridad:
    def __init__(self):
        self.tabla_transiciones = TRANS_CIBERSEGURIDAD
        self.estado_inicial = Estados_Ciberseguridad.q0
        self.estados_aceptacion = {Estados_Ciberseguridad.q3}
        self.estados = list(TRANS_CIBERSEGURIDAD.keys())
        self.alfabeto = ["SYN", "ACK", "DATA", "RST"]
    
    def ejecutar(self, cadena_lista):
        resultado = _procesar_afn_ciberseguridad(
            self.tabla_transiciones,
            self.estado_inicial,
            self.estados_aceptacion,
            cadena_lista
        )
        return {
            "valida": resultado,
            "estado_final": "aceptado" if resultado else "rechazado"
        }
    
    def obtener_tabla_html(self):
        trans_simplificada = {}
        for estado in TRANS_CIBERSEGURIDAD:
            trans_simplificada[estado.name] = {}
            for simbolo, destinos in TRANS_CIBERSEGURIDAD[estado].items():
                trans_simplificada[estado.name][simbolo] = [d.name for d in destinos]
        
        estados_nombres = [e.name for e in self.estados]
        return GeneradorDiagrama.generar_tabla_html(
            trans_simplificada,
            estados_nombres,
            [],
            es_afn=True
        )
    
    def obtener_ejemplos(self):
        return [
            ["SYN", "ACK", "RST"],
            ["SYN", "ACK", "ACK", "RST"],
            ["SYN", "ACK"]
        ]
    
    def obtener_diagrama_filename(self):
        return "ciberseguridad.png"


class LecturasIOT:
    def __init__(self):
        self.tabla_transiciones = TRANS_IOT
        self.estado_inicial = Estados_IOT.q0
        self.estados_aceptacion = {Estados_IOT.q3}
        self.estados = list(TRANS_IOT.keys())
        self.alfabeto = ["HDR", "TEMP", "HUM", "CRC"]
    
    def ejecutar(self, cadena_lista):
        resultado = _procesar_afn_iot(
            self.tabla_transiciones,
            self.estado_inicial,
            self.estados_aceptacion,
            cadena_lista
        )
        return {
            "valida": resultado,
            "estado_final": "aceptado" if resultado else "rechazado"
        }
    
    def obtener_tabla_html(self):
        trans_simplificada = {}
        for estado in TRANS_IOT:
            trans_simplificada[estado.name] = {}
            for simbolo, destinos in TRANS_IOT[estado].items():
                trans_simplificada[estado.name][simbolo] = [d.name for d in destinos]
        
        estados_nombres = [e.name for e in self.estados]
        return GeneradorDiagrama.generar_tabla_html(
            trans_simplificada,
            estados_nombres,
            [],
            es_afn=True
        )
    
    def obtener_ejemplos(self):
        return [
            ["HDR", "TEMP", "HUM", "CRC"],
            ["HDR", "TEMP", "TEMP", "HUM", "CRC"],
            ["HDR", "CRC"]
        ]
    
    def obtener_diagrama_filename(self):
        return "iot.png"


class NotacionCientifica:
    def __init__(self):
        self.ejemplos_validos = ["1e10", "1e0", "-123e5"]
        self.ejemplos_invalidos = ["123", "-123.45", "1e10.5"]
    
    def ejecutar(self, cadena):
        return {
            "valida": _es_valido(cadena),
            "estado_final": "aceptado" if _es_valido(cadena) else "rechazado"
        }
    
    def obtener_tabla_html(self):
        html = '<table border="1" cellpadding="8" cellspacing="0" class="tabla-transiciones">'
        html += '<tr><th>Estado</th><th>Digito 1-9</th><th>Digito 0-9</th><th>. (Punto)</th><th>e/E</th><th>+/-</th></tr>'
        html += '<tr><td style="background-color: #87CEEB; font-weight: bold;">q0</td><td>q2</td><td>-</td><td>-</td><td>-</td><td>q1</td></tr>'
        html += '<tr><td style="background-color: #87CEEB; font-weight: bold;">q1</td><td>q2</td><td>-</td><td>-</td><td>-</td><td>-</td></tr>'
        html += '<tr><td style="background-color: #87CEEB; font-weight: bold;">q2</td><td>q4</td><td>q4</td><td>q3</td><td>q5</td><td>-</td></tr>'
        html += '<tr><td style="background-color: #87CEEB; font-weight: bold;">q3</td><td>q4</td><td>q4</td><td>-</td><td>-</td><td>-</td></tr>'
        html += '<tr><td style="background-color: #87CEEB; font-weight: bold;">q4</td><td>q4</td><td>q4</td><td>-</td><td>q5</td><td>-</td></tr>'
        html += '<tr><td style="background-color: #87CEEB; font-weight: bold;">q5</td><td>q7</td><td>q7</td><td>-</td><td>-</td><td>q6</td></tr>'
        html += '<tr><td style="background-color: #87CEEB; font-weight: bold;">q6</td><td>q7</td><td>q7</td><td>-</td><td>-</td><td>-</td></tr>'
        html += '<tr><td style="background-color: #90EE90; font-weight: bold;">q7</td><td>q7</td><td>q7</td><td>-</td><td>-</td><td>-</td></tr>'
        html += '</table>'
        return html
    
    def obtener_ejemplos(self):
        return {
            "validos": ["1e10", "-123e5", "3.14e-2"],
            "invalidos": ["123", "-123.45", ".5"]
        }
    
    def obtener_diagrama_filename(self):
        return "notacion.png"


class TransaccionBancaria:
    def __init__(self):
        self.transiciones = TRANS_TRANSACCION
        self.estado_inicial = INICIAL_TRANSACCION
        self.estados_finales = FINALES_TRANSACCION
        self.estados = list(self.transiciones.keys())
    
    def ejecutar(self, eventos):
        return _validar_transaccion(eventos)
    
    def obtener_tabla_html(self):
        return GeneradorDiagrama.generar_tabla_html(
            self.transiciones,
            self.estados,
            self.estados_finales
        )
    
    def obtener_diagrama_filename(self):
        return "transaccion.png"
    
    def obtener_ejemplos(self):
        return [
            ["Autorizar", "Capturar", "Liquidar", "Completar"],
            ["Autorizar", "Capturar", "Liquidar"],
            ["Autorizar", "Cancelar"]
        ]


class ECommerce:
    def __init__(self):
        self.transiciones = TRANS_ECOMMERCE
        self.estado_inicial = INICIAL_ECOMMERCE
        self.estados_finales = FINALES_ECOMMERCE
        self.estados = list(self.transiciones.keys())
    
    def ejecutar(self, tokens):
        return _simular_afd(tokens)
    
    def obtener_tabla_html(self):
        return GeneradorDiagrama.generar_tabla_html(
            self.transiciones,
            self.estados,
            self.estados_finales
        )
    
    def obtener_diagrama_filename(self):
        return "ecommerce.png"
    
    def obtener_ejemplos(self):
        return [
            ["HOME", "SEARCH", "CART"],
            ["HOME", "SEARCH", "SEARCH", "CART"],
            ["HOME", "CART"]
        ]


cerradura = CerraduraInteligente()
ciberseguridad = Ciberseguridad()
lecturas_iot = LecturasIOT()
notacion = NotacionCientifica()
transaccion = TransaccionBancaria()
e_commerce = ECommerce()


@app.route('/')
def inicio():
    return render_template('inicio.html')


@app.route('/diagramas/<filename>')
def serve_diagram(filename):
    return send_from_directory('diagrams', filename)


@app.route('/cerradura')
def formulario_cerradura():
    return render_template('cerradura.html', 
                         tabla=cerradura.obtener_tabla_html(),
                         diagrama_filename=cerradura.obtener_diagrama_filename(),
                         ejemplos=cerradura.obtener_ejemplos())


@app.route('/cerradura/procesar', methods=['POST'])
def procesar_cerradura():
    datos = request.get_json()
    cadena = datos.get('cadena', '')
    
    resultado = cerradura.ejecutar(cadena)
    return jsonify({
        'resultado': resultado['valida'],
        'estado_final': resultado['estado_final'],
        'recorrido': resultado['recorrido']
    })


@app.route('/ciberseguridad')
def formulario_cibersuridad():
    return render_template('ciberseguridad.html',
                         tabla=ciberseguridad.obtener_tabla_html(),
                         diagrama_filename=ciberseguridad.obtener_diagrama_filename(),
                         ejemplos=ciberseguridad.obtener_ejemplos())


@app.route('/ciberseguridad/procesar', methods=['POST'])
def procesar_ciberseguridad():
    datos = request.get_json()
    cadena = datos.get('cadena', [])
    
    resultado = ciberseguridad.ejecutar(cadena)
    return jsonify({
        'resultado': resultado['valida'],
        'estado_final': resultado['estado_final']
    })


@app.route('/lecturas-iot')
def formulario_iot():
    return render_template('iot.html',
                         tabla=lecturas_iot.obtener_tabla_html(),
                         diagrama_filename=lecturas_iot.obtener_diagrama_filename(),
                         ejemplos=lecturas_iot.obtener_ejemplos())


@app.route('/lecturas-iot/procesar', methods=['POST'])
def procesar_iot():
    datos = request.get_json()
    cadena = datos.get('cadena', [])
    
    resultado = lecturas_iot.ejecutar(cadena)
    return jsonify({
        'resultado': resultado['valida'],
        'estado_final': resultado['estado_final']
    })


@app.route('/notacion')
def formulario_notacion():
    ejemplos = notacion.obtener_ejemplos()
    return render_template('notacion.html',
                         tabla=notacion.obtener_tabla_html(),
                         diagrama_filename=notacion.obtener_diagrama_filename(),
                         ejemplos_validos=ejemplos['validos'],
                         ejemplos_invalidos=ejemplos['invalidos'])


@app.route('/notacion/procesar', methods=['POST'])
def procesar_notacion():
    datos = request.get_json()
    cadena = datos.get('cadena', '')
    
    resultado = notacion.ejecutar(cadena)
    return jsonify({
        'resultado': resultado['valida'],
        'estado_final': resultado['estado_final']
    })


@app.route('/transaccion')
def formulario_transaccion():
    return render_template('transaccion.html',
                         tabla=transaccion.obtener_tabla_html(),
                         diagrama_filename=transaccion.obtener_diagrama_filename(),
                         ejemplos=transaccion.obtener_ejemplos())


@app.route('/transaccion/procesar', methods=['POST'])
def procesar_transaccion():
    datos = request.get_json()
    eventos = datos.get('eventos', [])
    
    resultado = transaccion.ejecutar(eventos)
    return jsonify({
        'resultado': resultado['valida'],
        'estado_final': resultado['estado_final'],
        'recorrido': resultado['recorrido']
    })


@app.route('/e-commerce')
def formulario_ecommerce():
    return render_template('ecommerce.html',
                         tabla=e_commerce.obtener_tabla_html(),
                         diagrama_filename=e_commerce.obtener_diagrama_filename(),
                         ejemplos=e_commerce.obtener_ejemplos())


@app.route('/e-commerce/procesar', methods=['POST'])
def procesar_ecommerce():
    datos = request.get_json()
    secuencia = datos.get('secuencia', [])
    
    resultado = e_commerce.ejecutar(secuencia)
    return jsonify({
        'resultado': resultado['aceptada'],
        'estado_final': resultado['estado_final'],
        'recorrido': resultado['recorrido'],
        'mensaje': resultado.get('mensaje', '')
    })


if __name__ == '__main__':
    app.run(debug=True)