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

class TestRemoveStatusEndpoint:
    """Tests for DELETE /removeStatus endpoint"""

    def test_remove_status_no_version(self, no_version_state):
        no_version_state.delete("/removeStatus")
        response = no_version_state.get("/status")
        assert json.loads(response.data)["version"] is None

    def test_remove_status_from_version_1(self, version_1_state):
        version_1_state.delete("/removeStatus")
        response = version_1_state.get("/status")
        assert json.loads(response.data)["version"] is None

    def test_remove_status_from_version_2(self, version_2_state):
        version_2_state.delete("/removeStatus")
        response = version_2_state.get("/status")
        assert json.loads(response.data)["version"] is None


class TestRollbackStatusEndpoint:
    """Tests for POST /rollbackStatusVersion endpoint"""

    def test_rollback_status_no_version(self, no_version_state):
        response = no_version_state.post("/rollbackStatusVersion")
        assert response.status_code == HTTPStatus.BAD_REQUEST

        response = no_version_state.get("/status")
        assert json.loads(response.data)["version"] is None

    def test_rollback_status_from_version_1(self, version_1_state):
        response = version_1_state.post("/rollbackStatusVersion")
        assert response.status_code == HTTPStatus.BAD_REQUEST

        response = version_1_state.get("/status")
        assert json.loads(response.data)["version"] == "1"

    def test_rollback_status_from_version_2(self, version_2_state):
        response = version_2_state.post("/rollbackStatusVersion")
        assert response.status_code == HTTPStatus.OK

        response = version_2_state.get("/status")
        assert json.loads(response.data)["version"] == "1"

    def test_rollback_to_specific_version(self, version_2_state):
        response = version_2_state.post(
            "/rollbackStatusVersion", json={"version": "1.1"}
        )
        assert response.status_code == HTTPStatus.OK
        response = version_2_state.get("/status")
        assert json.loads(response.data)["version"] == "1.1"

    def test_rollback_to_invalid_version(self, version_2_state):
        response = version_2_state.post("/rollbackStatusVersion", json={"version": "5"})
        assert response.status_code == HTTPStatus.BAD_REQUEST

        response = version_2_state.get("/status")
        assert json.loads(response.data)["version"] == "2"


class TestStateTransitions:
    """Tests for complex state transitions"""

    def test_full_version_lifecycle(self, no_version_state):
        # Start with no version
        response = no_version_state.get("/status")
        assert json.loads(response.data)["version"] is None

        # Set initial version
        no_version_state.post("/setStatus")
        response = no_version_state.get("/status")
        assert json.loads(response.data)["version"] == "1"

        # Update to minor version
        no_version_state.patch("/updateStatus")
        response = no_version_state.get("/status")
        assert json.loads(response.data)["version"] == "1.1"

        # Update to another minor version
        no_version_state.patch("/updateStatus")
        response = no_version_state.get("/status")
        assert json.loads(response.data)["version"] == "1.2"

        # Rewrite to major version
        no_version_state.put("/rewriteStatus")
        response = no_version_state.get("/status")
        assert json.loads(response.data)["version"] == "2"

        # Rollback to previous major
        no_version_state.post("/rollbackStatusVersion")
        response = no_version_state.get("/status")
        assert json.loads(response.data)["version"] == "1"

        # Remove status
        no_version_state.delete("/removeStatus")
        response = no_version_state.get("/status")
        assert json.loads(response.data)["version"] is None

    def test_multiple_minor_updates(self, version_1_state):
        expected_versions = ["1.1", "1.2", "1.3"]
        for expected_version in expected_versions:
            response = version_1_state.patch("/updateStatus")
            assert response.status_code == HTTPStatus.OK

            response = version_1_state.get("/status")
            assert json.loads(response.data)["version"] == expected_version


class TestEdgeCases:
    """Tests for edge cases and error conditions"""

    def test_invalid_rollback_version_format(self, version_2_state):
        response = version_2_state.post(
            "/rollbackStatusVersion", json={"version": "invalid"}
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

        response = version_2_state.get("/status")
        assert json.loads(response.data)["version"] == "2"

    def test_rollback_with_empty_body(self, version_2_state):
        response = version_2_state.post("/rollbackStatusVersion", json={})
        assert response.status_code == HTTPStatus.OK

        response = version_2_state.get("/status")
        assert json.loads(response.data)["version"] == "1"

    def test_consecutive_major_version_updates(self, version_1_state):
        expected_versions = ["2", "3", "4"]
        for expected_version in expected_versions:
            response = version_1_state.put("/rewriteStatus")
            assert response.status_code == HTTPStatus.OK

            response = version_1_state.get("/status")
            assert json.loads(response.data)["version"] == expected_version

    def test_multiple_operations_sequence(self, clean_state, client):
        # Set initial version
        response = client.post("/setStatus")
        assert response.status_code == HTTPStatus.CREATED

        response = client.get("/status")
        assert json.loads(response.data)["version"] == "1"

        # Multiple minor updates
        for expected_minor in range(1, 4):
            client.patch("/updateStatus")
            response = client.get("/status")
            assert json.loads(response.data)["version"] == f"1.{expected_minor}"

        # Major update
        client.put("/rewriteStatus")
        response = client.get("/status")
        assert json.loads(response.data)["version"] == "2"

        # More minor updates on new major version
        client.patch("/updateStatus")
        response = client.get("/status")
        assert json.loads(response.data)["version"] == "2.1"

        # Rollback to specific version
        client.post("/rollbackStatusVersion", json={"version": "1.2"})
        response = client.get("/status")
        assert json.loads(response.data)["version"] == "1.2"

    def test_invalid_method_for_get_status(self, client):
        response = client.post("/status")
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_invalid_method_for_set_status(self, client):
        response = client.put("/setStatus")
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_invalid_method_for_update_status(self, client):
        response = client.delete("/updateStatus")
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_invalid_method_for_rewrite_status(self, client):
        response = client.get("/rewriteStatus")
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_invalid_method_for_remove_status(self, client):
        response = client.post("/removeStatus")
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_invalid_method_for_rollback_status(self, client):
        response = client.get("/rollbackStatusVersion")
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
