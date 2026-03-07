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


def test_shipment_list_endpoint_returns_expected_shape() -> None:
    response = client.get("/shipments")

    assert response.status_code == 200
    payload = response.json()
    assert payload["module"] == "shipments"
    assert len(payload["items"]) >= 1
    assert payload["items"][0]["record_no"].startswith("SHP-")


def test_shipment_detail_endpoint_returns_expected_shape() -> None:
    response = client.get("/shipments/shipment-001")

    assert response.status_code == 200
    payload = response.json()
    assert payload["module"] == "shipments"
    assert payload["item"]["id"] == "shipment-001"


def test_repair_list_endpoint_returns_expected_shape() -> None:
    response = client.get("/repairs")

    assert response.status_code == 200
    payload = response.json()
    assert payload["module"] == "repairs"
    assert payload["items"][0]["record_no"].startswith("RPR-")


def test_return_detail_endpoint_returns_expected_shape() -> None:
    response = client.get("/returns/return-001")

    assert response.status_code == 200
    payload = response.json()
    assert payload["module"] == "returns"
    assert payload["item"]["id"] == "return-001"