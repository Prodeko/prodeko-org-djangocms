import pytest
from django.contrib.auth import get_user_model

from alumnirekisteri.rekisteri.models import Person

User = get_user_model()


@pytest.fixture(autouse=True)
def _db(db):
    pass


def test_new_member_gets_a_matrikkeli_profile():
    user = User.objects.create_user(email="a@prodeko.org")
    assert Person.objects.filter(user=user).exists()


def test_superuser_also_gets_a_profile():
    """The old guard skipped superusers, so matrikkeli raised
    Person.DoesNotExist for every one of them."""
    user = User.objects.create_superuser(email="root@prodeko.org", password=None)
    assert Person.objects.filter(user=user).exists()


def test_profile_is_created_once_not_on_every_save():
    user = User.objects.create_user(email="a@prodeko.org")
    user.first_name = "Changed"
    user.save()
    assert Person.objects.filter(user=user).count() == 1


def test_login_does_not_reset_the_profile():
    """The PendingUser branch used to rewrite member_until and the privacy
    flags on every save, including the last_login write at each login."""
    user = User.objects.create_user(email="a@prodeko.org")
    person = Person.objects.get(user=user)
    person.city = "Espoo"
    person.save()

    user.save()  # stands in for the last_login update

    person.refresh_from_db()
    assert person.city == "Espoo"
