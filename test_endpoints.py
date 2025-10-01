import requests

rutas_a_probar = [
    "/api/v1/paises",
    "/paises",
    "/api/paises",
    "/api/v1/paises/",
    "/api/v1/countries"
]

print("🧪 Probando diferentes rutas para países...")

for ruta in rutas_a_probar:
    try:
        r = requests.get(f"http://127.0.0.1:8000{ruta}")
        print(f"  {ruta}: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"    ✅ ¡Funciona! {len(data)} países encontrados")
            break
    except Exception as e:
        print(f"  {ruta}: Error - {e}")

# Probar también rutas de usuario
print("\n🧪 Probando endpoints de usuario...")
rutas_usuario = [
    "/api/v1/users/me",
    "/api/v1/users/",
]

for ruta in rutas_usuario:
    try:
        r = requests.get(f"http://127.0.0.1:8000{ruta}")
        print(f"  {ruta}: {r.status_code}")
    except Exception as e:
        print(f"  {ruta}: Error - {e}")