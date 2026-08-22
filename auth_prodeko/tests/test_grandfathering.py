"""The accounts that exist when Keycloak takes over keep their access.

Drives the migration's helper directly, because the suite runs with
--nomigrations.
"""

import pytest
from django.contrib.auth import get_user_model

from auth_prodeko.migrations._grandfather import grandfather_existing_accounts

User = get_user_model()


@pytest.fixture(autouse=True)
def _db(db):
    pass


def test_every_existing_account_is_grandfathered():
    User.objects.create_user(email="maija@prodeko.org")
    User.objects.create_user(email="matti@prodeko.org")

    grandfather_existing_accounts(User)

    assert User.objects.filter(predates_keycloak=False).count() == 0


def test_a_deactivated_account_is_grandfathered_too():
    """Deactivation is not the same as never having been a member, and
    the login reactivates whoever Keycloak still issues a token for."""
    User.objects.create_user(email="maija@prodeko.org", is_active=False)

    grandfather_existing_accounts(User)

    assert User.objects.get(email="maija@prodeko.org").predates_keycloak


def test_it_reports_how_many_accounts_it_changed():
    User.objects.create_user(email="maija@prodeko.org")

    assert grandfather_existing_accounts(User) == 1


def test_an_empty_database_is_no_obstacle():
    """A fresh install migrates before it has any account at all."""
    assert grandfather_existing_accounts(User) == 0
