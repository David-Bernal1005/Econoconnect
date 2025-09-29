# tests/test_noticias.py
import pytest
from fastapi.testclient import TestClient
import sys
import os
# Añadir la carpeta 'backend' al sys.path para que los imports funcionen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.main import app

client = TestClient(app)

NOTICIAS_PATHS = [
    "/api/v1/noticias",
    "/api/v1/news",
    "/noticias",
    "/news",
]

def try_paths(method, candidates, json=None, headers=None):
    """Intenta rutas en candidates y devuelve (ruta, response) del primer endpoint no 404/405."""
    for p in candidates:
        if method == "post":
            resp = client.post(p, json=json, headers=headers or {})
        else:
            resp = client.get(p, headers=headers or {})
        if resp.status_code not in (404, 405):
            return p, resp
    return None, None

def test_get_noticias_devuelve_lista():
    get_path, resp = try_paths("get", NOTICIAS_PATHS)
    assert get_path is not None, "No se encontró endpoint GET de noticias entre los candidatos."
    assert resp.status_code == 200, f"GET {get_path} debe devolver 200, devolvió {resp.status_code}"
    assert isinstance(resp.json(), list), "GET /noticias debe devolver una lista (aunque esté vacía)."

def test_post_noticia_sin_asumir_auth():
    """
    Prueba simple para POST /noticias.
    Acepta varios comportamientos comunes:
      - Si el endpoint requiere autenticación: 401 o 403.
      - Si el payload es inválido: 422.
      - Si el endpoint permite crear directamente: 200 o 201.
    """
    payload = {
        "titulo": "Prueba rápida",
        "resumen": "Contenido de prueba.",
        "enlace": "http://ejemplo.com",
        "fecha_publicacion": "2025-09-25T00:00:00",
        "categoria": "General",
        "usuario": "testuser"
    }
    post_path, resp = try_paths("post", NOTICIAS_PATHS, json=payload)
    assert post_path is not None, "No se encontró endpoint POST de noticias entre los candidatos."

    assert resp.status_code in (200, 201, 401, 403, 422), (
        f"POST {post_path} devolvió un código inesperado: {resp.status_code} - {resp.text}"
    )

    # Si la creación fue exitosa (200/201), comprobar que aparece en el GET
    if resp.status_code in (200, 201):
        get_path, rget = try_paths("get", NOTICIAS_PATHS)
        assert get_path is not None and rget.status_code == 200
        items = rget.json()
        assert any(
            isinstance(n, dict) and (
                n.get("titulo") == payload["titulo"] or
                payload["resumen"] in (n.get("resumen") or "")
            )
            for n in items
        ), "La noticia creada no apareció en el listado tras POST exitoso."

def test_get_noticias_usuario():
    # Crear noticia para usuario específico
    payload = {
        "titulo": "Noticia de usuario",
        "resumen": "Solo para test usuario.",
        "enlace": "http://usuario.com",
        "fecha_publicacion": "2025-09-25T00:00:00",
        "categoria": "Test",
        "usuario": "usuario_test"
    }
    post_path, resp = try_paths("post", NOTICIAS_PATHS, json=payload)
    assert resp.status_code in (200, 201)
    # Obtener noticias del usuario
    get_path, resp = try_paths("get", [f"/api/v1/noticias/usuario/{payload['usuario']}"])
    assert get_path is not None and resp.status_code == 200
    items = resp.json()
    assert any(n.get("titulo") == payload["titulo"] for n in items)

def test_editar_noticia():
    # Crear noticia
    payload = {
        "titulo": "Editar noticia",
        "resumen": "Original.",
        "enlace": "http://editar.com",
        "fecha_publicacion": "2025-09-25T00:00:00",
        "categoria": "Test",
        "usuario": "edituser"
    }
    post_path, resp = try_paths("post", NOTICIAS_PATHS, json=payload)
    assert resp.status_code in (200, 201)
    noticia_id = resp.json().get("Id_Noticia")
    # Editar noticia
    edit_payload = {"titulo": "Editada", "resumen": "Modificada."}
    put_path = f"/api/v1/noticias/{noticia_id}"
    resp = client.put(put_path, json=edit_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["titulo"] == "Editada"
    assert data["resumen"] == "Modificada."

def test_inactivar_noticia():
    # Crear noticia
    payload = {
        "titulo": "Inactivar noticia",
        "resumen": "Activa.",
        "enlace": "http://inactivar.com",
        "fecha_publicacion": "2025-09-25T00:00:00",
        "categoria": "Test",
        "usuario": "inactuser"
    }
    post_path, resp = try_paths("post", NOTICIAS_PATHS, json=payload)
    assert resp.status_code in (200, 201)
    noticia_id = resp.json().get("Id_Noticia")
    # Inactivar noticia
    patch_path = f"/api/v1/noticias/{noticia_id}/inactivar"
    resp = client.patch(patch_path)
    assert resp.status_code == 200
    data = resp.json()
    assert data["activa"] == 0

def test_editar_noticia_inexistente():
    # Editar noticia que no existe
    put_path = "/api/v1/noticias/999999"
    edit_payload = {"titulo": "No existe"}
    resp = client.put(put_path, json=edit_payload)
    assert resp.status_code == 404

def test_inactivar_noticia_inexistente():
    # Inactivar noticia que no existe
    patch_path = "/api/v1/noticias/999999/inactivar"
    resp = client.patch(patch_path)
    assert resp.status_code == 404

def test_post_noticia_invalida():
    # Payload inválido (falta campo obligatorio)
    payload = {"titulo": "Sin resumen"}
    post_path, resp = try_paths("post", NOTICIAS_PATHS, json=payload)
    assert resp.status_code == 422
