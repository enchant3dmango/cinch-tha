from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_product():
    response = client.get("/products/1")
    # OK or Not Found (if no data yet)
    assert response.status_code in [200, 404]
