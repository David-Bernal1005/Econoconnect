import pytest
from fastapi.testclient import TestClient
from app.models.datografica import DatoGrafica


def test_get_graficas_uses_db_data_and_external_api(client: TestClient, test_db):
    """Verifica que /api/v1/graficas responde 200 y devuelve estructura válida.

    No fuerza un número fijo de elementos porque la vista también intenta
    consultar APIs externas y rellenar el año actual.
    """
    # Crear un dato histórico mínimo
    dato = DatoGrafica(
        id_grafica=1,
        anio=2020,
        cop_usd=1000.0,
        cop_eur=2000.0,
    )
    test_db.add(dato)
    test_db.commit()

    response = client.get("/api/v1/graficas")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    first = data[0]
    assert "year" in first
    assert "cop_usd" in first
    assert "cop_eur" in first