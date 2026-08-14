import configparser

from django.conf import settings


def test_keycloak_settings_exist():
    assert isinstance(settings.KEYCLOAK_ISSUER, str)
    assert isinstance(settings.KEYCLOAK_CLIENT_ID, str)
    assert isinstance(settings.KEYCLOAK_CLIENT_SECRET, str)
    assert settings.KEYCLOAK_MEMBERSHIP_ROLES == ["membership"]
    assert settings.KEYCLOAK_STAFF_ROLE == "prodeko-org-admin"
    assert settings.KEYCLOAK_SUPERUSER_ROLE == "prodeko-org-superuser"


def test_missing_keycloak_section_falls_back_to_empty():
    """A variables.txt without [KEYCLOAK] must not break django.setup().

    deploy.sh runs collectstatic and migrate before Ansible has
    necessarily rendered the new section.
    """
    parser = configparser.ConfigParser(interpolation=None)
    parser.read_string("[DJANGO]\nSECRET = x\n")
    assert parser.get("KEYCLOAK", "ISSUER", fallback="") == ""


def test_client_secret_with_percent_sign_is_read_literally():
    """Keycloak secrets are opaque; a % must not be treated as interpolation."""
    parser = configparser.ConfigParser(interpolation=None)
    parser.read_string("[KEYCLOAK]\nCLIENT_SECRET = ab%cd\n")
    assert parser.get("KEYCLOAK", "CLIENT_SECRET") == "ab%cd"
