"""
Pruebas de funcionalidad con Locust.

Instrucciones:
1. Instalar Locust:
   pip install locust
2. Ejecutar solo este archivo:
   locust -f tests_locust/test_funcionalidad.py
3. Ejecutar toda la carpeta (todos los archivos):
   locust -f tests_locust
4. Abrir UI (si headless = false):
   http://localhost:8089

Descripción de las pruebas:
- GET /               Verifica que el endpoint raíz responde 200.
- GET /items          Verifica listado (espera 200 y JSON válido).
- POST /items         Crea un item (espera 201/200 y campos devueltos).

Nota: Ajustar claves JSON según la API real si difieren.
"""
from locust import HttpUser, task, between

class FuncionalidadUser(HttpUser):
    # Espera entre 1 y 3 segundos entre tareas simulando usuario humano
    wait_time = between(1, 3)

    @task(2)
    def get_root(self):
        """Verifica que / responde correctamente."""
        resp = self.client.get("/")
        if resp.status_code != 200:
            resp.failure(f"GET / status inesperado: {resp.status_code}")

    @task(2)
    def get_items(self):
        """Verifica listado de items."""
        resp = self.client.get("/items")
        if resp.status_code != 200:
            resp.failure(f"GET /items status inesperado: {resp.status_code}")
        else:
            # Intento de parseo para garantizar JSON
            try:
                data = resp.json()
                if not isinstance(data, (list, dict)):
                    resp.failure("Respuesta /items no es lista ni dict")
            except Exception as ex:
                resp.failure(f"JSON inválido /items: {ex}")

    @task(1)
    def post_item(self):
        """Crea un item de prueba."""
        payload = {"nombre": "Item de prueba", "precio": 100}
        resp = self.client.post("/items", json=payload)
        if resp.status_code not in (200, 201):
            resp.failure(f"POST /items status inesperado: {resp.status_code}")
        else:
            try:
                data = resp.json()
                # Validaciones básicas opcionales
                if "nombre" not in data:
                    resp.failure("Respuesta POST /items sin campo 'nombre'")
            except Exception as ex:
                resp.failure(f"JSON inválido POST /items: {ex}")
