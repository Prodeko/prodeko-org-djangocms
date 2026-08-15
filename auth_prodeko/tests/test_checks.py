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
}


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
    for other in {"ISSUER", "CLIENT_ID", "CLIENT_SECRET"} - {key}:
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


def test_all_three_missing_keys_are_named_at_once(settings):
    settings.DEBUG = False
    for name in CONFIGURED:
        setattr(settings, name, "")

    (error,) = check_keycloak_configured(app_configs=None)

    for key in ("ISSUER", "CLIENT_ID", "CLIENT_SECRET"):
        assert key in error.msg


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
