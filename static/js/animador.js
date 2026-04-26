class AnimadorAutomata {
    constructor(cadena, recorrido) {
        this.cadena = Array.isArray(cadena) ? cadena : cadena.split('');
        this.recorrido = recorrido || [];
        this.pasoActual = 0;
        this.velocidad = 1000;
        this.reproduciendo = false;
        this.historialPasos = [];
    }

    obtenerPasoActual() {
        return {
            indice: this.pasoActual,
            simbolo: this.pasoActual > 0 ? this.cadena[this.pasoActual - 1] : null,
            estado: this.recorrido[this.pasoActual] || null
        };
    }

    siguientePaso() {
        if (this.pasoActual < this.cadena.length) {
            this.pasoActual++;
            return true;
        }
        return false;
    }

    pasoAnterior() {
        if (this.pasoActual > 0) {
            this.pasoActual--;
            return true;
        }
        return false;
    }

    reiniciar() {
        this.pasoActual = 0;
        this.reproduciendo = false;
    }

    establecerVelocidad(velocidad) {
        this.velocidad = 1000 / velocidad;
    }

    esFinalizadoAceptablemente() {
        return this.pasoActual === this.cadena.length;
    }

    obtenerRecorridoCompleto() {
        return this.recorrido.slice(0, this.pasoActual + 1);
    }
}

function inicializarAnimadores() {
    window.animadores = {};
}

function crearAnimador(id, cadena, recorrido) {
    window.animadores[id] = new AnimadorAutomata(cadena, recorrido);
    return window.animadores[id];
}

function obtenerAnimador(id) {
    return window.animadores[id];
}

function actualizarVisualizacionAnimacion(contenedor, animador, tipo_entrada = 'cadena') {
    const paso = animador.obtenerPasoActual();
    
    const cadenaHTML = contenedor.querySelector('.cadena-visual');
    if (cadenaHTML) {
        cadenaHTML.innerHTML = '';
        for (let i = 0; i < animador.cadena.length; i++) {
            const span = document.createElement('span');
            span.className = 'simbolo';
            span.textContent = animador.cadena[i];
            
            if (i === animador.pasoActual - 1) {
                span.classList.add('procesado');
            } else if (i === animador.pasoActual) {
                span.classList.add('actual');
            }
            
            cadenaHTML.appendChild(span);
        }
    }
    
    const infoEstado = contenedor.querySelector('.estado-info');
    if (infoEstado) {
        const contenido = infoEstado.querySelector('.estado-info-contenido');
        if (contenido) {
            contenido.innerHTML = `
                Paso: ${animador.pasoActual}/${animador.cadena.length}<br>
                Estado actual: <strong>${paso.estado || 'N/A'}</strong><br>
                Símbolo: <strong>${paso.simbolo || '-'}</strong><br>
                Recorrido: <strong>${animador.obtenerRecorridoCompleto().join(' → ')}</strong>
            `;
        }
    }
}

function reproducirAutomata(contenedor, animador, callbackActualizacion) {
    animador.reproduciendo = true;
    
    const reproducir = () => {
        if (!animador.reproduciendo) {
            return;
        }
        
        callbackActualizacion(animador);
        
        if (animador.siguientePaso()) {
            setTimeout(reproducir, animador.velocidad);
        } else {
            animador.reproduciendo = false;
        }
    };
    
    reproducir();
}

document.addEventListener('DOMContentLoaded', function() {
    inicializarAnimadores();
});
