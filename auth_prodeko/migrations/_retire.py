"""Retiring local passwords.

Kept out of the migration module so it can be tested directly: the suite
runs with --nomigrations and never executes migrations.
"""


def retire_passwords(user_model, break_glass_email: str) -> int:
    """Make every password unusable, except the break-glass account's.

    Returns the number of accounts changed.
    """
    accounts = user_model.objects.all()
    if break_glass_email:
        accounts = accounts.exclude(email__iexact=break_glass_email)

    changed = 0
    for user in accounts.iterator():
        if user.has_usable_password():
            user.set_unusable_password()
            user.save(update_fields=["password"])
            changed += 1
    return changed
