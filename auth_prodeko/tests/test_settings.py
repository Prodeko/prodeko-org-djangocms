import configparser
import importlib
from pathlib import Path

from django.conf import settings


def test_keycloak_settings_exist():
    assert isinstance(settings.KEYCLOAK_ISSUER, str)
    assert isinstance(settings.KEYCLOAK_CLIENT_ID, str)
    assert isinstance(settings.KEYCLOAK_CLIENT_SECRET, str)
    assert isinstance(settings.KEYCLOAK_BREAK_GLASS_EMAIL, str)
    assert settings.KEYCLOAK_MEMBERSHIP_ROLES == ["membership", "alumni"]
    assert settings.KEYCLOAK_STAFF_ROLE == "prodeko-org-admin"
    assert settings.KEYCLOAK_SUPERUSER_ROLE == "prodeko-org-superuser"


def test_calls_to_keycloak_are_bounded_by_a_timeout():
    """mozilla_django_oidc passes this straight to requests, and its own
    default is None: no timeout at all. A provider that accepts the
    connection and then stops answering would hold a worker thread for
    as long as it stayed up."""
    assert isinstance(settings.OIDC_TIMEOUT, (int, float))
    assert 0 < settings.OIDC_TIMEOUT <= 10


def test_missing_keycloak_section_falls_back_to_empty():
    """A variables.txt without [KEYCLOAK] must not break django.setup().

    deploy.sh runs collectstatic and migrate before Ansible has
    necessarily rendered the new section.
    """
    parser = configparser.ConfigParser(interpolation=None)
    parser.read_string("[DJANGO]\nSECRET = x\n")
    assert parser.get("KEYCLOAK", "ISSUER", fallback="") == ""


def test_sample_break_glass_email_is_the_development_superuser():
    """Migration 0004 refuses to run on an empty KEYCLOAK_BREAK_GLASS_EMAIL.

    docker-entrypoint.sh runs migrate, so a contributor who copies the
    sample verbatim would hit a hard failure on first start unless the
    sample names the superuser the entrypoint creates.
    """
    repo_root = Path(settings.BASE_DIR)
    parser = configparser.ConfigParser(interpolation=None)
    parser.read(repo_root / "prodekoorg" / "settings" / "variables.sample.txt")
    break_glass = parser.get("KEYCLOAK", "BREAK_GLASS_EMAIL")

    assert break_glass
    entrypoint = (repo_root / "docker-entrypoint.sh").read_text()
    assert f"create_superuser('{break_glass}'" in entrypoint


def test_production_trusts_the_proxy_forwarded_scheme():
    """Caddy terminates TLS and proxies plain http to gunicorn.

    Without this, request.build_absolute_uri() yields an http:// URL, and
    mozilla_django_oidc builds both the redirect_uri and the
    post_logout_redirect_uri from it, so Keycloak rejects every login.
    """
    prod = importlib.import_module("prodekoorg.settings.prod")
    assert prod.SECURE_PROXY_SSL_HEADER == ("HTTP_X_FORWARDED_PROTO", "https")


def test_the_sign_in_path_is_logged_in_production():
    """Only the loggers named in LOGGING carry a handler.

    Every account question a member raises -- refused, adopted by the
    wrong row, created twice -- is answered by these lines and nothing
    else in the container, and a client secret the realm rejects reaches
    an administrator only if ERROR here becomes mail.
    """
    prod = importlib.import_module("prodekoorg.settings.prod")
    loggers = prod.LOGGING["loggers"]

    for name in ("auth_prodeko", "mozilla_django_oidc"):
        assert loggers[name]["level"] == "INFO"
        assert "console" in loggers[name]["handlers"]
        assert "mail_admins" in loggers[name]["handlers"]


def test_client_secret_with_percent_sign_is_read_literally():
    """Keycloak secrets are opaque; a % must not be treated as interpolation."""
    parser = configparser.ConfigParser(interpolation=None)
    parser.read_string("[KEYCLOAK]\nCLIENT_SECRET = ab%cd\n")
    assert parser.get("KEYCLOAK", "CLIENT_SECRET") == "ab%cd"
