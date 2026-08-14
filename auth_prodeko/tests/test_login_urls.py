import pytest
from django.urls import reverse


@pytest.fixture(autouse=True)
def _db(db):
    pass


def test_login_url_redirects_to_keycloak_init(client):
    response = client.get("/en/login/")
    assert response.status_code == 302
    assert response["Location"] == reverse("oidc_authentication_init")


def test_login_url_preserves_next(client):
    response = client.get("/en/login/?next=/en/kokouspoytakirjat/")
    assert response.status_code == 302
    assert response["Location"] == (
        reverse("oidc_authentication_init") + "?next=%2Fen%2Fkokouspoytakirjat%2F"
    )


def test_callback_url_has_no_language_prefix():
    """It must match the redirect URI registered in Keycloak verbatim."""
    assert reverse("oidc_authentication_callback") == "/oidc/callback/"


def test_password_reset_urls_are_gone(client):
    assert client.get("/en/password_reset/").status_code == 404
