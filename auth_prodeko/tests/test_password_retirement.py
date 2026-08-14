from importlib import import_module

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import connection
from django.db.migrations.loader import MigrationLoader
from django.test import override_settings

from auth_prodeko.migrations import _retire  # noqa: F401  (see step 3)

_migration = import_module("auth_prodeko.migrations.0004_unusable_passwords")

User = get_user_model()


@pytest.fixture(autouse=True)
def _db(db):
    pass


def historical_apps():
    """The app registry the migration engine hands to ``forwards``.

    Its models are built from migration state, so they carry the fields but
    none of ``AbstractBaseUser``'s password helpers.
    """
    # The suite runs with --nomigrations, which blanks MIGRATION_MODULES; the
    # override lets the loader see the real migration files again.
    with override_settings(MIGRATION_MODULES={}):
        state = MigrationLoader(connection).project_state(
            ("auth_prodeko", "0003_keycloak_link")
        )
    return state.apps


def historical_user_model():
    return historical_apps().get_model("auth_prodeko", "User")


def test_retires_every_password():
    User.objects.create_user(email="a@prodeko.org", password="hunter2hunter2")
    _retire.retire_passwords(User, break_glass_email="")
    assert not User.objects.get(email="a@prodeko.org").has_usable_password()


def test_keeps_the_break_glass_password():
    User.objects.create_user(email="rescue@prodeko.org", password="hunter2hunter2")
    _retire.retire_passwords(User, break_glass_email="rescue@prodeko.org")
    assert User.objects.get(email="rescue@prodeko.org").has_usable_password()


def test_break_glass_match_is_case_insensitive():
    User.objects.create_user(email="Rescue@Prodeko.org", password="hunter2hunter2")
    _retire.retire_passwords(User, break_glass_email="rescue@prodeko.org")
    assert User.objects.get(email__iexact="Rescue@Prodeko.org").has_usable_password()


def test_retires_passwords_on_the_historical_model():
    User.objects.create_user(email="a@prodeko.org", password="hunter2hunter2")
    User.objects.create_user(email="rescue@prodeko.org", password="hunter2hunter2")

    changed = _retire.retire_passwords(
        historical_user_model(), break_glass_email="rescue@prodeko.org"
    )

    assert changed == 1
    assert not User.objects.get(email="a@prodeko.org").has_usable_password()
    assert User.objects.get(email="rescue@prodeko.org").has_usable_password()


def test_already_unusable_passwords_are_not_counted_again():
    user = User.objects.create_user(email="a@prodeko.org", password="hunter2hunter2")
    user.set_unusable_password()
    user.save(update_fields=["password"])

    assert _retire.retire_passwords(historical_user_model(), break_glass_email="") == 0


def test_migration_leaves_an_empty_database_alone(settings):
    """A fresh database has no password to retire, so nothing to guard."""
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = ""

    _migration.forwards(historical_apps(), None)

    assert not User.objects.exists()


def test_migration_passes_over_a_database_whose_passwords_are_already_gone(settings):
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = ""
    user = User.objects.create_user(email="a@prodeko.org", password=None)

    _migration.forwards(historical_apps(), None)

    user.refresh_from_db()
    assert not user.has_usable_password()


def test_migration_refuses_to_run_without_a_break_glass_email(settings):
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = ""
    User.objects.create_user(email="a@prodeko.org", password="hunter2hunter2")

    with pytest.raises(_migration.NoBreakGlassAccount):
        _migration.forwards(historical_apps(), None)

    assert User.objects.get(email="a@prodeko.org").has_usable_password()


def test_migration_refuses_when_no_account_holds_the_address(settings):
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = "rescue@prodeko.org"
    User.objects.create_user(email="a@prodeko.org", password="hunter2hunter2")

    with pytest.raises(_migration.NoBreakGlassAccount):
        _migration.forwards(historical_apps(), None)

    assert User.objects.get(email="a@prodeko.org").has_usable_password()


def test_migration_refuses_when_the_break_glass_password_is_unusable(settings):
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = "rescue@prodeko.org"
    User.objects.create_user(email="rescue@prodeko.org", password=None)
    User.objects.create_user(email="a@prodeko.org", password="hunter2hunter2")

    with pytest.raises(_migration.NoBreakGlassAccount):
        _migration.forwards(historical_apps(), None)

    assert User.objects.get(email="a@prodeko.org").has_usable_password()


def test_migration_runs_when_the_break_glass_account_can_sign_in(settings):
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = "rescue@prodeko.org"
    User.objects.create_user(email="rescue@prodeko.org", password="hunter2hunter2")

    _migration.forwards(historical_apps(), None)

    assert User.objects.get(email="rescue@prodeko.org").has_usable_password()


def test_the_break_glass_account_is_the_only_one_left_with_a_password(settings):
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = "rescue@prodeko.org"
    User.objects.create_user(email="rescue@prodeko.org", password="hunter2hunter2")
    User.objects.create_user(email="a@prodeko.org", password="hunter2hunter2")
    User.objects.create_user(email="b@prodeko.org", password="hunter2hunter2")

    _migration.forwards(historical_apps(), None)

    with_passwords = [
        user.email for user in User.objects.all() if user.has_usable_password()
    ]
    assert with_passwords == ["rescue@prodeko.org"]


def test_setting_is_wired_up():
    assert hasattr(settings, "KEYCLOAK_BREAK_GLASS_EMAIL")
