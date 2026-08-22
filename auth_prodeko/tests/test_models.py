import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

User = get_user_model()


@pytest.fixture(autouse=True)
def _db(db):
    pass


def test_new_user_has_no_keycloak_link():
    user = User.objects.create_user(email="a@prodeko.org")
    assert user.keycloak_sub is None
    assert user.keycloak_linked_at is None


def test_keycloak_sub_is_unique():
    User.objects.create_user(email="a@prodeko.org", keycloak_sub="sub-1")
    with pytest.raises(IntegrityError), transaction.atomic():
        User.objects.create_user(email="b@prodeko.org", keycloak_sub="sub-1")


def test_many_users_may_have_no_keycloak_sub():
    """Unique must not collapse the ~2000 unlinked legacy rows."""
    User.objects.create_user(email="a@prodeko.org")
    User.objects.create_user(email="b@prodeko.org")
    assert User.objects.filter(keycloak_sub__isnull=True).count() == 2
