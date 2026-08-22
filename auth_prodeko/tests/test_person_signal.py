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


def test_a_slug_a_legacy_row_already_holds_does_not_break_the_sign_in():
    """Person.slug is unique and legacy rows carry numeric slugs of their
    own, so the primary key a new account gets can be taken already.
    Creating the account is someone's first sign-in: an IntegrityError
    there is a 500 they can neither act on nor get past by trying again.
    """
    Person.objects.create(member_type=0, slug="9999")

    user = User.objects.create_user(pk=9999, email="a@prodeko.org")

    assert Person.objects.get(user=user).slug == "9999-1"


def test_superuser_also_gets_a_profile():
    """Matrikkeli raises Person.DoesNotExist for an account without one,
    and being staff is no reason to be spared that."""
    user = User.objects.create_superuser(email="root@prodeko.org", password=None)
    assert Person.objects.filter(user=user).exists()


def test_profile_is_created_once_not_on_every_save():
    user = User.objects.create_user(email="a@prodeko.org")
    user.first_name = "Changed"
    user.save()
    assert Person.objects.filter(user=user).count() == 1


def test_login_does_not_reset_the_profile():
    """Every login writes last_login, which is a save on the account. A
    profile someone has edited must survive all of them."""
    user = User.objects.create_user(email="a@prodeko.org")
    person = Person.objects.get(user=user)
    person.city = "Espoo"
    person.save()

    user.save()  # stands in for the last_login update

    person.refresh_from_db()
    assert person.city == "Espoo"
