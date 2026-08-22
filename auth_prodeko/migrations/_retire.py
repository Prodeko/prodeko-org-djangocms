"""Retiring local passwords.

Kept out of the migration module so it can be tested directly: the suite
runs with --nomigrations and never executes migrations.
"""

from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, make_password


def accounts_to_retire(user_model, break_glass_email: str):
    """The accounts a retirement would change: everyone still able to sign in.

    Excludes the break-glass account, which keeps its password, and accounts
    whose password is already unusable, which the retirement would leave
    untouched. Reading the raw ``password`` column keeps this usable on the
    historical model the migration engine builds from migration state, which
    has the fields but none of ``AbstractBaseUser``'s helpers.
    """
    accounts = user_model.objects.exclude(
        password__startswith=UNUSABLE_PASSWORD_PREFIX
    )
    if break_glass_email:
        accounts = accounts.exclude(email__iexact=break_glass_email)
    return accounts


def retire_passwords(user_model, break_glass_email: str) -> int:
    """Make every password unusable, except the break-glass account's.

    Returns the number of accounts changed.
    """
    changed = 0
    for user in accounts_to_retire(user_model, break_glass_email).iterator():
        user.password = make_password(None)
        user.save(update_fields=["password"])
        changed += 1
    return changed
