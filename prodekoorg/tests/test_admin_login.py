import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.fixture(autouse=True)
def _db(db):
    pass


def test_admin_login_offers_keycloak(client):
    response = client.get("/en/admin/login/")
    assert response.status_code == 200
    assert reverse("oidc_authentication_init").encode() in response.content


def test_admin_login_still_has_a_password_form(client):
    """It is the only way to use the break-glass account."""
    response = client.get("/en/admin/login/")
    assert b'name="password"' in response.content


def test_break_glass_account_can_still_sign_in(client, settings):
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = "rescue@prodeko.org"
    User.objects.create_superuser(
        email="rescue@prodeko.org", password="a-long-rescue-password"
    )
    assert client.login(
        username="rescue@prodeko.org", password="a-long-rescue-password"
    )


def test_admin_logout_goes_through_keycloak(client, settings):
    settings.OIDC_OP_LOGOUT_ENDPOINT = (
        "https://id.prodeko.org/realms/membership-registry"
        "/protocol/openid-connect/logout"
    )
    user = User.objects.create_superuser(email="root@prodeko.org", password=None)
    client.force_login(user)
    response = client.post("/en/admin/logout/")
    assert response.status_code == 302
    assert "id.prodeko.org" in response["Location"] or response["Location"] == "/"
