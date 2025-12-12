"""
Pruebas de compatibilidad (User-Agent) con Locust.

Instrucciones:
1. Instalar:
   pip install locust
2. Ejecutar:
   locust -f tests_locust/test_compatibilidad.py
3. UI:
   http://localhost:8089

Se simulan diferentes navegadores enviando encabezado User-Agent:
- Chrome
- Firefox
- Android

Cada tarea realiza GET / con un header distinto.
"""
from locust import HttpUser, task, between

CHROME_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
FIREFOX_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0"
ANDROID_UA = "Mozilla/5.0 (Linux; Android 14; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"

class CompatibilidadUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def chrome_root(self):
        with self.client.get(
            "/",
            headers={"User-Agent": CHROME_UA},
            name="Chrome /",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Chrome / status: {resp.status_code}")

    @task(2)
    def firefox_root(self):
        with self.client.get(
            "/",
            headers={"User-Agent": FIREFOX_UA},
            name="Firefox /",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Firefox / status: {resp.status_code}")

    @task(1)
    def android_root(self):
        with self.client.get(
            "/",
            headers={"User-Agent": ANDROID_UA},
            name="Android /",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Android / status: {resp.status_code}")
