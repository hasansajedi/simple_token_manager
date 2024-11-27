import pytest
from typing import Dict

from django.urls import reverse
from rest_framework.test import APIClient

from tests.factories import ResourceFactory, TokenFactory


@pytest.fixture
def api_client(db):
    return APIClient()


@pytest.fixture
def default_valid_resource():
    return ResourceFactory()


@pytest.fixture
def default_valid_token(default_valid_resource):
    return TokenFactory(resource=default_valid_resource)


@pytest.fixture
def default_client_with_token_fixture(db, default_valid_token) -> APIClient:
    client = APIClient(enforce_csrf_checks=False)
    client.credentials(
        HTTP_AUTHORIZATION=f"Authorization: Bearer {default_valid_token.token}"
    )
    return client


@pytest.fixture
def generate_token_api(api_client):
    def _send_request(action: str, data: Dict = None):
        base_url = "token_auth:generate_token"

        if action == "post":
            url = reverse(base_url)
            return api_client.post(url, data=data, format="json")
        else:
            raise Exception("Action not supported")

    return _send_request


@pytest.fixture
def revoke_token_api(default_client_with_token_fixture):
    def _send_request(action: str, data: Dict = None):
        base_url = "token_auth:revoke_token"

        if action == "post":
            url = reverse(base_url)
            return default_client_with_token_fixture.post(
                url,
                data=data,
                format="json",
            )
        else:
            raise Exception("Action not supported")

    return _send_request


@pytest.fixture
def validate_token_api(default_client_with_token_fixture):
    def _send_request(action: str, data: Dict = None):
        base_url = "token_auth:validate_token"

        if action == "post":
            url = reverse(base_url)
            return default_client_with_token_fixture.post(
                url,
                data=data,
                format="json",
            )
        else:
            raise Exception("Action not supported")

    return _send_request
