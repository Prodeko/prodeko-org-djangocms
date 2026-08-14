from importlib import import_module

import pytest
from django.contrib.auth import get_user_model
from django.db import connection
from django.db.migrations.loader import MigrationLoader
from django.test import override_settings

from alumnirekisteri.rekisteri.migrations._backfill import backfill_profiles
from alumnirekisteri.rekisteri.models import Person

_migration = import_module(
    "alumnirekisteri.rekisteri.migrations.0004_backfill_profiles"
)

User = get_user_model()


def historical_apps():
    """The app registry the migration engine hands to ``forwards``.

    Its models are built from migration state, so ``Person`` there has none
    of the slug bookkeeping the real ``save()`` does.
    """
    # The suite runs with --nomigrations, which blanks MIGRATION_MODULES; the
    # override lets the loader see the real migration files again.
    with override_settings(MIGRATION_MODULES={}):
        state = MigrationLoader(connection).project_state(
            ("rekisteri", "0003_person_pora_member")
        )
    return state.apps


@pytest.fixture(autouse=True)
def _db(db):
    pass


def account_without_a_profile(email="orphan@prodeko.org"):
    """An account as the old signal left it: created, but no Person.

    The signal on the live model creates one for every account now, so the
    rows this migration exists for have to be made by taking it away again.
    """
    user = User.objects.create_user(email=email)
    Person.objects.filter(user=user).delete()
    return user


def test_missing_profile_is_created():
    user = account_without_a_profile()

    assert backfill_profiles(User, Person) == 1

    person = Person.objects.get(user=user)
    assert person.member_type == 0
    assert person.slug == str(user.pk)


def test_existing_profile_is_left_alone():
    user = User.objects.create_user(email="member@prodeko.org")
    person = Person.objects.get(user=user)
    person.city = "Espoo"
    person.member_type = 1
    person.save()

    assert backfill_profiles(User, Person) == 0

    assert Person.objects.filter(user=user).count() == 1
    person.refresh_from_db()
    assert person.city == "Espoo"
    assert person.member_type == 1


def test_second_run_changes_nothing():
    account_without_a_profile()
    backfill_profiles(User, Person)
    before = set(Person.objects.values_list("pk", "user_id", "slug", "member_type"))

    assert backfill_profiles(User, Person) == 0

    assert set(Person.objects.values_list("pk", "user_id", "slug", "member_type")) == (
        before
    )


def test_slug_already_taken_by_a_legacy_row_does_not_collide():
    user = account_without_a_profile()
    Person.objects.create(slug=str(user.pk))

    assert backfill_profiles(User, Person) == 1

    assert Person.objects.get(user=user).slug == f"{user.pk}-1"


def test_migration_creates_profiles_on_the_historical_models():
    user = account_without_a_profile()

    _migration.forwards(historical_apps(), None)

    person = Person.objects.get(user=user)
    assert person.member_type == 0
    assert person.slug == str(user.pk)


def test_profileless_accounts_are_found_among_profiled_ones():
    User.objects.create_user(email="member@prodeko.org")
    orphan = account_without_a_profile()
    User.objects.create_user(email="other@prodeko.org")

    assert backfill_profiles(User, Person) == 1

    assert Person.objects.filter(user=orphan).exists()
    assert Person.objects.count() == User.objects.count()
