"""Tests for authentication endpoints."""


class TestRegister:
    """Tests for POST /auth/register"""

    def test_register_success(self, client):
        response = client.post("/auth/register", json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "SecurePass123",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert "password" not in data  # Password should never be returned

    def test_register_duplicate_email(self, client, test_user):
        response = client.post("/auth/register", json={
            "name": "Another User",
            "email": test_user["email"],  # Same email
            "password": "AnotherPass123",
        })
        assert response.status_code == 409
        assert "already registered" in response.json()["detail"]

    def test_register_invalid_email(self, client):
        response = client.post("/auth/register", json={
            "name": "Bad Email",
            "email": "not-an-email",
            "password": "Pass123",
        })
        assert response.status_code == 422  # Validation error


class TestLogin:
    """Tests for POST /auth/login"""

    def test_login_success(self, client, test_user):
        response = client.post("/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"],
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == test_user["email"]

    def test_login_wrong_password(self, client, test_user):
        response = client.post("/auth/login", json={
            "email": test_user["email"],
            "password": "WrongPassword",
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post("/auth/login", json={
            "email": "nobody@example.com",
            "password": "NoPass",
        })
        assert response.status_code == 401
