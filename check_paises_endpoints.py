import requests

r = requests.get('http://127.0.0.1:8000/endpoints')
print(f"Status: {r.status_code}")

if r.status_code == 200:
    endpoints = r.json()
    print("🔍 Buscando endpoints de países...")
    
    paises_endpoints = [ep for ep in endpoints if 'paises' in ep['path'].lower()]
    
    if paises_endpoints:
        print("✅ Endpoints de países encontrados:")
        for ep in paises_endpoints:
            print(f"  - {ep['path']} ({ep['methods']})")
    else:
        print("❌ No se encontraron endpoints de países")
        print("📋 Todos los endpoints disponibles:")
        for ep in endpoints[:10]:  # Mostrar solo los primeros 10
            print(f"  - {ep['path']} ({ep['methods']})")
else:
    print("❌ Error al obtener endpoints")