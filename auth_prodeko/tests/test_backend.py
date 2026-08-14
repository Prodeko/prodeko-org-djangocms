import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import SuspiciousOperation

from auth_prodeko.oidc.backend import KeycloakOIDCBackend

User = get_user_model()


@pytest.fixture(autouse=True)
def _db(db):
    pass


@pytest.fixture
def backend(settings):
    # The library's __init__ insists on these; nothing here contacts them.
    settings.OIDC_RP_CLIENT_ID = "prodekoorg"
    settings.OIDC_RP_CLIENT_SECRET = "secret"
    settings.OIDC_OP_TOKEN_ENDPOINT = "https://id.invalid/token"
    settings.OIDC_OP_USER_ENDPOINT = "https://id.invalid/userinfo"
    settings.OIDC_OP_JWKS_ENDPOINT = "https://id.invalid/certs"
    return KeycloakOIDCBackend()


def claims(**overrides):
    base = {
        "sub": "sub-1",
        "email": "maija@prodeko.org",
        "email_verified": True,
        "given_name": "Maija",
        "family_name": "Meikalainen",
        "realm_access": {"roles": ["membership"]},
    }
    base.update(overrides)
    return base


# --- verify_claims -------------------------------------------------------


def test_member_is_allowed(backend):
    assert backend.verify_claims(claims()) is True


def test_unverified_email_is_refused(backend):
    assert backend.verify_claims(claims(email_verified=False)) is False


def test_non_member_is_refused(backend):
    """Keycloak allows self-registration, so a bare account is not enough."""
    assert backend.verify_claims(claims(realm_access={"roles": []})) is False


def test_malformed_token_is_refused_not_raised(backend):
    assert backend.verify_claims(claims(sub="")) is False


# --- resolution ----------------------------------------------------------


def test_links_existing_row_by_email(backend):
    legacy = User.objects.create_user(
        email="maija@prodeko.org", first_name="Vanha", last_name="Nimi"
    )
    user = backend.update_user(backend.filter_users_by_claims(claims())[0], claims())
    assert user.pk == legacy.pk
    assert user.keycloak_sub == "sub-1"
    assert user.keycloak_linked_at is not None


def test_email_match_is_case_insensitive(backend):
    legacy = User.objects.create_user(email="Maija@Prodeko.ORG")
    assert backend.filter_users_by_claims(claims())[0].pk == legacy.pk


def test_subject_match_wins_over_email(backend):
    linked = User.objects.create_user(
        email="old-address@prodeko.org", keycloak_sub="sub-1"
    )
    User.objects.create_user(email="maija@prodeko.org")
    assert backend.filter_users_by_claims(claims())[0].pk == linked.pk


def test_row_linked_to_another_subject_is_not_adopted(backend):
    User.objects.create_user(email="maija@prodeko.org", keycloak_sub="someone-else")
    assert not backend.filter_users_by_claims(claims()).exists()


def test_break_glass_account_is_never_adopted(backend, settings):
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = "maija@prodeko.org"
    User.objects.create_user(email="maija@prodeko.org")
    assert not backend.filter_users_by_claims(claims()).exists()


def test_creates_a_user_when_nothing_matches(backend):
    user = backend.create_user(claims())
    assert user.email == "maija@prodeko.org"
    assert user.first_name == "Maija"
    assert user.keycloak_sub == "sub-1"
    assert not user.has_usable_password()


# --- privilege synchronisation -------------------------------------------


def test_admin_role_grants_staff(backend):
    user = backend.create_user(
        claims(realm_access={"roles": ["membership", "prodeko-org-admin"]})
    )
    assert user.is_staff is True
    assert user.is_superuser is False


def test_superuser_role_grants_both(backend):
    user = backend.create_user(
        claims(realm_access={"roles": ["membership", "prodeko-org-superuser"]})
    )
    assert user.is_staff is True
    assert user.is_superuser is True


def test_losing_the_role_revokes_staff(backend):
    user = User.objects.create_user(
        email="maija@prodeko.org", keycloak_sub="sub-1", is_staff=True
    )
    updated = backend.update_user(user, claims())
    assert updated.is_staff is False


def test_adopting_a_stale_staff_row_does_not_escalate(backend):
    """A dormant admin account must not confer admin on whoever claims it."""
    User.objects.create_user(
        email="maija@prodeko.org", is_staff=True, is_superuser=True
    )
    user = backend.update_user(backend.filter_users_by_claims(claims())[0], claims())
    assert user.is_staff is False
    assert user.is_superuser is False


def test_inactive_row_is_reactivated_on_login(backend):
    """Keycloak would not have issued a token for a disabled account."""
    User.objects.create_user(
        email="maija@prodeko.org", keycloak_sub="sub-1", is_active=False
    )
    user = backend.update_user(User.objects.get(keycloak_sub="sub-1"), claims())
    assert user.is_active is True


# --- email changes -------------------------------------------------------


def test_email_change_in_keycloak_is_applied(backend):
    User.objects.create_user(email="old@prodeko.org", keycloak_sub="sub-1")
    user = backend.update_user(User.objects.get(keycloak_sub="sub-1"), claims())
    assert user.email == "maija@prodeko.org"


def test_email_change_colliding_with_another_row_is_refused(backend):
    User.objects.create_user(email="old@prodeko.org", keycloak_sub="sub-1")
    User.objects.create_user(email="maija@prodeko.org")
    with pytest.raises(SuspiciousOperation):
        backend.update_user(User.objects.get(keycloak_sub="sub-1"), claims())
