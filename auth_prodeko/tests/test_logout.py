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
