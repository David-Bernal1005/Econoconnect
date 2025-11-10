// Clase para manejar el foro
export class ForoManager {
    constructor(baseUrl = 'http://localhost:8000') {  // Ajusta esta URL según tu configuración
        this.baseUrl = baseUrl;
        this.token = localStorage.getItem('token');
    }

    // Crear un nuevo foro
    async crearForo(nombre, descripcion, idGrafica = null) {
        const response = await fetch(`${this.baseUrl}/foro`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre,
                descripcion,
                id_grafica: idGrafica
            })
        });
        return await response.json();
    }

    // Listar todos los foros
    async listarForos() {
        const response = await fetch(`${this.baseUrl}/foro`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return await response.json();
    }

    // Obtener un foro específico
    async obtenerForo(foroId) {
        const response = await fetch(`${this.baseUrl}/foro/${foroId}`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return await response.json();
    }

    // Obtener comentarios de un foro
    async obtenerComentarios(foroId) {
        const response = await fetch(`${this.baseUrl}/ws/foro/${foroId}/comentarios`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return await response.json();
    }

    // Conectar al WebSocket para comentarios en tiempo real
    conectarWebSocket(foroId, callbacks) {
        const ws = new WebSocket(`${this.baseUrl.replace('http', 'ws')}/ws/foro/${foroId}?token=${this.token}`);
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (callbacks.onNuevoComentario) {
                callbacks.onNuevoComentario(data);
            }
        };

        ws.onclose = () => {
            if (callbacks.onDesconexion) {
                callbacks.onDesconexion();
            }
        };

        return {
            enviarComentario: (contenido) => {
                ws.send(JSON.stringify({ contenido }));
            },
            cerrar: () => ws.close()
        };
    }
}