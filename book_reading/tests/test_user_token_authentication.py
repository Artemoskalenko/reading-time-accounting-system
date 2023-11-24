import pytest

from rest_framework.test import APIClient


@pytest.mark.django_db
def test_token_authentication():
    """

    """
    client = APIClient()

    response = client.get("/api/v1/user-statistics/")
    assert response.status_code == 401

    response = client.post("/auth/users/", {"username": "testusername", "password": "testpassword"})
    assert response.status_code == 201

    response = client.post("/auth/token/login/", {"username": "testusername", "password": "testpassword"})
    assert response.status_code == 200
    assert "auth_token" in response.data

    client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['auth_token']}")

    response = client.get("/api/v1/user-statistics/")
    assert response.status_code == 200
    assert response.data["Username"] == "testusername"



