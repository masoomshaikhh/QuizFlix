
# ==========================================================
# QUIZFLIX - HTTP CRUD METHOD TESTING
# Lab 8: API Testing
# Methods: GET, POST, PUT, PATCH, DELETE
# Database: Temporary SQLite
# ==========================================================

import pytest

from types import SimpleNamespace

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from backend.app.database import Base, get_db
from backend.app.services.dependencies import get_admin_user


# ==========================================================
# TEMPORARY DATABASE
# ==========================================================

@pytest.fixture
def db_session():

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


# ==========================================================
# TEST CLIENT
# ==========================================================

@pytest.fixture
def client(db_session):

    def override_get_db():
        yield db_session

    def override_admin():
        return SimpleNamespace(role="admin")

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_admin_user] = override_admin

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# ==========================================================
# TEST 1: GET CATEGORIES
# ==========================================================

def test_get_categories(client):

    response = client.get("/api/categories/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    print("GET Status:", response.status_code)


# ==========================================================
# TEST 2: POST CATEGORY
# ==========================================================

def test_post_category(client):

    response = client.post(
        "/api/categories/",
        json={
            "category_name": "Lab8 Test Category",
            "description": "Temporary category for CRUD testing."
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["category_name"] == "Lab8 Test Category"

    print("POST Status:", response.status_code)


# ==========================================================
# TEST 3: PUT CATEGORY
# ==========================================================

def test_put_category(client):

    create_response = client.post(
        "/api/categories/",
        json={
            "category_name": "Original Test Category",
            "description": "Original description."
        }
    )

    category_id = create_response.json()["category_id"]

    response = client.put(
        f"/api/categories/{category_id}",
        json={
            "category_name": "Updated Test Category",
            "description": "Updated description."
        }
    )

    assert response.status_code == 200

    assert response.json()["category_name"] == (
        "Updated Test Category"
    )

    print("PUT Status:", response.status_code)


# ==========================================================
# TEST 4: DELETE CATEGORY
# ==========================================================

def test_delete_category(client):

    create_response = client.post(
        "/api/categories/",
        json={
            "category_name": "Delete Test Category",
            "description": "Temporary deletion test."
        }
    )

    category_id = create_response.json()["category_id"]

    response = client.delete(
        f"/api/categories/{category_id}"
    )

    assert response.status_code == 200

    assert response.json()["message"] == (
        "Category deleted successfully."
    )

    print("DELETE Status:", response.status_code)


# ==========================================================
# TEST 5: PATCH METHOD NOT IMPLEMENTED
# ==========================================================

def test_patch_not_supported(client):

    create_response = client.post(
        "/api/categories/",
        json={
            "category_name": "Patch Test Category",
            "description": "Testing unsupported PATCH method."
        }
    )

    category_id = create_response.json()["category_id"]

    response = client.patch(
        f"/api/categories/{category_id}",
        json={
            "description": "Updated description."
        }
    )

    assert response.status_code == 405

    print("PATCH Status:", response.status_code)
    print("PATCH is not implemented in the current API.")
