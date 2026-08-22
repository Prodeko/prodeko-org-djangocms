from importlib import import_module

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError, connection
from django.db.migrations.recorder import MigrationRecorder

from auth_prodeko.migrations import _drop_oauth2

_migration = import_module("auth_prodeko.migrations.0005_drop_oauth2_provider_tables")

User = get_user_model()


@pytest.fixture(autouse=True)
def _db(db):
    pass


@pytest.fixture(autouse=True)
def migration_history():
    """The applied-migration table every real database has.

    The suite runs with --nomigrations, so nothing records a migration and
    the table is absent; sqlite also refuses django's schema editor inside
    the transaction a test runs in, hence the hand-written DDL.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS "django_migrations" ('
            "id integer NOT NULL PRIMARY KEY AUTOINCREMENT, "
            "app varchar(255) NOT NULL, "
            "name varchar(255) NOT NULL, "
            "applied datetime NOT NULL)"
        )
    yield MigrationRecorder(connection)


def leftover_tables():
    """The oauth2_provider tables as django-oauth-toolkit left them.

    Each one carries a nullable foreign key to the user table, deferred to
    commit time exactly as django creates it, so a dangling reference only
    surfaces when the constraints are checked.
    """
    with connection.cursor() as cursor:
        for table in _drop_oauth2.OAUTH2_PROVIDER_TABLES:
            cursor.execute(
                f'CREATE TABLE "{table}" ('
                "id integer PRIMARY KEY, "
                f'user_id integer NULL REFERENCES "{User._meta.db_table}" ("id") '
                "DEFERRABLE INITIALLY DEFERRED)"
            )


def user_with_a_token():
    user = User.objects.create_user(email="member@prodeko.org")
    leftover_tables()
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO oauth2_provider_accesstoken (id, user_id) VALUES (1, %s)",
            [user.pk],
        )
    return user


def present_tables():
    return set(connection.introspection.table_names()) & set(
        _drop_oauth2.OAUTH2_PROVIDER_TABLES
    )


def test_a_leftover_token_blocks_deleting_its_user():
    """The hazard the drop exists to remove."""
    user_with_a_token().delete()

    with pytest.raises(IntegrityError):
        connection.check_constraints()

    # Leave no dangling row behind, or the test teardown trips over it too.
    _drop_oauth2.drop_oauth2_provider_tables(connection)


def test_a_user_with_a_leftover_token_can_be_deleted_once_the_tables_are_gone():
    user = user_with_a_token()

    _drop_oauth2.drop_oauth2_provider_tables(connection)
    user.delete()

    connection.check_constraints()
    assert not User.objects.filter(email="member@prodeko.org").exists()


def test_every_table_is_dropped():
    leftover_tables()

    _drop_oauth2.drop_oauth2_provider_tables(connection)

    assert present_tables() == set()


def test_dropping_twice_is_harmless():
    leftover_tables()

    _drop_oauth2.drop_oauth2_provider_tables(connection)
    _drop_oauth2.drop_oauth2_provider_tables(connection)

    assert present_tables() == set()


def test_the_provider_is_forgotten_by_the_migration_history(migration_history):
    migration_history.record_applied("oauth2_provider", "0001_initial")
    migration_history.record_applied("auth_prodeko", "0004_unusable_passwords")

    _drop_oauth2.drop_oauth2_provider_tables(connection)

    applied = migration_history.applied_migrations()
    assert ("oauth2_provider", "0001_initial") not in applied
    assert ("auth_prodeko", "0004_unusable_passwords") in applied


def test_the_migration_drops_the_tables():
    leftover_tables()

    _migration.forwards(None, connection.schema_editor())

    assert present_tables() == set()


def test_the_migration_follows_the_password_retirement():
    assert ("auth_prodeko", "0004_unusable_passwords") in (
        _migration.Migration.dependencies
    )
