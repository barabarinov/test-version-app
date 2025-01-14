import json
from http import HTTPStatus

import pytest

from app import app


@pytest.fixture
def client():
    """Create a test client"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def clean_state(client):
    """Clean version state before each test"""
    response = client.delete("/removeStatus")
    assert response.status_code == HTTPStatus.OK
    assert json.loads(client.get("/status").data)["version"] is None


# State setup fixtures
@pytest.fixture
def no_version_state(clean_state, client):
    """Setup: No version set"""
    return client


@pytest.fixture
def version_1_state(clean_state, client):
    """Setup: Version 1 set"""
    client.post("/setStatus")
    assert json.loads(client.get("/status").data)["version"] == "1"
    return client


@pytest.fixture
def version_1_1_state(version_1_state, client):
    """Setup: Version 1.1 set"""
    client.patch("/updateStatus")
    assert json.loads(client.get("/status").data)["version"] == "1.1"
    return client


@pytest.fixture
def version_2_state(version_1_1_state, client):
    """Setup: Version 2 set"""
    client.put("/rewriteStatus")
    assert json.loads(client.get("/status").data)["version"] == "2"
    return client


class TestStatusEndpoint:
    """Tests for GET /status endpoint"""

    def test_get_status_no_version(self, no_version_state):
        response = no_version_state.get("/status")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert json.loads(response.data)["version"] is None

    def test_get_status_version_1(self, version_1_state):
        response = version_1_state.get("/status")
        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.data)["version"] == "1"

    def test_get_status_version_1_1(self, version_1_1_state):
        response = version_1_1_state.get("/status")
        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.data)["version"] == "1.1"

    def test_get_status_version_2(self, version_2_state):
        response = version_2_state.get("/status")
        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.data)["version"] == "2"


class TestSetStatusEndpoint:
    """Tests for POST /setStatus endpoint"""

    def test_set_status_when_no_version(self, no_version_state):
        response = no_version_state.post("/setStatus")
        assert response.status_code == HTTPStatus.CREATED

        response = no_version_state.get("/status")
        assert json.loads(response.data)["version"] == "1"

    def test_set_status_when_version_exists(self, version_1_state):
        response = version_1_state.post("/setStatus")
        assert response.status_code == HTTPStatus.BAD_REQUEST

        response = version_1_state.get("/status")
        assert json.loads(response.data)["version"] == "1"


class TestUpdateStatusEndpoint:
    """Tests for PATCH /updateStatus endpoint"""

    def test_update_status_no_version(self, no_version_state):
        no_version_state.patch("/updateStatus")
        response = no_version_state.get("/status")
        assert json.loads(response.data)["version"] is None

    def test_update_status_from_version_1(self, version_1_state):
        version_1_state.patch("/updateStatus")
        response = version_1_state.get("/status")
        assert json.loads(response.data)["version"] == "1.1"

    def test_update_status_from_version_1_1(self, version_1_1_state):
        response = version_1_1_state.patch("/updateStatus")
        assert response.status_code == HTTPStatus.OK

        response = version_1_1_state.get("/status")
        assert json.loads(response.data)["version"] == "1.2"

    def test_update_status_from_version_2(self, version_2_state):
        response = version_2_state.patch("/updateStatus")
        assert response.status_code == HTTPStatus.OK

        response = version_2_state.get("/status")
        assert json.loads(response.data)["version"] == "2.1"


class TestRewriteStatusEndpoint:
    """Tests for PUT /rewriteStatus endpoint"""

    def test_rewrite_status_no_version(self, no_version_state):
        response = no_version_state.put("/rewriteStatus")
        assert response.status_code == HTTPStatus.BAD_REQUEST

        response = no_version_state.get("/status")
        assert json.loads(response.data)["version"] is None

    def test_rewrite_status_from_version_1(self, version_1_state):
        response = version_1_state.put("/rewriteStatus")
        assert response.status_code == HTTPStatus.OK

        response = version_1_state.get("/status")
        assert json.loads(response.data)["version"] == "2"

    def test_rewrite_status_from_version_1_1(self, version_1_1_state):
        response = version_1_1_state.put("/rewriteStatus")
        assert response.status_code == HTTPStatus.OK

        response = version_1_1_state.get("/status")
        assert json.loads(response.data)["version"] == "2"
