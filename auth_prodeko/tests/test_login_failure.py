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


# The membership registry link in the page body, as distinct from the
# one the site footer puts on every page.
JOIN_LINK = b'href="https://membership.prodeko.org/"'


def test_page_renders_for_an_anonymous_visitor(client):
    response = client.get(reverse("auth_prodeko:login_failed"))
    assert response.status_code == 200
    assert JOIN_LINK in response.content


def test_page_offers_a_way_out_of_the_keycloak_session(client, settings):
    """Without it the login link signs the visitor back into the same
    refusal, with no way to try another account."""
    settings.OIDC_OP_LOGOUT_ENDPOINT = (
        "https://id.prodeko.org/realms/membership-registry"
        "/protocol/openid-connect/logout"
    )
    response = client.get(reverse("auth_prodeko:login_failed"))
    assert settings.OIDC_OP_LOGOUT_ENDPOINT.encode() in response.content


# --- the page explains the reason the refusal left behind -----------------


def _stash(client, reason):
    session = client.session
    session["keycloak_refusal"] = reason
    session.save()


def test_a_conflict_names_an_administrator_not_the_membership(client):
    """Telling someone whose address is tangled with another account to
    go renew their membership sends them, and whoever helps them, down
    the wrong road entirely."""
    _stash(client, "account_conflict")

    response = client.get(reverse("auth_prodeko:login_failed"))

    assert b"mediakeisari@prodeko.org" in response.content
    assert JOIN_LINK not in response.content


def test_a_provider_fault_accuses_nobody(client):
    """When Keycloak is down or misconfigured, the visitor has nothing
    to act on: no membership to renew, no administrator to write to."""
    _stash(client, "provider_unavailable")

    response = client.get(reverse("auth_prodeko:login_failed"))

    assert JOIN_LINK not in response.content
    assert b"mediakeisari@prodeko.org" not in response.content


def test_the_reason_is_shown_once(client):
    """A stale reason must not explain some later, unrelated failure."""
    _stash(client, "account_conflict")
    client.get(reverse("auth_prodeko:login_failed"))

    response = client.get(reverse("auth_prodeko:login_failed"))

    assert JOIN_LINK in response.content


def test_a_reason_nobody_recognises_falls_back_to_the_default(client):
    _stash(client, "not-a-reason")

    response = client.get(reverse("auth_prodeko:login_failed"))

    assert JOIN_LINK in response.content


@pytest.mark.parametrize("reason", ["account_conflict", "provider_unavailable"])
def test_every_variant_offers_the_way_out_of_the_keycloak_session(
    client, settings, reason
):
    settings.OIDC_OP_LOGOUT_ENDPOINT = (
        "https://id.prodeko.org/realms/membership-registry"
        "/protocol/openid-connect/logout"
    )
    _stash(client, reason)

    response = client.get(reverse("auth_prodeko:login_failed"))

    assert settings.OIDC_OP_LOGOUT_ENDPOINT.encode() in response.content
