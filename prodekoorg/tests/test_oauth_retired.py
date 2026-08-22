import pytest
from django.conf import settings


@pytest.fixture(autouse=True)
def _db(db):
    pass


@pytest.mark.parametrize(
    "url", ["/oauth2/auth", "/oauth2/token", "/oauth2/user_details/"]
)
def test_provider_endpoints_are_gone(client, url):
    """Nothing under /oauth2/ resolves any more.

    The requests are followed because an unmatched path is redirected to
    its language-prefixed form first, where the django CMS catch-all
    answers with the 404.
    """
    assert client.get(url, follow=True).status_code == 404


def test_provider_app_is_uninstalled():
    assert "oauth2_provider" not in settings.INSTALLED_APPS
    assert "prodekoorg.app_oauth" not in settings.INSTALLED_APPS


def test_provider_middleware_and_backend_are_gone():
    assert not any("oauth2" in m for m in settings.MIDDLEWARE)
    assert not any("oauth2" in b for b in settings.AUTHENTICATION_BACKENDS)


def test_basic_auth_is_gone():
    """Email-and-password over HTTP is meaningless once passwords are unusable."""
    classes = settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]
    assert not any("BasicAuthentication" in c for c in classes)
