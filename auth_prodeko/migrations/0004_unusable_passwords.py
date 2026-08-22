from django.conf import settings
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.db import migrations

from ._retire import accounts_to_retire, retire_passwords


class NoBreakGlassAccount(RuntimeError):
    """Raised when the break-glass account cannot actually be used."""


def check_break_glass_account(user_model, break_glass_email: str) -> None:
    """Refuse the retirement unless one account survives it and can sign in.

    Signing in means reaching the Django admin, the only page left with a
    password form once the site's own login form is gone. Its login form
    admits an account only when ``is_active`` and ``is_staff`` are both set,
    so a shared guild address that happens to exist as an ordinary member row
    is no rescue, and ``is_superuser`` on its own is not either.

    Reads the raw ``password`` column rather than ``has_usable_password()``,
    because the migration engine hands this a historical model built from
    migration state, which has the fields but not the methods.
    """
    if not break_glass_email:
        problem = "KEYCLOAK_BREAK_GLASS_EMAIL is empty"
    else:
        account = user_model.objects.filter(email__iexact=break_glass_email).first()
        if account is None:
            problem = f"no account has the address {break_glass_email}"
        elif not account.password or account.password.startswith(
            UNUSABLE_PASSWORD_PREFIX
        ):
            problem = f"the account {break_glass_email} has no usable password"
        else:
            missing = [
                flag for flag in ("is_active", "is_staff") if not getattr(account, flag)
            ]
            if not missing:
                return
            problem = (
                f"the account {break_glass_email} cannot reach the admin, the "
                "only page that still takes a password, because it is missing "
                f"{' and '.join(missing)}"
            )

    raise NoBreakGlassAccount(
        f"{problem}, so this migration would retire every password including "
        "the break-glass account's, leaving no way into the site while "
        "Keycloak is unreachable. Set [KEYCLOAK] BREAK_GLASS_EMAIL in the "
        "settings variables file, create an active staff account with that "
        "exact address, and give it a password. All of these are "
        "prerequisites of the deploy, not steps that follow it. Then run "
        "migrate again."
    )


def forwards(apps, schema_editor):
    break_glass_email = getattr(settings, "KEYCLOAK_BREAK_GLASS_EMAIL", "")
    user_model = apps.get_model("auth_prodeko", "User")

    # A database with no password to retire cannot be locked out of by this
    # migration, so it needs no break-glass account: a fresh install migrates
    # before it has any account at all.
    if not accounts_to_retire(user_model, break_glass_email).exists():
        return

    check_break_glass_account(user_model, break_glass_email)
    retire_passwords(user_model, break_glass_email)


class Migration(migrations.Migration):
    """Authentication moves to Keycloak; local passwords stop being usable.

    Deliberately irreversible: the hashes are gone once this has run, and
    restoring them is not something a reverse migration could do. Whenever it
    has a password to retire it therefore refuses to run at all unless the
    break-glass account exists, has a usable password and can reach the
    admin, so an outage of the identity provider cannot lock us out of our
    own site.
    """

    dependencies = [("auth_prodeko", "0003_keycloak_link")]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
