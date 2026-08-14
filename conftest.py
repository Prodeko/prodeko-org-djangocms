import time
from pathlib import Path

import polib
import pytest
from cms.utils.permissions import set_current_user
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(autouse=True)
def reset_cms_current_user():
    """django-cms's CurrentUserMiddleware stores the request user in a
    module-level threading.local that nothing clears after the response,
    so a user from one test leaks into cms's post_save signal handlers
    in later tests and inserts rows referencing rolled-back PKs."""
    set_current_user(None)
    yield


@pytest.fixture(autouse=True)
def sso_session_on_force_login(request, monkeypatch):
    """force_login() mints the session a real Keycloak login would.

    force_login() picks the first entry of AUTHENTICATION_BACKENDS, the
    Keycloak one, so SessionRefresh treats the session as an SSO session
    and bounces every authenticated GET to the provider unless the id
    token is recorded as fresh, exactly as the callback view records it.

    Mark a test ``no_sso_session`` to get the untouched force_login()
    back: a session with a stale id token is what the tests about the
    recheck itself are about.
    """
    if "no_sso_session" in request.keywords:
        return

    original = Client.force_login

    def force_login(self, user, backend=None, **kwargs):
        original(self, user, backend=backend, **kwargs)
        session = self.session
        session["oidc_id_token_expiration"] = (
            time.time() + settings.OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS
        )
        session.save()

    monkeypatch.setattr(Client, "force_login", force_login)


@pytest.fixture(autouse=True, scope="session")
def compiled_translations():
    """Compile .po -> .mo so translation-dependent tests pass.

    Uses polib instead of `manage.py compilemessages` so neither
    developers nor CI need GNU gettext installed.
    """
    for po_path in Path(__file__).parent.joinpath("locale").rglob("*.po"):
        mo_path = po_path.with_suffix(".mo")
        if not mo_path.exists() or mo_path.stat().st_mtime < po_path.stat().st_mtime:
            polib.pofile(str(po_path)).save_as_mofile(str(mo_path))


@pytest.fixture
def user(db):
    """A plain member account.

    This fixture (and logged_in_client) is the auth seam: tests that
    need an authenticated user go through here, never through login
    views or passwords, so replacing Django auth with SSO does not
    touch the test suite.
    """
    return get_user_model().objects.create_user(
        email="fixture-user@prodeko.org",
        first_name="Testi",
        last_name="Prodeko",
    )


@pytest.fixture
def logged_in_client(client, user):
    client.force_login(user)
    return client
