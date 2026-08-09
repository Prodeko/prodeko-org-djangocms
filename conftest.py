from pathlib import Path

import polib
import pytest
from django.contrib.auth import get_user_model


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(autouse=True, scope="session")
def compiled_translations():
    """Compile .po -> .mo so translation-dependent tests pass.

    Uses polib instead of `manage.py compilemessages` so neither
    developers nor CI need GNU gettext installed.
    """
    for po_path in Path(__file__).parent.joinpath("locale").rglob("*.po"):
        mo_path = po_path.with_suffix(".mo")
        if (
            not mo_path.exists()
            or mo_path.stat().st_mtime < po_path.stat().st_mtime
        ):
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
