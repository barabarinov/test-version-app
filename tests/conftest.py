import os
from http import HTTPStatus

import pytest
import requests

from .client import StatusApiClient


@pytest.fixture(scope="session")
def api_url():
    return os.getenv("SERVICE_HOST", "http://localhost:5000")


@pytest.fixture(scope="session")
def session():
    session = requests.Session()

    yield session

    session.close()


@pytest.fixture
def api_client(session, api_url):
    return StatusApiClient(session, api_url)


@pytest.fixture
def clean_state(api_client):
    """Clean version state before each test"""
    status_code = api_client.remove_status()
    assert status_code == HTTPStatus.OK

    status_code, version = api_client.get_status()
    assert version is None


@pytest.fixture
def no_version_state(clean_state, api_client) -> StatusApiClient:
    """Setup: No version set"""
    return api_client


@pytest.fixture
def version_1_state(clean_state, api_client) -> StatusApiClient:
    """Setup: Version 1 set"""
    api_client.set_status()
    status_code, version = api_client.get_status()
    assert version == "1"
    return api_client


@pytest.fixture
def version_1_1_state(version_1_state, api_client) -> StatusApiClient:
    """Setup: Version 1.1 set"""
    api_client.update_status()
    status_code, version = api_client.get_status()
    assert version == "1.1"
    return api_client


@pytest.fixture
def version_2_state(version_1_1_state, api_client) -> StatusApiClient:
    """Setup: Version 2 set"""
    api_client.rewrite_status()
    status_code, version = api_client.get_status()
    assert version == "2"
    return api_client
