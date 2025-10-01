import requests

print("🔍 Verificando endpoints disponibles...")

try:
    # Verificar si el servidor está funcionando
    response = requests.get("http://127.0.0.1:8000/docs")
    if response.status_code == 200:
        print("✅ Servidor funcionando")
    
    # Intentar diferentes rutas
    rutas = [
        "/api/v1/paises",
        "/paises",
        "/api/paises",
        "/api/v1/endpoints"
    ]
    
    for ruta in rutas:
        try:
            resp = requests.get(f"http://127.0.0.1:8000{ruta}")
            print(f"  {ruta}: {resp.status_code}")
        except:
            print(f"  {ruta}: Error")
            
except Exception as e:
    print(f"❌ Error: {e}")