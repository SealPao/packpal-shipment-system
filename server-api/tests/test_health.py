from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_expected_shape() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "PackPal Shipment System API",
        "version": "0.1.0",
        "environment": "development",
    }


def test_shipment_placeholder_endpoint_returns_expected_shape() -> None:
    response = client.get("/shipments/placeholder")

    assert response.status_code == 200
    payload = response.json()
    assert payload["module"] == "shipments"
    assert payload["status"] == "placeholder"


def test_repair_placeholder_endpoint_returns_expected_shape() -> None:
    response = client.get("/repairs/placeholder")

    assert response.status_code == 200
    payload = response.json()
    assert payload["module"] == "repairs"
    assert payload["status"] == "placeholder"


def test_return_placeholder_endpoint_returns_expected_shape() -> None:
    response = client.get("/returns/placeholder")

    assert response.status_code == 200
    payload = response.json()
    assert payload["module"] == "returns"
    assert payload["status"] == "placeholder"