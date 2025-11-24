"""
Pruebas de rendimiento (carga, estrés, spike) con Locust.

Instrucciones:
1. Instalar:
   pip install locust
2. Ejecutar:
   locust -f tests_locust/test_rendimiento.py
3. UI:
   http://localhost:8089

Tipos de prueba implementados como tareas:
- Carga (load): Solicitudes regulares a /items.
- Estrés (stress): Rafaga moderada interna para ver degradación.
- Spike: Pico súbito de muchas solicitudes consecutivas.

Métricas observables en UI Locust:
- RPS (Requests per second)
- Tiempo de respuesta (Average, Median, Percentiles)
- Failures (conteo y ratio)
"""
from locust import HttpUser, task, between
import random

class RendimientoUser(HttpUser):
    wait_time = between(0.5, 1)

    @task(3)
    def carga_items(self):
        """Carga normal: una petición a /items."""
        resp = self.client.get("/items", name="LOAD /items")
        if resp.status_code != 200:
            resp.failure(f"Status inesperado LOAD /items: {resp.status_code}")

    @task(2)
    def estres_items(self):
        """Estrés: varias peticiones secuenciales para elevar presión."""
        for i in range(5):
            resp = self.client.get("/items", name="STRESS /items")
            if resp.status_code != 200:
                resp.failure(f"Status inesperado STRESS /items: {resp.status_code}")

    @task(1)
    def spike_items(self):
        """Spike: pico súbito (ej. 10-15 peticiones rápidas)."""
        burst = random.randint(10, 15)
        for i in range(burst):
            resp = self.client.get("/items", name="SPIKE /items")
            if resp.status_code != 200:
                resp.failure(f"Status inesperado SPIKE /items: {resp.status_code}")
