
import pytest
import requests

from fastapi.testclient import TestClient
from backend.app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


# ==========================================
# TEST 1: SUCCESSFUL EXTERNAL API RESPONSE
# ==========================================

def test_external_api_success(client, monkeypatch):

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "resultCount": 1,
                "results": [
                    {
                        "trackId": 123,
                        "trackName": "Avatar",
                        "artistName": "James Horner",
                        "collectionName": "Avatar Soundtrack",
                        "primaryGenreName": "Soundtrack"
                    }
                ]
            }

    def mock_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        "backend.app.services.external_api.requests.get",
        mock_get
    )

    response = client.get(
        "/api/external/search",
        params={
            "query": "Avatar",
            "media": "movie",
            "limit": 10
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["result_count"] == 1
    assert data["results"][0]["title"] == "Avatar"


# ==========================================
# TEST 2: EMPTY SEARCH QUERY
# ==========================================

def test_external_api_empty_query(client):

    response = client.get(
        "/api/external/search",
        params={
            "query": "  ",
            "media": "movie"
        }
    )

    assert response.status_code == 400


# ==========================================
# TEST 3: INVALID MEDIA TYPE
# ==========================================

def test_external_api_invalid_media(client):

    response = client.get(
        "/api/external/search",
        params={
            "query": "Avatar",
            "media": "invalid"
        }
    )

    assert response.status_code == 422


# ==========================================
# TEST 4: INVALID RESULT LIMIT
# ==========================================

@pytest.mark.parametrize("limit", [0, 51])
def test_external_api_invalid_limit(client, limit):

    response = client.get(
        "/api/external/search",
        params={
            "query": "Avatar",
            "media": "movie",
            "limit": limit
        }
    )

    assert response.status_code == 422


# ==========================================
# TEST 5: API TIMEOUT
# ==========================================

def test_external_api_timeout(client, monkeypatch):

    def mock_timeout(*args, **kwargs):
        raise requests.Timeout("Connection timed out.")

    monkeypatch.setattr(
        "backend.app.services.external_api.requests.get",
        mock_timeout
    )

    response = client.get(
        "/api/external/search",
        params={
            "query": "Avatar",
            "media": "movie"
        }
    )

    assert response.status_code == 504

    assert response.json()["detail"] == (
        "External API request timed out."
    )


# ==========================================
# TEST 6: CONNECTION FAILURE
# ==========================================

def test_external_api_connection_error(client, monkeypatch):

    def mock_connection_error(*args, **kwargs):
        raise requests.ConnectionError("Connection failed.")

    monkeypatch.setattr(
        "backend.app.services.external_api.requests.get",
        mock_connection_error
    )

    response = client.get(
        "/api/external/search",
        params={
            "query": "Avatar",
            "media": "movie"
        }
    )

    assert response.status_code == 502

    assert response.json()["detail"] == (
        "Unable to connect to the external API."
    )


# ==========================================
# TEST 7: INVALID JSON RESPONSE
# ==========================================

def test_external_api_invalid_json(client, monkeypatch):

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            raise ValueError("Invalid JSON")

    def mock_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        "backend.app.services.external_api.requests.get",
        mock_get
    )

    response = client.get(
        "/api/external/search",
        params={
            "query": "Avatar",
            "media": "movie"
        }
    )

    assert response.status_code == 502

    assert response.json()["detail"] == (
        "External API returned invalid JSON."
    )
