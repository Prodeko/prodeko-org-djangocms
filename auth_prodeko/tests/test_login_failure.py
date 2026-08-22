"""The page a refused Keycloak login lands on."""

import pytest
from django.urls import reverse


@pytest.fixture(autouse=True)
def _db(db):
    pass


def test_refused_callback_lands_on_the_explanation(client):
    """A callback the library refuses must not drop the visitor on the
    front page, anonymous and unaddressed."""
    response = client.get("/oidc/callback/?code=irrelevant&state=unknown")
    assert response.status_code == 302
    assert response["Location"] != "/"
    assert response["Location"] == reverse("auth_prodeko:login_failed")


def test_page_renders_for_an_anonymous_visitor(client):
    response = client.get(reverse("auth_prodeko:login_failed"))
    assert response.status_code == 200
    assert b"membership.prodeko.org" in response.content


def test_page_offers_a_way_out_of_the_keycloak_session(client, settings):
    """Without it the login link signs the visitor back into the same
    refusal, with no way to try another account."""
    settings.OIDC_OP_LOGOUT_ENDPOINT = (
        "https://id.prodeko.org/realms/membership-registry"
        "/protocol/openid-connect/logout"
    )
    response = client.get(reverse("auth_prodeko:login_failed"))
    assert settings.OIDC_OP_LOGOUT_ENDPOINT.encode() in response.content
