"""
Pruebas básicas de seguridad con Locust.

Instrucciones:
1. Instalar:
   pip install locust
2. Ejecutar:
   locust -f tests_locust/test_seguridad.py
3. UI:
   http://localhost:8089

Pruebas:
- Acceso no autenticado a /admin (espera 401 o 403).
- Intento de SQL Injection en /buscar?query=' OR '1'='1'.

Nota: Ajustar rutas según implementación real.
"""
from locust import HttpUser, task, between

class SeguridadUser(HttpUser):
    wait_time = between(1, 2)

    @task(2)
    def acceso_admin_sin_auth(self):
        """Intento de acceso a zona restringida /admin sin credenciales."""
        with self.client.get("/admin", catch_response=True) as resp:
            if resp.status_code not in (401, 403):
                # Si devuelve 200 es una falla potencial
                resp.failure(f"/admin accesible sin auth: status {resp.status_code}")

    @task(1)
    def sql_injection_busqueda(self):
        """Intento de SQL Injection básico en /buscar."""
        payload = "%27 OR %271%27=%271"  # URL encoded ' OR '1'='1
        with self.client.get(
            f"/buscar?query={payload}", name="SQLi /buscar", catch_response=True
        ) as resp:
            if resp.status_code >= 500:
                resp.failure("Posible vulnerabilidad (error 5xx ante SQLi)")
            # Opcional: inspección de contenido que podría indicar fuga de datos
