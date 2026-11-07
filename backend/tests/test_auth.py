
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from backend.app.database import Base, get_db
from backend.app.models.user import User
from backend.app.services.auth import verify_password


# ==========================================
# TEST DATABASE SETUP
# ==========================================

@pytest.fixture
def db_session():

    # Create an isolated in-memory SQLite database.
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


# ==========================================
# FASTAPI TEST CLIENT
# ==========================================

@pytest.fixture
def client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# ==========================================
# HELPER: REGISTER TEST USER
# ==========================================

def register_test_user(
    client,
    username="test_player",
    email="testplayer@example.com",
    password="QuizFlix@123"
):

    return client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )


# ==========================================
# TEST 1: SUCCESSFUL REGISTRATION
# ==========================================

def test_user_registration_success(client, db_session):

    response = register_test_user(client)

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "test_player"
    assert data["email"] == "testplayer@example.com"
    assert data["role"] == "user"

    # Password must never be returned by the API.
    assert "password_hash" not in data
    assert "password" not in data

    # Verify that the user is saved in the database.
    user = db_session.query(User).filter(
        User.email == "testplayer@example.com"
    ).first()

    assert user is not None
    assert user.password_hash != "QuizFlix@123"
    assert verify_password(
        "QuizFlix@123",
        user.password_hash
    )


# ==========================================
# TEST 2: DUPLICATE EMAIL REGISTRATION
# ==========================================

def test_duplicate_email_registration(client):

    register_test_user(client)

    response = register_test_user(
        client,
        username="another_player",
        email="testplayer@example.com"
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered."


# ==========================================
# TEST 3: DUPLICATE USERNAME REGISTRATION
# ==========================================

def test_duplicate_username_registration(client):

    register_test_user(client)

    response = register_test_user(
        client,
        username="test_player",
        email="another@example.com"
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Username already taken."


# ==========================================
# TEST 4: PASSWORD EXCEEDING 72 BYTES
# ==========================================

def test_password_exceeding_72_bytes(client):

    # 40 characters, but 80 UTF-8 bytes.
    long_password = "é" * 40

    response = register_test_user(
        client,
        username="long_password_user",
        email="longpassword@example.com",
        password=long_password
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Password must not exceed 72 bytes."
    )


# ==========================================
# TEST 5: SUCCESSFUL LOGIN
# ==========================================

def test_user_login_success(client):

    register_test_user(client)

    response = client.post(
        "/api/auth/login",
        json={
            "email": "testplayer@example.com",
            "password": "QuizFlix@123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert len(data["access_token"]) > 0
    assert data["token_type"] == "bearer"


# ==========================================
# TEST 6: LOGIN WITH INCORRECT PASSWORD
# ==========================================

def test_login_with_wrong_password(client):

    register_test_user(client)

    response = client.post(
        "/api/auth/login",
        json={
            "email": "testplayer@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401

    assert response.json()["detail"] == (
        "Invalid email or password."
    )


# ==========================================
# TEST 7: LOGIN WITH NON-EXISTENT EMAIL
# ==========================================

def test_login_with_unknown_email(client):

    response = client.post(
        "/api/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "QuizFlix@123"
        }
    )

    assert response.status_code == 401

    assert response.json()["detail"] == (
        "Invalid email or password."
    )
