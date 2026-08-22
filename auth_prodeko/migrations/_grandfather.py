"""Grandfathering the accounts that exist when Keycloak takes over.

Kept out of the migration module so it can be tested directly: the suite
runs with --nomigrations and never executes migrations.
"""


def grandfather_existing_accounts(user_model) -> int:
    """Mark every account as predating Keycloak. Returns the count.

    Every row, with no exceptions: the flag records when an account came
    into being, which is a fact about the row and not a decision about
    who may sign in. Whether it opens the site is settled at sign-in,
    which is also where the accounts that must never be adopted -- the
    deactivated ones and the break-glass account -- are set aside. A
    deactivated row carrying the flag is what makes reactivating it
    enough to let a former member back in.
    """
    return user_model.objects.update(predates_keycloak=True)
