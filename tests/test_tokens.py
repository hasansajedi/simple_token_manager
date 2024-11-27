import pytest
from datetime import timedelta
from django.utils.timezone import now

pytestmark = pytest.mark.integration


@pytest.fixture
def default_valid_data(default_valid_resource):
    return {
        "apikey": default_valid_resource.api_key,
        "identifier": default_valid_resource.identifier,
    }


def test_generate_token(generate_token_api, default_valid_data):
    response = generate_token_api(action="post", data=default_valid_data)
    assert response.status_code == 201
    assert response.json()["token"]
    assert not response.json()["is_revoked"]


def test_cannot_generate_token_with_invalid_api_key(generate_token_api):
    data = {"apikey": "invalid_api_key", "identifier": "test"}

    response = generate_token_api(action="post", data=data)
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid parameters."


def test_revoke_token(revoke_token_api, default_valid_token, default_valid_data):
    response = revoke_token_api(action="post", data=default_valid_data)
    print(response.json())
    assert response.status_code == 200
    default_valid_token.refresh_from_db()
    assert default_valid_token.is_revoked


def test_validate_valid_token(validate_token_api, default_valid_token):
    response = validate_token_api(
        action="post", data={"token": default_valid_token.token}
    )
    assert response.status_code == 200
    assert response.data["valid"]


def test_validate_expired_token(validate_token_api, default_valid_token):
    default_valid_token.expires_at = now() - timedelta(days=1)
    default_valid_token.save()

    response = validate_token_api(
        action="post", data={"token": "invalid_token"}
    )
    assert response.status_code == 401
    assert response.data["detail"] == "Invalid request."
