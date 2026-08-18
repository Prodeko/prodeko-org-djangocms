"""Grandfathering the accounts that exist when Keycloak takes over.

Kept out of the migration module so it can be tested directly: the suite
runs with --nomigrations and never executes migrations.
"""


def grandfather_existing_accounts(user_model) -> int:
    """Mark every account as predating Keycloak. Returns the count.

    Every row, with no exceptions. An account deactivated years ago still
    belongs to someone who was a member, and the break-glass account is
    kept out of the sign-in path where it is resolved rather than here.
    """
    return user_model.objects.update(predates_keycloak=True)
