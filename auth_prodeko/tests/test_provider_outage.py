"""What a member sees when Keycloak stops answering mid-login.

The stubs here replace ``requests`` itself, so no test in this file can
reach id.prodeko.org even if the timeout setting were removed.
"""

import logging
from urllib.parse import parse_qs, urlparse

import pytest
import requests
from django.urls import reverse
from mozilla_django_oidc import auth as oidc_auth


@pytest.fixture(autouse=True)
def _db(db):
    pass


def _timing_out(*args, **kwargs):
    raise requests.exceptions.ReadTimeout("stubbed: id.prodeko.org did not answer")


@pytest.fixture
def keycloak_hangs(monkeypatch):
    """Every outbound call the login flow makes times out."""
    monkeypatch.setattr(oidc_auth.requests, "post", _timing_out)
    monkeypatch.setattr(oidc_auth.requests, "get", _timing_out)


def _start_login(client):
    """Seeds the session state a callback needs, and returns it."""
    response = client.get(reverse("oidc_authentication_init"))
    return parse_qs(urlparse(response["Location"]).query)["state"][0]


def test_a_timed_out_callback_refuses_instead_of_erroring(client, keycloak_hangs):
    """A 500 here would mail the admins on every click during an outage
    and show the member a stack-trace page they cannot act on."""
    state = _start_login(client)

    response = client.get(f"/oidc/callback/?code=irrelevant&state={state}")

    assert response.status_code == 302
    assert response["Location"] == reverse("auth_prodeko:login_failed")


@pytest.mark.parametrize(
    "failure",
    [
        requests.exceptions.ConnectionError("stubbed: connection refused"),
        requests.exceptions.HTTPError("stubbed: 503 from the token endpoint"),
    ],
    ids=["refused", "server error"],
)
def test_any_failed_call_to_keycloak_refuses_rather_than_erroring(
    client, monkeypatch, failure
):
    """A timeout is only one of the ways a call to Keycloak fails. A
    refused connection and an error status from the token endpoint reach
    the same code by a different exception, and a 500 apiece is not an
    answer the member can act on."""

    def _failing(*args, **kwargs):
        raise failure

    monkeypatch.setattr(oidc_auth.requests, "post", _failing)
    monkeypatch.setattr(oidc_auth.requests, "get", _failing)
    state = _start_login(client)

    response = client.get(f"/oidc/callback/?code=irrelevant&state={state}")

    assert response.status_code == 302
    assert response["Location"] == reverse("auth_prodeko:login_failed")


def test_a_timed_out_callback_is_logged(client, keycloak_hangs, caplog):
    with caplog.at_level(logging.WARNING, logger="auth_prodeko.oidc.callback"):
        state = _start_login(client)
        client.get(f"/oidc/callback/?code=irrelevant&state={state}")

    assert any(
        record.levelno == logging.WARNING and "Keycloak" in record.getMessage()
        for record in caplog.records
    )


# --- an outage and a misconfiguration are not the same event --------------
#
# Production mails the admins on ERROR and only logs WARNING, so the
# level chosen here decides whether anyone finds out. An outage clears on
# its own and mailing on every click through it is noise; a client secret
# that no longer matches the realm never clears, and every login fails
# until someone is told.


def _levels_for(client, monkeypatch, caplog, failure):
    def _failing(*args, **kwargs):
        raise failure

    monkeypatch.setattr(oidc_auth.requests, "post", _failing)
    monkeypatch.setattr(oidc_auth.requests, "get", _failing)

    with caplog.at_level(logging.WARNING, logger="auth_prodeko.oidc.callback"):
        state = _start_login(client)
        client.get(f"/oidc/callback/?code=irrelevant&state={state}")

    return {
        record.levelno
        for record in caplog.records
        if record.name == "auth_prodeko.oidc.callback"
    }


@pytest.mark.parametrize(
    "failure",
    [
        requests.exceptions.ConnectionError("stubbed: connection refused"),
        requests.exceptions.ReadTimeout("stubbed: id.prodeko.org did not answer"),
    ],
    ids=["refused", "timed out"],
)
def test_an_unreachable_keycloak_does_not_mail_the_admins(
    client, monkeypatch, caplog, failure
):
    """The site is fine and the outage is someone else's to end. Mail on
    every click for as long as it lasts buries anything worth reading."""
    assert _levels_for(client, monkeypatch, caplog, failure) == {logging.WARNING}


def test_credentials_keycloak_rejects_do_mail_the_admins(client, monkeypatch, caplog):
    """A 401 from the token endpoint means the client secret here does
    not match the realm. Nobody but us can fix it, no member can report
    anything more useful than "login is broken", and every login fails
    until it is fixed."""
    failure = requests.exceptions.HTTPError("stubbed: 401 invalid_client")

    assert _levels_for(client, monkeypatch, caplog, failure) == {logging.ERROR}
