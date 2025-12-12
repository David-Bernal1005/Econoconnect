"""
Pruebas de usabilidad: flujo completo de interacción básica.

Instrucciones:
1. Instalar:
   pip install locust
2. Ejecutar:
   locust -f tests_locust/test_usabilidad.py
3. UI:
   http://localhost:8089

Flujo:
1. GET /
2. GET /items
3. POST /items (json={"nombre": "Flujo", "precio": 50})
4. GET /items (verificar que se recibe lista tras creación)

Observaciones:
- Esta prueba ayuda a detectar interrupciones en el journey básico del usuario.
- Ajustar claves JSON según API real si difiere.
"""
from locust import HttpUser, task, between

class UsabilidadUser(HttpUser):
    wait_time = between(2, 4)

    @task
    def flujo_basico(self):
        # Paso 1: Home
        with self.client.get("/", name="Flujo GET /", catch_response=True) as home:
            if home.status_code != 200:
                home.failure(f"Home status inesperado {home.status_code}")

        # Paso 2: Listado inicial
        with self.client.get("/items", name="Flujo GET /items inicial", catch_response=True) as listado:
            if listado.status_code != 200:
                listado.failure(f"Listado inicial status {listado.status_code}")

        # Paso 3: Creación
        payload = {"nombre": "Flujo", "precio": 50}
        with self.client.post("/items", json=payload, name="Flujo POST /items", catch_response=True) as creado:
            if creado.status_code not in (200, 201):
                creado.failure(f"Creación item status {creado.status_code}")

        # Paso 4: Listado posterior
        with self.client.get("/items", name="Flujo GET /items final", catch_response=True) as listado2:
            if listado2.status_code != 200:
                listado2.failure(f"Listado final status {listado2.status_code}")
