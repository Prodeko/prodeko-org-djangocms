import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

from auth_prodeko.migrations import _retire  # noqa: F401  (see step 3)

User = get_user_model()


@pytest.fixture(autouse=True)
def _db(db):
    pass


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


def test_setting_is_wired_up():
    assert hasattr(settings, "KEYCLOAK_BREAK_GLASS_EMAIL")
