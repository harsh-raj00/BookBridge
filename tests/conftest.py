"""
Test fixtures and configuration.
Sets up an in-memory SQLite database and test client for isolated testing.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app


# In-memory SQLite for tests — fast, isolated, no cleanup needed
TEST_DATABASE_URL = "sqlite:///./test_bookbridge.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the DB dependency for tests
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create tables before each test and drop after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    """Test client for making HTTP requests."""
    return TestClient(app)


@pytest.fixture
def test_user(client):
    """Create and return a registered test user."""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPassword123",
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    return {**user_data, **response.json()}


@pytest.fixture
def auth_headers(client, test_user):
    """Get authorization headers with a valid JWT token."""
    response = client.post("/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"],
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
