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