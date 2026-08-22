"""Dropping the tables django-oauth-toolkit left behind.

Kept out of the migration module so it can be tested directly: the suite
runs with --nomigrations and never executes migrations.
"""

from django.db.migrations.recorder import MigrationRecorder

# Dependants first, so the drop also works on a backend without CASCADE.
OAUTH2_PROVIDER_TABLES = (
    "oauth2_provider_idtoken",
    "oauth2_provider_accesstoken",
    "oauth2_provider_refreshtoken",
    "oauth2_provider_grant",
    "oauth2_provider_application",
)


def drop_oauth2_provider_tables(connection) -> None:
    """Drop the provider's tables and forget that its migrations ran.

    Every one of these tables holds a foreign key to the user table. The
    library declares those as cascading, but the cascade is django's, not the
    database's: postgres is left with a plain deferred NO ACTION constraint.
    With the app uninstalled there is no model to cascade from, so a user who
    was ever issued a token could not be deleted at all while the tables
    stand.
    """
    cascade = " CASCADE" if connection.vendor == "postgresql" else ""
    with connection.cursor() as cursor:
        for table in OAUTH2_PROVIDER_TABLES:
            cursor.execute(f'DROP TABLE IF EXISTS "{table}"{cascade}')
    MigrationRecorder(connection).migration_qs.filter(app="oauth2_provider").delete()
