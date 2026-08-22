from urllib.parse import parse_qs, urlparse

import pytest
from django.conf import settings
from django.test import RequestFactory, override_settings

from auth_prodeko.oidc.logout import provider_logout


@pytest.fixture
def request_with_session(rf: RequestFactory):
    request = rf.get("/")
    request.session = {}
    return request


def test_logout_url_points_at_the_provider(request_with_session):
    url = provider_logout(request_with_session)
    assert url.startswith(settings.OIDC_OP_LOGOUT_ENDPOINT)


def test_logout_url_asks_to_come_back_here(request_with_session):
    query = parse_qs(urlparse(provider_logout(request_with_session)).query)
    assert query["post_logout_redirect_uri"] == ["http://testserver/"]


def test_id_token_is_passed_as_a_hint_when_stored(request_with_session):
    request_with_session.session["oidc_id_token"] = "a.b.c"
    query = parse_qs(urlparse(provider_logout(request_with_session)).query)
    assert query["id_token_hint"] == ["a.b.c"]


@override_settings(OIDC_RP_CLIENT_ID="prodekoorg")
def test_missing_id_token_is_tolerated(request_with_session):
    """Keycloak refuses a post_logout_redirect_uri backed by neither a
    hint nor a client id, and the break-glass account never has a hint."""
    query = parse_qs(urlparse(provider_logout(request_with_session)).query)
    assert "id_token_hint" not in query
    assert query["client_id"] == ["prodekoorg"]


KEYCLOAK_LOGOUT = (
    "https://id.prodeko.org/realms/membership-registry/protocol/openid-connect/logout"
)


@pytest.fixture
def signed_in(logged_in_client, settings):
    """A session carrying the id token a Keycloak login leaves behind."""
    settings.OIDC_OP_LOGOUT_ENDPOINT = KEYCLOAK_LOGOUT
    session = logged_in_client.session
    session["oidc_id_token"] = "a.b.c"
    session.save()
    return logged_in_client


def test_toolbar_logout_keeps_the_browser_on_this_site(signed_in):
    """The django-cms toolbar posts here over XHR and cannot follow a
    redirect to Keycloak: no CORS headers, so the call fails and the
    editor is shown an error banner over a logout that worked."""
    response = signed_in.post(
        "/en/admin/logout/", headers={"x-requested-with": "XMLHttpRequest"}
    )
    assert response.status_code == 302
    assert urlparse(response["Location"]).netloc == ""


def test_toolbar_logout_still_ends_the_django_session(signed_in):
    signed_in.post("/en/admin/logout/", headers={"x-requested-with": "XMLHttpRequest"})
    assert "_auth_user_id" not in signed_in.session


def test_a_normal_logout_still_ends_the_keycloak_session(signed_in):
    response = signed_in.post("/en/admin/logout/")
    assert response.status_code == 302
    assert response["Location"].startswith(KEYCLOAK_LOGOUT)
    query = parse_qs(urlparse(response["Location"]).query)
    assert query["id_token_hint"] == ["a.b.c"]
    assert "_auth_user_id" not in signed_in.session


def test_a_get_is_still_refused(signed_in):
    """ALLOW_LOGOUT_GET_METHOD is off, so only POST logs anyone out."""
    assert signed_in.get("/en/admin/logout/").status_code == 405
