import uuid

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from tests.conftest import DataManagement


def generate_uuid():
    return uuid.uuid4().hex[:6]


def test_create_user(client_test: TestClient, data_management: DataManagement):
    payload = {
        "first_name": "string",
        "last_name": "string",
        "email": f"user{generate_uuid()}@example.com",
        "password": "string",
    }
    response = client_test.post(
        "/v1/users",
        json=payload,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == status.HTTP_201_CREATED
    _data = response.json()["data"]
    _data["password"] = payload["password"]
    data_management.add("user", _data)


def test_user_login(client_test: TestClient, data_management: DataManagement):
    payload = {
        "email": data_management.get("user")["email"],
        "password": data_management.get("user")["password"],
    }
    response = client_test.post(
        "/v1/auth/users/login",
        json=payload,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == status.HTTP_200_OK
    data_management.add("token", response.json()["data"])

    _data = {
        "access_token": response.json()["data"]["access_token"],
        "refresh_token": response.json()["data"]["refresh_token"],
    }

    data_management.add("user_token", _data)


def test_invalid_user_login(client_test: TestClient, data_management: DataManagement):
    payload = {
        "email": data_management.get("user")["email"],
        "password": "invalid_password",
    }
    response = client_test.post(
        "/v1/auth/users/login",
        json=payload,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["status"] == status.HTTP_401_UNAUTHORIZED


def test_get_all_users(client_test: TestClient, data_management: DataManagement):
    response = client_test.get(
        "/v1/users",
        headers={
            "Authorization": f"{data_management.get('user_token')['access_token']}"
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == status.HTTP_200_OK
    data_management.add("users", response.json()["data"])



def test_get_user_profile(client_test: TestClient, data_management: DataManagement):
    response = client_test.get(
        f"/v1/users/me",
        headers={
            "Authorization": f"{data_management.get('user_token')['access_token']}"
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == status.HTTP_200_OK
    data_management.add("user_profile", response.json()["data"])

def test_get_user_by_uuid(client_test: TestClient, data_management: DataManagement):
    response = client_test.get(
        f"/v1/users/{data_management.get('user_profile')['uuid']}",
        headers={
            "Authorization": f"{data_management.get('user_token')['access_token']}"
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == status.HTTP_200_OK
    data_management.add("user_by_uuid", response.json()["data"])

def test_get_user_by_uuid_not_found(client_test: TestClient, data_management: DataManagement):
    response = client_test.get(
        f"/v1/users/{uuid.uuid4()}",
        headers={
            "Authorization": f"{data_management.get('user_token')['access_token']}"
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["status"] == status.HTTP_404_NOT_FOUND

def test_update_user(client_test: TestClient, data_management: DataManagement):
    payload = {
        "first_name": "Update test",
    }
    response = client_test.patch(
        f"/v1/users",
        headers={
            "Authorization": f"{data_management.get('user_token')['access_token']}"
        },
        json=payload,
    )
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["status"] == status.HTTP_202_ACCEPTED