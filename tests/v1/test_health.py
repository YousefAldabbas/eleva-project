from fastapi import status
from fastapi.testclient import TestClient


def test_health(client_test: TestClient):
    response = client_test.get("/v1/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == status.HTTP_200_OK
