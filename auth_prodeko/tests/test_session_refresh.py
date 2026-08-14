"""The periodic recheck of an SSO session against Keycloak.

Tests here opt out of the ``sso_session_on_force_login`` fixture with the
``no_sso_session`` marker, because a session without a fresh id token is
exactly the state under test.
"""

from urllib.parse import parse_qs, urlparse

import pytest
from django.conf import settings
from django.contrib import auth
from django.urls import reverse


@pytest.fixture(autouse=True)
def _db(db):
    pass


def _query_of(response):
    return parse_qs(urlparse(response["Location"]).query)


@pytest.mark.no_sso_session
def test_a_stale_session_is_rechecked_at_the_provider(client, user):
    client.force_login(user)

    response = client.get("/en/")

    assert response.status_code == 302
    assert response["Location"].startswith(settings.OIDC_OP_AUTHORIZATION_ENDPOINT)
    assert _query_of(response)["prompt"] == ["none"]


@pytest.mark.no_sso_session
def test_the_sso_endpoints_are_exempt_from_the_recheck(client, user):
    """Rechecking the login flow itself would bounce it back on itself."""
    client.force_login(user)

    response = client.get(reverse("oidc_authentication_init"))

    assert response.status_code == 302
    assert "prompt" not in _query_of(response)


@pytest.mark.no_sso_session
def test_a_refused_recheck_signs_the_user_out(client, user, monkeypatch):
    """A membership role revoked in Keycloak must end the session.

    Keycloak answers the prompt=none handoff with a code, the backend
    refuses the claims behind it, and without a sign-out the session
    stays authenticated with an expired id token, so the next request
    is bounced to Keycloak again, and the one after that, forever.
    """
    client.force_login(user)
    state = _query_of(client.get("/en/"))["state"][0]

    monkeypatch.setattr(auth, "authenticate", lambda **kwargs: None)
    response = client.get(f"/oidc/callback/?code=refused&state={state}")

    assert response.status_code == 302
    assert "_auth_user_id" not in client.session
    assert "prompt=none" not in client.get("/en/").get("Location", "")


def test_a_stray_callback_leaves_a_live_session_alone(logged_in_client):
    """Logging out is a POST; a link to the callback url is not one."""
    response = logged_in_client.get("/oidc/callback/")

    assert response.status_code == 302
    assert "_auth_user_id" in logged_in_client.session


@pytest.mark.no_sso_session
def test_an_ended_keycloak_session_sends_the_member_to_sign_in_again(client, user):
    """Keycloak's SSO session ends long before Django's thirty days.

    The silent handoff then comes back with error=login_required, which
    says nothing about the member's right to be here: their sign-in
    simply expired. Sending them to the failure page would accuse them
    of having no membership.
    """
    client.force_login(user)
    state = _query_of(client.get("/en/"))["state"][0]

    response = client.get(f"/oidc/callback/?error=login_required&state={state}")

    assert response.status_code == 302
    assert response["Location"] != reverse("auth_prodeko:login_failed")
    assert response["Location"].startswith(reverse("oidc_authentication_init"))
    assert "_auth_user_id" not in client.session


@pytest.mark.no_sso_session
def test_an_expired_sign_in_keeps_the_page_the_member_asked_for(client, user):
    wanted = "/en/blog/"
    client.force_login(user)
    state = _query_of(client.get(wanted))["state"][0]

    response = client.get(f"/oidc/callback/?error=login_required&state={state}")

    assert _query_of(response)["next"] == [wanted]


@pytest.mark.no_sso_session
def test_an_expired_sign_in_reaches_a_keycloak_login_form(client, user):
    """The expiry path must not bounce between two of our own urls: the
    hop it makes has to end at a form the member can actually use."""
    client.force_login(user)
    state = _query_of(client.get("/en/"))["state"][0]

    response = client.get(f"/oidc/callback/?error=login_required&state={state}")
    login = client.get(response["Location"])

    assert login.status_code == 302
    assert login["Location"].startswith(settings.OIDC_OP_AUTHORIZATION_ENDPOINT)
    assert "prompt" not in _query_of(login)


@pytest.mark.no_sso_session
def test_refused_claims_still_reach_the_explanation(client, user, monkeypatch):
    """A revoked role, a taken address, the break-glass account: these
    are refusals of the identity, and the failure page exists for them.
    """
    client.force_login(user)
    state = _query_of(client.get("/en/"))["state"][0]

    monkeypatch.setattr(auth, "authenticate", lambda **kwargs: None)
    response = client.get(f"/oidc/callback/?code=refused&state={state}")

    assert response["Location"] == reverse("auth_prodeko:login_failed")
    assert "_auth_user_id" not in client.session
