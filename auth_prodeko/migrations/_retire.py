"""Retiring local passwords.

Kept out of the migration module so it can be tested directly: the suite
runs with --nomigrations and never executes migrations.
"""

from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, make_password


def retire_passwords(user_model, break_glass_email: str) -> int:
    """Make every password unusable, except the break-glass account's.

    Works on the raw ``password`` column rather than ``AbstractBaseUser``'s
    helpers, because the migration engine hands this a historical model built
    from migration state, which has the fields but not the methods.

    Returns the number of accounts changed.
    """
    accounts = user_model.objects.all()
    if break_glass_email:
        accounts = accounts.exclude(email__iexact=break_glass_email)

    changed = 0
    for user in accounts.iterator():
        if not user.password.startswith(UNUSABLE_PASSWORD_PREFIX):
            user.password = make_password(None)
            user.save(update_fields=["password"])
            changed += 1
    return changed
