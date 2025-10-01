import requests

print("🧪 Probando funcionalidad de países...")

try:
    # Probar endpoint de países
    response = requests.get("http://127.0.0.1:8000/api/v1/paises")
    if response.status_code == 200:
        paises = response.json()
        print(f"✅ Endpoint de países funciona! {len(paises)} países encontrados")
        
        # Mostrar algunos países
        for pais in paises[:5]:
            print(f"  - {pais['nombre']}")
    else:
        print(f"❌ Error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error de conexión: {e}")