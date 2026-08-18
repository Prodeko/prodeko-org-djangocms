"""A production deploy with no Keycloak configuration must not start.

Every endpoint URL is an f-string built from KEYCLOAK_ISSUER, so an empty
issuer produces a login link to https://prodeko.org/protocol/... and a
CMS 404. Nothing else notices: manage.py check passes, collectstatic
copies its files, and deploy.sh's health check on /robots.txt returns
200, so the deploy is reported successful and the first person to find
out is a member trying to sign in.
"""

import pytest

from auth_prodeko.checks import check_keycloak_configured

CONFIGURED = {
    "KEYCLOAK_ISSUER": "https://id.prodeko.org/realms/membership-registry",
    "KEYCLOAK_CLIENT_ID": "prodekoorg",
    "KEYCLOAK_CLIENT_SECRET": "s3cret",
    "KEYCLOAK_BREAK_GLASS_EMAIL": "webbitiimi@prodeko.org",
}
KEYS = ("ISSUER", "CLIENT_ID", "CLIENT_SECRET", "BREAK_GLASS_EMAIL")


def test_a_configured_production_site_passes(settings):
    settings.DEBUG = False
    for name, value in CONFIGURED.items():
        setattr(settings, name, value)

    assert check_keycloak_configured(app_configs=None) == []


@pytest.mark.parametrize(
    ("setting", "key"),
    [
        ("KEYCLOAK_ISSUER", "ISSUER"),
        ("KEYCLOAK_CLIENT_ID", "CLIENT_ID"),
        ("KEYCLOAK_CLIENT_SECRET", "CLIENT_SECRET"),
        ("KEYCLOAK_BREAK_GLASS_EMAIL", "BREAK_GLASS_EMAIL"),
    ],
)
def test_production_refuses_a_missing_key_and_names_it(settings, setting, key):
    settings.DEBUG = False
    for name, value in CONFIGURED.items():
        setattr(settings, name, value)
    setattr(settings, setting, "")

    errors = check_keycloak_configured(app_configs=None)

    (error,) = errors
    assert error.id == "auth_prodeko.E001"
    assert key in error.msg
    # The keys that are configured are not reported as missing.
    for other in set(KEYS) - {key}:
        assert other not in error.msg
    assert "[KEYCLOAK]" in error.hint
    assert "variables.txt" in error.hint
    assert "Ansible" in error.hint


def test_a_whitespace_only_value_counts_as_missing(settings):
    settings.DEBUG = False
    for name, value in CONFIGURED.items():
        setattr(settings, name, value)
    settings.KEYCLOAK_CLIENT_SECRET = "   "

    errors = check_keycloak_configured(app_configs=None)

    assert len(errors) == 1
    assert "CLIENT_SECRET" in errors[0].msg


def test_every_missing_key_is_named_at_once(settings):
    """An operator filling them in one at a time and redeploying between
    each is four failed deploys."""
    settings.DEBUG = False
    for name in CONFIGURED:
        setattr(settings, name, "")

    (error,) = check_keycloak_configured(app_configs=None)

    for key in KEYS:
        assert key in error.msg


def test_an_empty_break_glass_address_fails_the_deploy(settings):
    """With nothing to compare against, the backend's exclusion matches
    no row, and a Keycloak identity registered at the break-glass address
    takes over the one account that still holds a usable password."""
    settings.DEBUG = False
    for name, value in CONFIGURED.items():
        setattr(settings, name, value)
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = ""

    (error,) = check_keycloak_configured(app_configs=None)

    assert "BREAK_GLASS_EMAIL" in error.msg


def test_development_is_left_alone(settings):
    """Contributors who are not working on authentication run with an
    empty [KEYCLOAK] section, and every manage.py command runs checks."""
    settings.DEBUG = True
    for name in CONFIGURED:
        setattr(settings, name, "")

    assert check_keycloak_configured(app_configs=None) == []


def test_the_check_is_registered_without_an_explicit_import():
    """auth_prodeko.apps imports the module, so django.setup() is enough."""
    from django.core.checks import registry

    assert check_keycloak_configured in registry.registry.get_checks()
